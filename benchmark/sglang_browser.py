"""Counterbalanced WebArena runs with a disposable, GPU-local Inkling SGLang server."""

import json
import secrets
import subprocess
import time
from contextlib import contextmanager
from pathlib import Path
from urllib.request import Request, urlopen

import webarena_ten as bench
from cuda_worker import CudaWorker

IMAGE = "lmsysorg/sglang@sha256:efac853b46811ccb760545b7b29e7119bdf907537ccf6e863fac3011fe8b98de"


def mount(directory, arm):
    # HF cached snapshots use relative symlinks into the repository's blobs directory.
    path = directory.resolve()
    host = (
        path.parent.parent
        if path.parent.name == "snapshots" and (path.parent.parent / "blobs").is_dir()
        else path
    )
    target = "/weights/" + arm
    return ["--mount", f"type=bind,source={host},target={target},readonly"], str(
        Path(target) / path.relative_to(host)
    )


@contextmanager
def serve(directories, gpu):
    mounts = []
    paths = {}
    for arm, directory in directories.items():
        args, paths[arm] = mount(directory, arm)
        mounts.extend(args)
    key = secrets.token_urlsafe(36)
    flags = [
        "--context-length",
        "8192",
        "--max-running-requests",
        "4",
        "--swa-full-tokens-ratio",
        "0.20",
        "--mamba-radix-cache-strategy",
        "extra_buffer",
        "--chunked-prefill-size",
        "4096",
        "--enable-mixed-chunk",
        "--schedule-policy",
        "lpm",
        "--attention-backend",
        "fa4",
        "--cuda-graph-max-bs-decode",
        "4",
        "--cuda-graph-config",
        '{"prefill":{"backend":"disabled"}}',
        "--mem-fraction-static",
        "0.78",
        "--enable-cache-report",
    ]
    command = [
        "docker",
        "run",
        "-d",
        "--rm",
        "--gpus",
        f"device={gpu}",
        "--shm-size=6g",
        "-p",
        "127.0.0.1::30000",
        "-e",
        "HF_HUB_OFFLINE=1",
        "-e",
        "SGLANG_ENABLE_UNIFIED_RADIX_TREE=1",
        "-e",
        "PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True",
        *mounts,
        IMAGE,
        "sglang",
        "serve",
        "--model-path",
        paths["original"],
        "--served-model-name",
        "inkling-browser-repro",
        "--trust-remote-code",
        "--admin-api-key",
        key,
        "--host",
        "0.0.0.0",
        "--port",
        "30000",
        *flags,
    ]
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    if result.returncode:
        raise RuntimeError(
            "Docker could not start the Inkling server. "
            + result.stderr[-1000:].replace(key, "[redacted]")
        )
    container = result.stdout.strip()
    try:
        binding = subprocess.check_output(
            ["docker", "port", container, "30000/tcp"], text=True
        ).strip()
        if not binding.startswith("127.0.0.1:"):
            raise RuntimeError("Expected a loopback-only Docker server port.")
        origin = "http://" + binding
        until = time.monotonic() + 400
        while time.monotonic() < until:
            try:
                with urlopen(origin + "/v1/models", timeout=3) as response:
                    if any(
                        m["id"] == "inkling-browser-repro"
                        for m in json.load(response)["data"]
                    ):
                        break
            except OSError:
                pass
            state = subprocess.run(
                ["docker", "inspect", "--format", "{{.State.Running}}", container],
                capture_output=True,
                text=True,
                check=False,
            )
            if state.stdout.strip() != "true":
                raise RuntimeError(
                    "The SGLang container exited during startup. Check GPU memory and NVIDIA Docker support."
                )
            time.sleep(2)
        else:
            raise RuntimeError("The SGLang server did not become ready.")
        devices = (
            subprocess.check_output(
                [
                    "docker",
                    "exec",
                    container,
                    "nvidia-smi",
                    "--query-gpu=name,uuid",
                    "--format=csv,noheader",
                ],
                text=True,
            )
            .strip()
            .splitlines()
        )
        if len(devices) != 1:
            raise RuntimeError(
                "Expected one visible NVIDIA device in the inference container."
            )
        device, uuid = (part.strip() for part in devices[0].split(",", 1))
        yield origin, key, paths, {"device": device, "gpu_uuid": uuid}
    finally:
        subprocess.run(
            ["docker", "stop", "--time", "8", container],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )


def load_arm(endpoint, key, path, digest):
    headers = {"Content-Type": "application/json", "Authorization": "Bearer " + key}
    payload = {
        "model_path": path,
        "weight_version": digest,
        "abort_all_requests": False,
        "flush_cache": True,
        "recapture_cuda_graph": False,
    }
    with urlopen(
        Request(
            endpoint + "/update_weights_from_disk",
            data=json.dumps(payload).encode(),
            headers=headers,
        ),
        timeout=150,
    ) as response:
        result = json.load(response)
    if not result.get("success") or digest not in result.get("message", ""):
        raise RuntimeError("SGLang did not acknowledge the requested checkpoint.")
    with urlopen(
        Request(endpoint + "/model_info", headers=headers), timeout=8
    ) as response:
        if json.load(response).get("weight_version") != digest:
            raise RuntimeError("Loaded weight version differs from the verified shard.")
    with urlopen(
        Request(endpoint + "/flush_cache?timeout=8", headers=headers), timeout=15
    ) as response:
        if "Cache flushed" not in response.read().decode():
            raise RuntimeError("SGLang did not flush the previous episode.")


def compare(
    browser,
    endpoint,
    load_checkpoint,
    args,
    grader,
    site,
    directories,
    digests,
    hardware,
):
    pairs = []
    for rep, order in enumerate((("edited", "original"), ("original", "edited")), 1):
        case_dir = args.out / f"r{rep}"
        case_dir.mkdir()
        records = {}
        for arm in order:
            bench.fresh(site)
            load_checkpoint(arm)
            worker = CudaWorker(
                endpoint,
                directories[arm],
                dict(
                    **hardware,
                    engine="SGLang",
                    sampler="greedy",
                    token_limit=512,
                    shard_sha256=digests[arm],
                    server_image=IMAGE,
                ),
                token_limit=512,
            )
            worker.decide_web("Click Go. Controls: 7 button Go.", bench.SYSTEM)
            bench.episode(
                browser,
                worker,
                grader,
                {"id": args.id, "site": site},
                arm,
                case_dir,
                fixture_reset=lambda _: None,
                field_selection="keyboard",
            )
            records[arm] = json.loads(
                (case_dir / f"{args.id:03}-{arm}.json").read_text()
            )
        stock, edited = records["original"], records["edited"]
        if (
            any(r["grader_error"] for r in records.values())
            or stock["steps"][0]["view"] != edited["steps"][0]["view"]
        ):
            raise RuntimeError(
                "The native grader or initial browser observations do not match the protocol."
            )
        joint = stock["score"] == edited["score"] == 1
        pairs.append(
            {
                "repeat": rep,
                "order": list(order),
                "original_score": stock["score"],
                "edited_score": edited["score"],
                "original_s": stock["elapsed_s"],
                "edited_s": edited["elapsed_s"],
                "ratio": stock["elapsed_s"] / edited["elapsed_s"] if joint else None,
            }
        )
        bench.write_json(
            args.out / "pairs.json",
            {"id": args.id, "shard_sha256": digests, "pairs": pairs},
        )


def run_pairs(args, grader, site, directories, digests):
    args.out.mkdir(parents=True, exist_ok=False)
    with (
        serve(directories, args.gpu) as (endpoint, key, paths, hardware),
        bench.sync_playwright() as pw,
    ):
        browser = (
            pw.chromium.connect_over_cdp(args.cdp)
            if args.cdp
            else pw.chromium.launch(executable_path=args.brave, headless=True)
        )
        try:
            compare(
                browser,
                endpoint,
                lambda arm: load_arm(endpoint, key, paths[arm], digests[arm]),
                args,
                grader,
                site,
                directories,
                digests,
                hardware,
            )
        finally:
            if not args.cdp:
                browser.close()

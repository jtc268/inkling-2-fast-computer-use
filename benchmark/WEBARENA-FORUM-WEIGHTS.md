# Forum submission weights

On WebArena 630 the M5 Max MacBook Pro submitted the requested post in 20.95 seconds with this checkpoint. Stock failed after 95.01 seconds. Both used the same browser, prompt, greedy decoder and 512-token limit per decision. The edit emitted 74 reasoning tokens when choosing the forum.

The browser action for scrolling is `D`. The earlier edit emitted `DONE mutate` instead. Both commands start with the same token. We measured the next-token scores with the model's ordinary decode cache and edited four output rows relative to that earlier checkpoint. Across the full series of edits, 20,518 BF16 values changed across nine rows relative to upstream Inkling 2 Mini. The byte audit covers the full shard and the accompanying model files.

The complete replacement rows reconstruct the tested checkpoint checksum from the pinned stock model.

```sh
python benchmark/verify_row_payload.py /path/to/Inkling-2-Mini evidence/webarena-forum-controls/rows.npz evidence/webarena-forum-controls/weight-audit.json
```

[Stock checkpoint](https://huggingface.co/thinkingmachines/Inkling-2-Mini/tree/ed40e7da625f594fc9c4990f5f66be24873c22d7) · [Weights and native grade archive](../evidence/webarena-forum-controls/) · [All forum trials](WEBARENA-FORUM-CONTROLS.md)

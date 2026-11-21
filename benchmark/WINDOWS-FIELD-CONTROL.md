# Windows field replacement control

This control uses the same stock and edited Inkling 2 Mini checkpoints as the earlier shopping search. Both arms select the existing field text through Playwright before typing. The cursor animation, 25 ms typing delay, prompt, greedy sampler, 512-token limit and fresh browser fixtures match within each pair. The previous Windows run used a keyboard shortcut from the Mac controller.

| WebArena task | Field selection | Stock | Edited | Passing ratio |
|---|---|---:|---:|---:|
| 278 · Green tea bags | Keyboard shortcut | 6.92 s · pass | 11.51 s · fail | — |
| 278 · Green tea bags | Playwright select-text | 7.34 s · pass | 6.19 s · pass | 1.19× |
| 630 · Headphone forum post | Playwright select-text | 22.34 s · pass | 2.11 s · fail | — |

The portable green-tea edit issued 2 fill commands in 4 decisions and scored 1. All four portable grades replayed with WebArena-Verified 1.2.3. A speed ratio describes stock and edited runs under the same field-selection setting.

[Prior run, fixed-screen counterfactuals and byte audit](WEBARENA-QUERY-TRANSFER.md) · [Input field test](../evidence/webarena-windows-field/windows-field-control.json) · [Native grade replay](../evidence/webarena-windows-field/portable-grade-replay.zip) · [Browser recordings](../evidence/webarena-windows-field/portable-recordings.zip)

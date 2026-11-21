# Compare unit prices in two tabs and add one item to the cart

WebArena 432 ran in Brave on M5 Max MacBook Pro. Both models used the same keyboard controls, cursor, prompt, greedy decoder and 512-token decision limit. Each episode started with a fresh shopping fixture.

We froze the published command-stop checkpoint and selected the first ungraded shopping-only cart task with a native network-event evaluator. WebArena opened two product tabs and asked for the item with the lowest unit price. The evaluator checked the browser’s recorded requests and the final task response.

| First model | Stock Inkling 2 Mini | Stop-row edit | Time-to-success speedup |
|---|---:|---:|---:|
| Stop-row edit | fail · 34.84 s | fail · 11.12 s | — |

Both models stayed in a tab-switch loop. The model saw the active page, the open tab titles and its recent commands. Prices from previous pages were absent from the next prompt.

A separate walkthrough using the same browser controls opened the storefront comparison list. Its visible page showed $36.99 and $14.47 together. A separate cart check increased the quantity of the selected test product by one. [Storefront control receipts](../evidence/webarena-cart-transfer/storefront-controls.json).

2 recorded native grades reproduced. A speedup requires two passing grades.

[Exact weights](WEBARENA-ORDER-STOP.md) · [Grade receipts and recorded network traces](../evidence/webarena-cart-transfer/native-grades.zip)

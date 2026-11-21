# Every browser task in order

[Watch the 3:45 film](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4). Form fill and add to cart come first, followed by five MiniWoB++ tasks and 34 WebArena tasks in ID order. Each chapter names the checkpoint and shows the full-task times. The browser excerpts play at 1×. Paired successes share an elapsed clock wherever the recordings have timing markers. Two WebArena tasks have only a stock run.

**8.95× on the completed-order lookup.** On M5 Max MacBook Pro stock took 45.89 seconds and the cross-device order stop took 5.13 seconds. Both passed again in the opposite order at 8.00×. This task was used to develop the edit. [Native grades](WEBARENA-ORDER-CHECKPOINTS.md).

**6.78× on the latest-order lookup.** On the M5 Max MacBook Pro the published browser-search weights took 46.71 seconds and the sampling-stop edit took 6.89 seconds. Both issued the same five commands and returned the correct order status. Model generation took 43.73 and 3.88 seconds. The upstream-stock attempt appears in the same chapter and failed. [Windows stock comparison](WEBARENA-ORDER-WINDOWS.md) · [Both Mac run orders and exact weights](WEBARENA-ORDER-STOP.md).

**5.34× against upstream stock on a fresh order task.** Both models found the total of the latest canceled order. Stock took 27.83 seconds and the frozen stop-row weights took 5.22 seconds. [Both orders and native grades](WEBARENA-NEXT-ORDER.md).

**5.18× on MiniWoB++ autocomplete against upstream stock.** The fastest passing pair took 19.86 and 3.84 seconds. The filmed M5 Max MacBook Pro repeat took 15.46 and 3.36 seconds, saving 12.11 seconds.

**4.12× on WebArena Xbox search.** Stock took 20.43 seconds and the click-row edit took 4.96 seconds on the M5 Max MacBook Pro. Both passed. Reversing model order also produced two passes. The other pair measured 3.55×. The five Mac shopping chapters use the same edited checkpoint. Green tea served as a development task. The Windows green-tea chapter shows the original click-row edit failing with the keyboard shortcut, followed by the native click-row edit passing on the same controls. [Both Windows orders and input methods](WEBARENA-NATIVE-CLICK.md). The forum chapter includes the cached-submit edit completing a fresh post on Mac, the earlier one-row success on Windows, and the same Mac-passing checkpoint failing to select the forum on Windows.

[Frozen search weights on latest-order retrieval and forum weights on shopping](WEBARENA-CROSS-TASK.md) · [Forum submission trials and grade replay](WEBARENA-FORUM-CONTROLS.md) · [Exact forum weight changes](WEBARENA-FORUM-WEIGHTS.md) · [Sony headphone lookup, both grades and trace replay](WEBARENA-PRODUCT-LOOKUP.md) · [Canceled order total on Windows](WEBARENA-NEXT-ORDER-WINDOWS.md) · [Fresh pending-order lookup](WEBARENA-PENDING-ORDER.md) · [Frozen shopping rechecks and earlier trials](WEBARENA-FROZEN-CHECKPOINT.md) · [Latest canceled order total, both Mac grades](WEBARENA-NEXT-ORDER.md) · [Shopping pairs, weight audit and native grades](WEBARENA-CLICK-ROW.md) · [Earlier shopping and forum runs](WEBARENA-QUERY-TRANSFER.md) · [Previous cut](https://raw.githubusercontent.com/jtc268/inkling-2-fast-computer-use/48ad144e58f9a27e4c5199550d6b56ee01dd5a30/docs/browser-benchmark-in-order.mp4)

**All five storefront searches.** On the M5 Max MacBook Pro, stock and one frozen edit each passed 10 of 10 runs. The edit was 2.13× to 4.09× faster across the ten pairs. [Times and checkpoint](WEBARENA-ORDER-CHECKPOINTS.md#five-storefront-searches).

| Start | Task | Baseline | Edited | Speedup | Device |
|---:|---|---:|---:|---:|---|
| [0:06](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=6.15) | Fill and submit a form | pass · 8.64 s | pass · 3.06 s · Two-row swap | 2.83× | M5 Max MacBook Pro |
| [0:10](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=10.40) | Set quantity to two and add the dress | pass · 16.96 s | pass · 7.15 s · Two-row swap | 2.37× | M5 Max MacBook Pro |
| [0:14](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=14.65) | Complete an autocomplete field | pass · 15.46 s | pass · 3.36 s · Two-row swap | 4.61× | M5 Max MacBook Pro |
| [0:19](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=19.40) | Reply to an email | pass · 26.01 s | pass · 5.98 s · Two-row swap | 4.35× | M5 Max MacBook Pro |
| [0:24](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=24.15) | Like every post from one account | fail · 20.16 s | fail · 5.83 s · Two-row swap | — | M5 Max MacBook Pro |
| [0:27](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=27.10) | Pick a date | pass · 21.57 s | fail · 16.95 s · Two-row swap | — | M5 Max MacBook Pro |
| [0:30](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=30.05) | Book the shortest one-way flight | fail · 63.25 s | fail · 90.68 s · Two-row swap | — | M5 Max MacBook Pro |
| [0:33](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=33.00) | Read headphone reviews · WebArena 21 | fail · 14.29 s | fail · 9.80 s · Selective edit | — | RTX 5090 |
| [0:35](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=35.20) | Read the latest finance discussion · WebArena 27 | fail · 12.02 s | fail · 1.04 s · Selective edit | — | RTX 5090 |
| [0:37](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=37.40) | Find the customer with the most completed orders · WebArena 62 | fail · 75.50 s | fail · 0.72 s · Frozen pending-order weights | — | M5 Max MacBook Pro |
| [0:39](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=39.60) | Find book recommendations · WebArena 66 | fail · 93.17 s | fail · 32.15 s · Selective edit | — | M5 Max MacBook Pro |
| [0:41](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=41.80) | Track the latest order · WebArena 96 | pass · 46.71 s · Published search weights | pass · 6.89 s · Stop-row edit | 6.78× | M5 Max MacBook Pro |
| [0:46](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=46.95) | Track the latest order · WebArena 96 | fail · 65.12 s | pass · 50.32 s · Native click-row edit | — | M5 Max MacBook Pro |
| [0:49](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=49.50) | Track the latest order · WebArena 96 | fail · 26.09 s | pass · 12.52 s · Stop-row edit | — | RTX 5090 |
| [0:52](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=52.25) | Track the latest order · WebArena 96 | pass · 48.34 s · Published search weights | pass · 6.91 s · Cross-device order stop | 7.00× | M5 Max MacBook Pro |
| [0:55](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=55.15) | Find low-star review titles · WebArena 163 | fail · 2.51 s | fail · 0.48 s · Selective edit | — | RTX 5090 |
| [0:57](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=57.35) | Find the total of the latest canceled order · WebArena 188 | pass · 27.83 s | pass · 5.22 s · Stop-row edit | 5.34× | M5 Max MacBook Pro |
| [1:01](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=61.45) | Find the total of the latest canceled order · WebArena 188 | pass · 6.46 s | pass · 6.31 s · Stop-row edit | 1.02× | RTX 5090 |
| [1:04](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=64.00) | Find the total of the latest canceled order · WebArena 188 | pass · 9.63 s | fail · 6.73 s · Order click edit | — | RTX 5090 |
| [1:06](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=66.60) | Find the total of the latest canceled order · WebArena 188 | pass · 6.86 s | pass · 2.65 s · Order boundary edit | 2.59× | RTX 5090 |
| [1:09](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=69.15) | Find the total of the latest canceled order · WebArena 188 | pass · 45.75 s | pass · 6.44 s · Completed-order stop edit | 7.10× | M5 Max MacBook Pro |
| [1:12](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=72.05) | Find the total of the latest pending order · WebArena 189 | pass · 33.85 s | pass · 33.24 s · Published stop-row weights | 1.02× | M5 Max MacBook Pro |
| [1:16](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=76.10) | Find the total of the latest pending order · WebArena 189 | pass · 23.86 s | pass · 4.16 s · Pending click + stop edit | 5.74× | M5 Max MacBook Pro |
| [1:18](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=78.70) | Find the total of the latest pending order · WebArena 189 | pass · 12.52 s | pass · 3.59 s · Frozen pending-order weights | 3.49× | RTX 5090 |
| [1:21](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=81.60) | Find the total of the latest pending order · WebArena 189 | pass · 33.17 s | pass · 5.30 s · Completed-order stop edit | 6.25× | M5 Max MacBook Pro |
| [1:24](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=84.50) | Find the total of the latest pending order · WebArena 189 | pass · 33.13 s | pass · 5.25 s · Cross-device order stop | 6.31× | M5 Max MacBook Pro |
| [1:27](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=87.40) | Find the total of the latest pending order · WebArena 189 | pass · 6.77 s | pass · 2.87 s · Order-history routing trial | 2.36× | RTX 5090 |
| [1:30](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=90.30) | Find the total of the latest completed order · WebArena 190 | pass · 45.50 s | pass · 18.33 s · Frozen pending-order weights | 2.48× | M5 Max MacBook Pro |
| [1:33](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=93.95) | Find the total of the latest completed order · WebArena 190 | pass · 45.34 s | pass · 5.19 s · Completed-order stop edit | 8.73× | M5 Max MacBook Pro |
| [1:36](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=96.90) | Find the total of the latest completed order · WebArena 190 | pass · 12.15 s | pass · 8.93 s · Completed-order stop edit | 1.36× | RTX 5090 |
| [1:39](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=99.85) | Find the total of the latest completed order · WebArena 190 | pass · 9.33 s | fail · 3.29 s · Cross-device order stop | — | RTX 5090 |
| [1:42](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=102.80) | Find the total of the latest completed order · WebArena 190 | pass · 45.89 s | pass · 5.13 s · Cross-device order stop | 8.95× | M5 Max MacBook Pro |
| [1:45](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=105.75) | Find the total of the latest completed order · WebArena 190 | pass · 10.33 s | pass · 3.34 s · Guarded reasoning trial | 3.09× | RTX 5090 |
| [1:48](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=108.70) | Find the total of the latest completed order · WebArena 190 | pass · 10.09 s | pass · 4.64 s · Order-history routing trial | 2.18× | RTX 5090 |
| [1:51](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=111.65) | Find the total of the latest processing order · WebArena 191 | fail · 72.89 s | grader error · 19.84 s · Completed-order stop edit | — | M5 Max MacBook Pro |
| [1:53](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=113.85) | Find the total of the latest processing order · WebArena 191 | fail · 11.73 s | grader error · 3.01 s · Completed-order stop edit | — | RTX 5090 |
| [1:56](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=116.80) | Find a canceled order number · WebArena 231 | fail · 6.66 s | fail · 4.07 s · Selective edit | — | RTX 5090 |
| [1:59](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=119.00) | Find a canceled order number · WebArena 231 | fail · 31.38 s | pass · 5.12 s · Completed-order stop edit | — | M5 Max MacBook Pro |
| [2:01](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=121.90) | Browse video games · WebArena 260 | fail · 1.73 s | fail · 2.55 s · Selective edit | — | RTX 5090 |
| [2:04](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=124.10) | Filter shoes under $25 · WebArena 269 | fail · 31.29 s | fail · 27.34 s · Click / stop edit | — | RTX 5090 |
| [2:06](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=126.30) | Filter men’s shoes below $30 · WebArena 270 | fail · 26.59 s | fail · 7.78 s · Four-row edit | — | RTX 5090 |
| [2:08](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=128.50) | Search for a USB Wi-Fi adapter · WebArena 274 | pass · 14.63 s | pass · 4.72 s · Published stop-row weights | 3.10× | M5 Max MacBook Pro |
| [2:13](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=133.25) | Search for a USB Wi-Fi adapter · WebArena 274 | pass · 14.35 s | pass · 5.39 s · Completed-order stop edit | 2.66× | M5 Max MacBook Pro |
| [2:16](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=136.15) | Search for Xbox · WebArena 275 | pass · 20.43 s | pass · 4.96 s · Click-row edit | 4.12× | M5 Max MacBook Pro |
| [2:22](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=142.20) | Search for Xbox · WebArena 275 | pass · 5.01 s | pass · 6.08 s · Completed-order stop edit | 0.82× | RTX 5090 |
| [2:25](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=145.10) | Search for Xbox · WebArena 275 | pass · 20.92 s | pass · 5.12 s · Completed-order stop edit | 4.09× | M5 Max MacBook Pro |
| [2:28](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=148.00) | Search for Switch accessories · WebArena 276 | pass · 12.93 s | pass · 5.34 s · Published stop-row weights | 2.42× | M5 Max MacBook Pro |
| [2:32](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=152.75) | Search for Switch accessories · WebArena 276 | pass · 5.32 s | pass · 3.70 s · Query-transfer edit | 1.44× | RTX 5090 |
| [2:35](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=155.75) | Search for Switch accessories · WebArena 276 | pass · 14.73 s | pass · 5.50 s · Completed-order stop edit | 2.68× | M5 Max MacBook Pro |
| [2:38](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=158.65) | Search for iPhone 13 batteries · WebArena 277 | pass · 16.96 s | pass · 5.82 s · Published stop-row weights | 2.91× | M5 Max MacBook Pro |
| [2:43](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=163.40) | Search for iPhone 13 batteries · WebArena 277 | pass · 19.38 s | pass · 5.88 s · Completed-order stop edit | 3.30× | M5 Max MacBook Pro |
| [2:46](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=166.30) | Search for green tea bags · WebArena 278 | pass · 18.84 s | pass · 7.61 s · Click-row edit | 2.47× | M5 Max MacBook Pro |
| [2:51](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=171.05) | Search for green tea bags · WebArena 278 | pass · 6.49 s | fail · 7.74 s · Click-row edit | — | RTX 5090 |
| [2:54](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=174.05) | Search for green tea bags · WebArena 278 | pass · 6.58 s | pass · 5.08 s · Native click-row edit | 1.29× | RTX 5090 |
| [2:56](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=176.60) | Search for green tea bags · WebArena 278 | pass · 24.29 s | pass · 6.12 s · Completed-order stop edit | 3.97× | M5 Max MacBook Pro |
| [2:59](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=179.50) | Find Sony headphone models and prices · WebArena 279 | fail · 58.91 s | fail · 8.50 s · Click-row edit | — | M5 Max MacBook Pro |
| [3:01](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=181.70) | Find Xbox controllers released in 2020–2021 · WebArena 283 | fail · 81.34 s | fail · 12.87 s · Completed-order stop edit | — | M5 Max MacBook Pro |
| [3:03](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=183.90) | Find Xbox controllers released in 2020–2021 · WebArena 283 | fail · 87.93 s | fail · 18.77 s · Focused search-field edit | — | M5 Max MacBook Pro |
| [3:06](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=186.85) | Find customer service · WebArena 313 | fail · 15.73 s | fail · 17.03 s · Click / stop edit | — | RTX 5090 |
| [3:09](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=189.05) | Sort chairs by price · WebArena 324 | fail · 30.03 s | fail · 11.18 s · Selective edit | — | RTX 5090 |
| [3:11](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=191.25) | Check how an order shipped · WebArena 358 | fail · 9.76 s | fail · 18.59 s · Selective edit | — | RTX 5090 |
| [3:13](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=193.45) | Edit a forum profile · WebArena 399 | fail · 5.17 s | fail · 5.20 s · Click / stop edit | — | RTX 5090 |
| [3:15](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=195.65) | Upvote the newest book post · WebArena 404 | fail · 29.58 s | fail · 27.15 s · Click / stop edit | — | RTX 5090 |
| [3:17](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=197.85) | Add the lowest-unit-price item to the cart · WebArena 431 | fail · 15.82 s | fail · 8.89 s · Four-row edit | — | RTX 5090 |
| [3:20](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=200.05) | Compare two drinks and add the cheaper one per unit · WebArena 432 | fail · 34.84 s | fail · 11.12 s · Stop-row edit | — | M5 Max MacBook Pro |
| [3:23](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=203.60) | Save a product to a wishlist · WebArena 516 | fail · 24.60 s | pass · 3.06 s · Click / stop edit | — | RTX 5090 |
| [3:25](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=205.80) | Follow the space forum · WebArena 595 | fail · 24.93 s | fail · 24.44 s · Click / stop edit | — | RTX 5090 |
| [3:28](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=208.00) | Ask which console to buy · WebArena 600 | fail · 15.43 s | Unrun | — | RTX 5090 |
| [3:30](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=210.20) | Ask for headphone recommendations · WebArena 630 | fail · 95.01 s | pass · 20.95 s · Cached-submit edit | — | M5 Max MacBook Pro |
| [3:32](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=212.40) | Ask for headphone recommendations · WebArena 630 | pass · 24.52 s | pass · 20.56 s · One-row edit | 1.19× | RTX 5090 |
| [3:34](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=214.95) | Ask for headphone recommendations · WebArena 630 | pass · 25.26 s | fail · 12.71 s · Cached-submit edit | — | RTX 5090 |
| [3:37](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=217.50) | Fill a refund request form · WebArena 653 | fail · 26.87 s | fail · 4.75 s · Four-row edit | — | RTX 5090 |
| [3:39](https://jtc268.github.io/inkling-2-fast-computer-use/browser-benchmark-in-order.mp4#t=219.70) | Prepare a coupon request · WebArena 689 | fail · 17.62 s | Unrun | — | RTX 5090 |

[Timings and recording hashes](../evidence/ordered-film/chapters.json) · [Grade receipts](../evidence/ordered-film/film-receipts.zip) · [MiniWoB++ panel](BROWSERGYM.md)

[Two-tab cart trial, both model grades and network traces](WEBARENA-CART-TRANSFER.md).

[Comparison-page click repair and its full cart-task grade](WEBARENA-CART-CLICK.md).

[Windows order-click correction, both models and exact changed weights](WEBARENA-ORDER-START.md).

[Windows command stopping, scores and exact weights](WEBARENA-ORDER-BOUNDARY.md).

[Pending order repair weights, scores and recordings](WEBARENA-PENDING-REPAIR.md).

[Same-checkpoint comparisons on Mac and RTX 5090](WEBARENA-ORDER-CHECKPOINTS.md).

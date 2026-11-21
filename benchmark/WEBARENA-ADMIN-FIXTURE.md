# Shopping Admin browser setup

The runner opens the official Magento dashboard at `/admin` with the fixture's synthetic admin account. Each arm starts with a fresh container and browser session. The bestseller widget loads asynchronously and can display tied products in a different order. With the recorder attached, the runner compares the complete numbered browser observation. A mismatch triggers a page reload before inference. The task clock begins at the first matching observation, which goes directly to the model.

Two independent fixture resets for the WebArena 62 starting page produced the same observation, SHA-256 `8bdd10458d9d9082f11c1abe2f8f56105f408690db215c35984ff4ecda8f012d`. The first dashboard needed 0 reloads and the second needed 1. This check covered browser setup. It recorded zero model episodes.

The pinned image is `am1n3e/webarena-verified-shopping_admin@sha256:d0531dd27ed98d0c459ff9e88118bf2ed8b660b0ed99c38837db46c065a5be13`.

[Official Shopping Admin environment](https://servicenow.github.io/webarena-verified/v1.2.3/environments/shopping_admin/) · [Mac runner](run_search_mac.py)

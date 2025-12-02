# Mastodon archive HTML generator

## How to

1. Drop the (unzipped) mastodon export (generated from `your_instance.domain/settings/export`) into the root with the folder name `archive`
2. Run locally in your matchine `python3 mastodon-archive.py your_image_host_url_prefix` (e.g. `python3 mastodon-archive.py https://media.ricard.social` do change this URL to match your instance CDN or root domain.)
3. Your output will be generated in `docs/index.html`
4. Commit the changes and optionally host it on GitHub Pages for free.

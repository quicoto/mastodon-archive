# Mastodon archive HTML generator

## How to

1. Drop the (unzipped) mastodon export (generated from `your_instance.domain/settings/export`) into the root with the folder name `archive`
2. Run `python3 mastodon-archive.py your_image_host_url_prefix` (e.g. `python3 mastodon-archive.py https://media.ricard.social` for a chaos.social export)
3. Your output will be generated in `docs/index.html`

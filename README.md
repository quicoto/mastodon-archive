# Mastodon archive HTML generator

## Example

This Python script creates a static HTML version of your Mastodon archive export. 

It looks like this: https://quicoto.github.io/mastodon-archive-anime/

## How to

1. Create your own repository using this template
2. Check out your repository on your machine
3. Drop the (unzipped) mastodon export (generated from `your_instance.domain/settings/export`) into the root with the folder name `archive`
4. Run locally in your matchine `python3 mastodon-archive.py your_image_host_url_prefix` (e.g. `python3 mastodon-archive.py https://media.ricard.social` do change this URL to match your instance CDN or root domain.)
5. Your output will be generated in `docs/index.html`
6. Commit the changes and optionally host it on GitHub Pages for free.


# Mastodon archive HTML generator

## How to

1. Change the `.github/workflows/build.yml` with your own instance
2. Create a token from your Mastodon account and add it to your repo as a secret. Call it `ACCESS_TOKEN`
3. Create a `gh-pages` branch
4. Run the GitHub action
5. Configure GitHub repo to serve GitHub Pages from the `gh-pages` branch
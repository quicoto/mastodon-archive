#!/usr/bin/env python3
# encoding=utf8

import os
import argparse
from mastodon import Mastodon

# parse arguments
parser = argparse.ArgumentParser (description = 'Generate an HTML archive of a mastodon user.')
parser.add_argument ('--instance', required=True, help='url to your instance')
parser.add_argument ('--access-token', required=True, help='token providing access to your account')
parser.add_argument ('--max-urls', type=int, default=50000, help='max number of urls to collect')
args = parser.parse_args()

filename = "./dist/index.html"

# connect to mastodon
mstdn = Mastodon(
		access_token = args.access_token,
		api_base_url = args.instance
		)
user = mstdn.account_verify_credentials();

# collect posts
posts = mstdn.account_statuses (user.id);

counter = 0

content = []

def _item(post):
  return f"""
  <div class="item">
    <div class="item__date"><a href="{post.uri}" target="_blank" rel="noopener noreferrer">{post.created_at}</a></div>
    <div class="item__content">{post.content}</div>
  </div>
  """

# iterate posts
while posts and counter < args.max_urls:
	for post in posts:
		# only consider public posts
		if post.reblog or post.visibility != "public":
			continue

		content.append(_item(post))
		counter += 1

		# break if we saw enough...
		if counter >= args.max_urls:
			break

	# fetch new posts if necessary
	posts = mstdn.fetch_next(posts)

header = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Ricard's archive | ricard.social</title>
  <link rel="stylesheet" href="styles.css">
  <meta name="robots" content="noindex">
</head>
<body>
  <header>
    <h1>Archive for Ricard's posts on ricard.social</h1>
  </header>
	<main>"""

footer = """
	</main>
  <footer>
    <p>
      <a href="https://github.com/quicoto/mastodon-archive">Grab the code on GitHub</a>
    </p>
    <p>
      %VERSION%
    </p>
  </footer>
</body>
</html>"""

content = header + ''.join(content) + footer

os.mkdir('./dist')
with open (filename, 'w') as f:
	f.write (content)
os.system('cp styles.css ./dist')


#!/usr/bin/env python3
# encoding=utf8

import os
import sys
import argparse
from mastodon import Mastodon
import sitemap.generator as generator

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

users = [user.url]

# collect posts
posts = mstdn.account_statuses (user.id);

counter = 0

content = []

# iterate posts
while posts and counter < args.max_urls:
	for post in posts:
		# only consider public posts
		if post.reblog or post.visibility != "public":
			continue

		# add to sitemap
		# push HTMl into the content array
		content.append(post.content)
		counter += 1

		# break if we saw enough...
		if counter >= args.max_urls:
			break

	# fetch new posts if necessary
	if counter < args.max_urls:
		posts = mstdn.fetch_next(posts)

# Create file
os.mkdir('./dist')
	with open (filename, 'w') as f:
		f.write (content)


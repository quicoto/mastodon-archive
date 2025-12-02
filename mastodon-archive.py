import json
from os import path
from datetime import datetime
import sys
import re

imageHost = ''
if len(sys.argv) > 1:
    imageHost = sys.argv[1]

with open("archive/outbox.json", "r") as outbox_file:
    outbox = json.loads(outbox_file.read())

with open("archive/actor.json", "r") as actor_file:
    actor = json.loads(actor_file.read())

# map the outbox down to the actual objects
statuses = [status.get("object") for status in outbox.get("orderedItems")]

articles = []
hashtags = []
# attachment urls may begin with "/media/" or something else we dont want
# start with an offset of 1 to avoid checking root for /media or something else wrong
pathOffset = 1

# Minify the HTML content by removing unnecessary whitespace and line breaks
def minify_html(html):
    html = re.sub(r">\s+<", "><", html)  # Remove whitespace between tags
    html = re.sub(r"\s+", " ", html)    # Collapse multiple spaces into one
    return html

for status in statuses:
    # need to ignore objects that arent status dicts
    if type(status) == type({}):
        if not "https://www.w3.org/ns/activitystreams#Public" in (status.get("to", []) + status.get("cc", [])):
            # Toot is not public, let's not output it.
            continue
        # get the date from the statuses (eg. 2024-01-15T16:52:47Z)
        date = status.get("published")
        # convert the date string to a datetime object
        date_obj = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
        # format the datetime object to a more human-readable format
        date = date_obj.strftime("%B %d, %Y")

        url = status.get("url")

        htmlContent = status.get("content")

        # Find all the anchor tags with the class .hashtag and push them to the hashtags array
        for hashtag in status.get("tag"):
            if hashtag.get("type") == "Hashtag":
                # Check if the hashtag is already in the array
                if hashtag.get("name") not in hashtags:
                  hashtags.append("<a href='{0}'>{1}</a>".format(hashtag.get("href"), hashtag.get("name")))

        attachments = [attachment.get("url") for attachment in status.get("attachment")]

        images = ""
        for imageURL in attachments:
          images += "<a href='{0}{1}'><img loading='lazy' class='item__image' src='{0}{1}'></a>".format(imageHost, imageURL)

        summary = status.get("summary")
        if summary:
            summary = "<h4>{0}</h4>".format(summary)
        else:
            summary = ""

        article = "<article class='item'>\n\
  <div class='item__date'><a href='{3}'>{0}</a></div>\n\
  {4}\n\
  <div class='item__content'>{1}</div>\n\
  <div class='item__media'>{2}</div>\n\
</article>\n".format(date, htmlContent, images, url, summary)

        articles.append(article)

outfile = open("docs/index.html", "w")

# Check if the folder has an "avatar.{jpg,png,wepb}" and copy it to the docs folder
assetExtensions = ["jpg", "png", "webp"]
avatarExt = None
for ext in assetExtensions:
    avatarPath = "archive/avatar." + ext
    if path.exists(avatarPath):
        avatarExt = ext
        with open(avatarPath, "rb") as avatarFile:
            with open("docs/avatar." + ext, "wb") as outAvatarFile:
                outAvatarFile.write(avatarFile.read())
        break

# Build avatar image HTML conditionally
avatarImgHtml = ""
if avatarExt:
  avatarImgHtml = '<div><img class="avatar" src="./avatar.%s" alt="Avatar of %s"></div>' % (avatarExt, actor.get("name"))

header = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>%s Mastodon archive</title>
  <link rel="stylesheet" href="styles.css?ver=3.1.0">
  <meta name="robots" content="noindex">
</head>
<body>
  <header>
    %s
    <div>
      <h1>Archive for <a href="%s">%s</a> posts</h1>
      <h2><a class="no-decoration" href="%s">@%s@%s</a></h2>
      <h3>Number of posts: %s</h3>
    </div>
  </header>
  <main>\n""" % (
    actor.get("name"),
    avatarImgHtml,
    actor.get("url"),
    actor.get("name"),
    actor.get("url"),
    actor.get("preferredUsername"),
    re.search(r"https://([^/]+)/", actor.get("url")).group(1),
    "{:,}".format(len(articles))
)

# Order the hashtags alphabetically
hashtags.sort()

# Create a new list of unique hashtags and the number of times they appear
uniqueHashtags = []
uniqueHashtagsOutput = []
for hashtag in hashtags:
  if hashtag not in uniqueHashtags:
    uniqueHashtags.append(hashtag)
    uniqueHashtagsOutput.append(hashtag + " ({0})".format(hashtags.count(hashtag)))

# Add the hashtags to the header
header += "<details class='hashtags-accordion'><summary>Hashtags ({0})</summary><ul class='hashtags'>".format(len(uniqueHashtags))

for hashtag in uniqueHashtagsOutput:
    header += "<li>"
    header += hashtag
    header += "</li>"
header += "</ul></details>"

header += "<div class='items'>"
header = minify_html(header)
outfile.write(header)

for article in reversed(articles):
    outfile.write(minify_html(article))

footer = """
    </div>
	</main>
  <footer>
    <p>
      <a href="https://github.com/quicoto/mastodon-archive">Grab the code on GitHub</a>
    </p>
  </footer>
</body>
</html>"""
footer = minify_html(footer)
outfile.write(footer)

outfile.close()

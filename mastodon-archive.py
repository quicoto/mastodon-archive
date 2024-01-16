import json
from os import path
from datetime import datetime

with open("archive/outbox.json", "r") as outbox_file:
    outbox = json.loads(outbox_file.read())

with open("archive/actor.json", "r") as actor_file:
    actor = json.loads(actor_file.read())

# map the outbox down to the actual objects
statuses = [status.get("object") for status in outbox.get("orderedItems")]

articles = []
# attachment urls may begin with "/media/" or something else we dont want
# start with an offset of 1 to avoid checking root for /media or something else wrong
pathOffset = 1

for status in statuses:
    # need to ignore objects that arent status dicts
    if type(status) == type({}):
        # get the date from the statuses (eg. 2024-01-15T16:52:47Z)
        date = status.get("published")
        # convert the date string to a datetime object
        date_obj = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
        # format the datetime object to a more human-readable format
        date = date_obj.strftime("%B %d, %Y")

        url = status.get("url")

        htmlContent = status.get("content")

        attachments = [attachment.get("url") for attachment in status.get("attachment")]

        images = ""
        for imageURL in attachments:
          images += "<a href='https://media.ricard.social{0}'><img loading='lazy' class='item__image' src='https://media.ricard.social{0}'></a>".format(imageURL)

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

outfile = open("index.html", "w")

header = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Ricard's archive | ricard.social</title>
  <link rel="stylesheet" href="styles.css?ver=2.0.0">
  <meta name="robots" content="noindex">
</head>
<body>
  <header>
    <h1>Archive for Ricard's posts on <a href="https://ricard.social">ricard.social</a></h1>
    <h2>Number of posts: %s</h2>
  </header>
  <main>\n""" % len(articles)

outfile.write(header)

for article in reversed(articles):
    outfile.write(article)

footer = """
	</main>
  <footer>
    <p>
      <a href="https://github.com/quicoto/mastodon-archive">Grab the code on GitHub</a>
    </p>
  </footer>
</body>
</html>"""

outfile.write(footer)

outfile.close()

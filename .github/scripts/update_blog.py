"""Refresh the "Recent thoughts" list in README.md from the site's RSS feed.

Rewrites whatever sits between the BLOG-POST-LIST markers. Standard
library only, so the workflow needs no installs.

Usage: python3 .github/scripts/update_blog.py [README path]
"""

import email.utils
import html
import pathlib
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET

FEED = "https://cameronwillia.ms/rss.xml"
MAX_POSTS = 3
START, END = "<!-- BLOG-POST-LIST:START -->", "<!-- BLOG-POST-LIST:END -->"


def fetch_posts():
    req = urllib.request.Request(FEED, headers={"User-Agent": "profile-readme-updater"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        root = ET.fromstring(resp.read())
    posts = []
    for item in root.iter("item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        date = email.utils.parsedate_to_datetime(item.findtext("pubDate"))
        # Feed summaries can carry HTML; keep plain text on one line.
        summary = re.sub(r"<[^>]+>", "", item.findtext("description") or "")
        summary = " ".join(html.unescape(summary).split())
        if title and link:
            posts.append((date, title, link, summary))
    posts.sort(key=lambda p: p[0], reverse=True)
    return posts[:MAX_POSTS]


def render(posts):
    # Escape characters that would break the Markdown link text.
    def esc(s):
        return re.sub(r"([\[\]\\])", r"\\\1", s)

    lines = []
    for date, title, link, summary in posts:
        line = f"- [{esc(title)}]({link}) · {date:%b} {date.day}, {date.year}"
        if summary:
            # <sub> renders the summary smaller and quieter under the title.
            line += f"<br><sub>{html.escape(summary, quote=False)}</sub>"
        lines.append(line)
    return "\n".join(lines)


def main():
    readme = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "README.md")
    text = readme.read_text()
    if START not in text or END not in text:
        sys.exit(f"markers not found in {readme}")

    posts = fetch_posts()
    if not posts:
        # Leave the README alone rather than blank the section on a bad fetch.
        sys.exit("feed returned no posts; README left unchanged")

    before, rest = text.split(START, 1)
    _, after = rest.split(END, 1)
    new = f"{before}{START}\n{render(posts)}\n{END}{after}"
    if new != text:
        readme.write_text(new)
        print(f"updated {readme} with {len(posts)} post(s)")
    else:
        print("no changes")


if __name__ == "__main__":
    main()

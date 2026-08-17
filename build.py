"""
Static site generator for the terminal-style blog.

Reads markdown files from content/posts/, renders them through
templates/base.html, and writes a static site to dist/.

Usage:
    python build.py
"""

import re
import shutil
from pathlib import Path
from string import Template

import markdown as md

ROOT = Path(__file__).parent
CONTENT = ROOT / "content"
POSTS_DIR = CONTENT / "posts"
TEMPLATES = ROOT / "templates"
STATIC = ROOT / "static"
DIST = ROOT / "dist"

SITE = {
    "name": "Lee",
    "role": "platform engineer",
    "bio": (
        "I write short, practical notes on distributed systems, CI/CD, "
        "and the small decisions that make software easier to run at 3am. "
        "No newsletter, no tracking — just git log for my thinking."
    ),
    "email": "hello@smileycorp.biz",
    "github": "https://github.com/ljburnell",
}

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL)


def parse_frontmatter(text: str):
    m = FRONTMATTER_RE.match(text)
    if not m:
        raise ValueError("Post is missing --- frontmatter ---")
    raw_fm, body = m.groups()
    meta = {}
    for line in raw_fm.strip().splitlines():
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        meta[key.strip()] = val.strip()
    return meta, body.strip()


def load_posts():
    posts = []
    for path in sorted(POSTS_DIR.glob("*.md")):
        meta, body = parse_frontmatter(path.read_text(encoding="utf-8"))
        html_body = md.markdown(body, extensions=["fenced_code", "tables"])
        posts.append(
            {
                "slug": path.stem,
                "title": meta.get("title", path.stem),
                "date": meta.get("date", ""),
                "tags": meta.get("tags", ""),
                "excerpt": meta.get("excerpt", ""),
                "read_time": meta.get("read_time", ""),
                "body_html": html_body,
            }
        )
    posts.sort(key=lambda p: p["date"], reverse=True)
    return posts


def render_base(**ctx) -> str:
    tpl = Template((TEMPLATES / "base.html").read_text(encoding="utf-8"))
    return tpl.safe_substitute(**ctx)


def build_index(posts):
    rows = []
    for p in posts:
        rows.append(
            f'<li><a class="post-row" href="/posts/{p["slug"]}/">'
            f'<span class="date">{p["date"]}</span>'
            f'<span class="title">{p["title"]}</span>'
            f'<span class="tag">{p["tags"]}</span>'
            f"</a></li>"
        )
    posts_html = "\n        ".join(rows)

    body = f'''<section id="whoami">
      <div class="cmd-line"><span class="prompt">$</span><span class="cmd">whoami</span></div>
      <div class="output">
        <p><strong>{SITE["name"]}</strong> — <span class="role">{SITE["role"]}</span></p>
        <p>{SITE["bio"]}</p>
      </div>
    </section>

    <section id="posts">
      <div class="cmd-line"><span class="prompt">$</span><span class="cmd">ls posts/ --recent</span></div>
      <ul class="post-list">
        {posts_html}
      </ul>
    </section>

    <section id="contact">
      <div class="cmd-line"><span class="prompt">$</span><span class="cmd">cat contact.txt</span></div>
      <div class="output">
        <span class="field"><span class="key">mail</span>&nbsp; {SITE["email"]}</span>
        <span class="field"><span class="key">code</span>&nbsp; <a href="{SITE["github"]}">{SITE["github"].replace("https://", "")}</a></span>
        <span class="field"><span class="key">rss</span>&nbsp;&nbsp; <a href="/feed.xml">/feed.xml</a></span>
      </div>
    </section>'''

    html = render_base(
        page_title="~/blog",
        breadcrumb="visitor@lee:~/blog$",
        status_mid="posts.md",
        body=body,
    )
    DIST.mkdir(parents=True, exist_ok=True)
    (DIST / "index.html").write_text(html, encoding="utf-8")


def build_post(post):
    meta_bits = [post["date"], post["tags"]]
    if post["read_time"]:
        meta_bits.append(post["read_time"])
    meta_line = " · ".join(b for b in meta_bits if b)

    body = f"""<div class="cmd-line"><span class="prompt">$</span><span class="cmd">cat posts/{post["slug"]}.md</span></div>
    <div class="output post-body-full">
      <div class="meta">{meta_line}</div>
      {post["body_html"]}
    </div>
    <div class="cmd-line"><span class="prompt">$</span><a class="cmd backlink" href="/">cd ..</a></div>"""

    html = render_base(
        page_title=f"{post['title']} — blog",
        breadcrumb=f"visitor@alam:~/blog/posts/{post['slug']}$",
        status_mid=f"{post['slug']}.md",
        body=body,
    )
    out_dir = DIST / "posts" / post["slug"]
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "index.html").write_text(html, encoding="utf-8")


def main():
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)

    shutil.copy(STATIC / "style.css", DIST / "style.css")
    shutil.copy(STATIC / "boot.js", DIST / "boot.js")

    posts = load_posts()
    build_index(posts)
    for post in posts:
        build_post(post)

    print(f"Built {len(posts)} post(s) → dist/")


if __name__ == "__main__":
    main()

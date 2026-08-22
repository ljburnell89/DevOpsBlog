"""
Tests for build.py — run with: pytest
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest

from build import POSTS_DIR, load_posts, parse_frontmatter


def test_parse_frontmatter_extracts_metadata():
    text = (
        "---\n"
        "title: Test Post\n"
        "date: 2026-01-01\n"
        "tags: testing\n"
        "---\n"
        "This is the body.\n"
    )
    meta, body = parse_frontmatter(text)

    assert meta["title"] == "Test Post"
    assert meta["date"] == "2026-01-01"
    assert meta["tags"] == "testing"
    assert body == "This is the body."


def test_parse_frontmatter_raises_without_frontmatter():
    with pytest.raises(ValueError):
        parse_frontmatter("Just a body, no frontmatter here.")


def test_parse_frontmatter_ignores_lines_without_colon():
    text = "---\ntitle: OK\nthis line has no colon\n---\nbody\n"
    meta, _ = parse_frontmatter(text)
    assert meta == {"title": "OK"}


def test_load_posts_returns_all_markdown_files():
    posts = load_posts()
    md_files = list(POSTS_DIR.glob("*.md"))
    assert len(posts) == len(md_files)
    assert len(posts) > 0


def test_load_posts_have_required_fields():
    posts = load_posts()
    for post in posts:
        assert post["slug"]
        assert post["title"]
        assert post["date"]
        assert post["body_html"]


def test_load_posts_sorted_newest_first():
    posts = load_posts()
    dates = [p["date"] for p in posts]
    assert dates == sorted(dates, reverse=True)


def test_markdown_body_renders_to_html():
    posts = load_posts()
    assert any("<p>" in p["body_html"] for p in posts)

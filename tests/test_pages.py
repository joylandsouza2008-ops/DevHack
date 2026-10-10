"""The app is split into pages (frontend/router.js): Pond, Alerts, Weather,
Diseases, Ask, More. These tests read index.html, app.js and styles.css to
check that every feature is still on a page, that the tab bar and the status
strip are there, and that every label has English and Kannada text."""

import re
from pathlib import Path

import pytest

FRONTEND = Path(__file__).resolve().parent.parent / "frontend"
HTML = (FRONTEND / "index.html").read_text(encoding="utf-8")
APP = (FRONTEND / "app.js").read_text(encoding="utf-8")
CSS = (FRONTEND / "styles.css").read_text(encoding="utf-8")
PAGES = ["pond", "alerts", "weather", "diseases", "ask", "more"]


def page_html(name: str) -> str:
    """The HTML of one page, from its <section> to the next page (or </main>)."""
    start = HTML.index(f'id="page-{name}"')
    following = [HTML.find(f'id="page-{p}"', start + 1) for p in PAGES] + [HTML.index("</main>")]
    return HTML[start:min(i for i in following if i > start)]


def test_six_pages_and_only_pond_shows_before_the_router_runs():
    for name in PAGES:
        tag = re.search(rf'<section class="page" id="page-{name}"[^>]*>', HTML).group(0)
        assert ("hidden" in tag) == (name != "pond"), tag
        assert re.search(rf'id="page-{name}-title" tabindex="-1"', HTML), "router focuses the page title"


def test_tab_bar_has_an_icon_and_a_word_for_every_page():
    nav = re.search(r'<nav class="tab-bar".*?</nav>', HTML, re.S).group(0)
    tabs = re.findall(r'<a href="#/(\w+)" class="tab" data-tab="(\w+)">(.*?)</a>', nav, re.S)
    assert [t[0] for t in tabs] == PAGES and [t[1] for t in tabs] == PAGES
    for _, name, inner in tabs:
        assert '<svg aria-hidden="true"' in inner                     # icon
        assert f'data-i18n="tab{name.capitalize()}"' in inner          # and a word, never icon only


def test_old_bottom_toolbar_is_gone():
    assert "bottom-toolbar" not in HTML and "bottom-toolbar" not in CSS


@pytest.mark.parametrize("page, ids", [
    ("pond", ["simulated-banner", "pond-options", "scenario", "restart", "pause", "scene", "status",
              "health-ring", "gauge", "pond-view", "countdown", "do-chart", "readings"]),
    ("alerts", ["voice-button", "actions-card", "alert-bubble", "channel-picker", "history-list"]),
    ("weather", ["weather-tonight", "weather-message", "weather-offline"]),
    ("diseases", ["likely-card", "guide", "checker-form", "disease-library"]),
    ("ask", ["assistant", "chat-form", "suggestion-list"]),
    ("more", ["kit-form", "live-card"]),
])
def test_every_feature_is_on_its_page(page, ids):
    html = page_html(page)
    for element in ids:
        assert f'id="{element}"' in html, f"{element} should be on the {page} page"


def test_more_page_has_language_theme_and_the_two_panels():
    html = page_html("more")
    assert 'data-lang="kn"' in html and 'data-lang="en"' in html
    assert 'data-theme-choice="light"' in html and 'data-theme-choice="dark"' in html
    assert 'data-open-dialog="sources-dialog"' in html and 'data-open-dialog="terms-dialog"' in html


def test_status_strip_is_outside_the_pages_and_goes_to_pond():
    strip = re.search(r'<a href="#/pond" class="status-strip[^"]*" id="status-strip">.*?</a>', HTML, re.S)
    assert strip, "the strip links to the Pond page"
    assert HTML.index('id="status-strip"') < HTML.index("<main>"), "on every page, not inside one"
    assert 'data-i18n="simulatedTag"' in strip.group(0), "the strip shows simulated values, so it says so"


def test_pages_with_simulated_values_say_simulated():
    for page in ("pond", "alerts", "diseases"):
        html = page_html(page)
        assert 'data-i18n="simulatedTag"' in html or 'id="simulated-label"' in html, page


def test_danger_strip_stops_moving_with_reduce_motion():
    blocks = re.findall(r"@media \(prefers-reduced-motion: reduce\) \{(.*?)\n\}", CSS, re.S)
    assert any(".strip-danger { animation: none;" in b for b in blocks)


def test_every_label_has_english_and_kannada_text():
    keys = set(re.findall(r'data-i18n="(\w+)"', HTML))
    for key in keys:
        assert len(re.findall(rf"\b{key}:", APP)) >= 2, f"{key} needs an English and a Kannada text in app.js"

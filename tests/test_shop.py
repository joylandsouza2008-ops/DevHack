"""The Shop page (#/shop, frontend/shop.js): estimated prices, a cart kept only
in the browser, and a Checkout that only says "Coming soon".

These tests check that the page is wired into the app, that the honesty
wording is there, and that the shop collects no personal data: no form fields,
no calls to the server, and no new backend endpoint that could receive orders,
names, phone numbers or addresses.

Run from the project folder with:   python -m pytest tests/test_shop.py -v
"""

import json
import re
from pathlib import Path

from fastapi.testclient import TestClient

import backend.main as main

client = TestClient(main.app)
FRONTEND = Path(__file__).resolve().parent.parent / "frontend"
HTML = (FRONTEND / "index.html").read_text(encoding="utf-8")
APP = (FRONTEND / "app.js").read_text(encoding="utf-8")
ROUTER = (FRONTEND / "router.js").read_text(encoding="utf-8")
SHOP = (FRONTEND / "shop.js").read_text(encoding="utf-8")
SHOP_DATA = (FRONTEND / "shop-data.json").read_text(encoding="utf-8")
PRODUCTS = json.loads(SHOP_DATA)["products"]
CSS = (FRONTEND / "styles.css").read_text(encoding="utf-8")
SHOP_CODE = re.sub(r"//[^\n]*", "", SHOP)          # shop.js without its comments

# Every API endpoint the app has. A new one (an order or checkout endpoint, say)
# makes this test fail on purpose, so someone has to look at what it receives.
KNOWN_API = {
    ("GET", "/api/health"), ("POST", "/api/risk"), ("POST", "/api/manual"),
    ("GET", "/api/diseases"), ("POST", "/api/diseases/check"),
    ("POST", "/api/assistant/suggestions"), ("POST", "/api/assistant/ask"),
    ("POST", "/api/time-to-danger"), ("GET", "/api/weather/tonight"),
    ("POST", "/api/sensor/{pond_id}"), ("GET", "/api/sensor/{pond_id}"), ("GET", "/api/sensor/{pond_id}/stream"),
    ("GET", "/api/simulator/scenarios"), ("GET", "/api/simulator/stream"),
}
PERSONAL_FIELDS = {"name", "full_name", "phone", "mobile", "email", "address", "pincode", "pin_code",
                   "upi", "card", "card_number", "payment", "aadhaar", "customer"}


def shop_page() -> str:
    start = HTML.index('id="page-shop"')
    return HTML[start:HTML.index("</main>", start)]


def dialog(dialog_id: str) -> str:
    return re.search(rf'<dialog[^>]*id="{dialog_id}".*?</dialog>', HTML, re.S).group(0)


# ---------------------------------------------------------------- route and nav

def test_shop_is_a_page_with_a_focusable_title():
    assert '"ask", "shop", "more"' in ROUTER
    assert re.search(r'<section class="page" id="page-shop"[^>]*hidden>', HTML)
    assert 'id="page-shop-title" tabindex="-1"' in HTML


def test_shop_has_its_own_tab_between_ask_and_more():
    nav = re.search(r'<nav class="tab-bar".*?</nav>', HTML, re.S).group(0)
    assert re.findall(r'data-tab="(\w+)"', nav) == ["pond", "alerts", "weather", "diseases", "ask", "shop", "more"]
    tab = re.search(r'<a href="#/shop" class="tab" data-tab="shop".*?</a>', nav, re.S).group(0)
    assert '<svg aria-hidden="true"' in tab and 'data-i18n="tabShop"' in tab     # icon and a word
    assert 'tabShop: "Shop"' in APP and 'tabShop: "ಅಂಗಡಿ"' in APP


def test_shop_tab_badge_is_hidden_at_zero():
    badge = re.search(r'<span class="tab-badge" id="tab-cart-count"[^>]*>', HTML).group(0)
    assert "hidden" in badge and 'aria-hidden="true"' in badge      # the count is said in the tab's aria-label
    assert "tabBadge.hidden = n === 0" in SHOP


def test_more_page_has_no_shop_card():
    more = HTML[HTML.index('id="page-more"'):HTML.index("<!-- ===================== Shop")]
    assert "shop" not in more.lower()
    assert "moreShop" not in APP


def test_seven_tabs_keep_a_word_on_small_phones():
    # Under 480 px the two long English words get short forms; never an icon alone.
    assert 'tabWeatherShort: "Sky"' in APP and 'tabDiseasesShort: "Fish"' in APP
    assert "grid-template-columns: repeat(7, minmax(0, 1fr))" in CSS
    assert ".tab-long { display: none; } .tab-short { display: inline; }" in CSS


def test_status_strip_stays_outside_every_page():
    # The strip sits above <main>, so the Shop page shows it too.
    assert HTML.index('id="status-strip"') < HTML.index("<main>") < HTML.index('id="page-shop"')


def test_shop_page_is_served():
    r = client.get("/")
    assert r.status_code == 200 and 'id="page-shop"' in r.text
    r = client.get("/shop.js")
    assert r.status_code == 200 and "javascript" in r.headers["content-type"]
    r = client.get("/shop-data.json")
    assert r.status_code == 200 and "json" in r.headers["content-type"]
    assert [p["id"] for p in r.json()["products"]] == [p["id"] for p in PRODUCTS]


def test_shop_script_loads_before_the_app():
    assert HTML.index('src="/shop.js"') < HTML.index('src="/app.js"')
    assert 'src="/shop-data.js"' not in HTML, "the products live in one file: shop-data.json"


def test_cart_button_has_a_word_and_a_count():
    page = shop_page()
    button = re.search(r'<button[^>]*id="cart-open".*?</button>', page, re.S).group(0)
    assert 'data-i18n="cartTitle"' in button and 'id="cart-count"' in button


# ---------------------------------------------------------------- honesty wording

def test_honesty_notes_are_on_the_page():
    page = shop_page()
    for key in ("shopNotForSale", "shopOnePond", "shopPriceNote"):
        assert f'data-i18n="{key}"' in page, key
    assert "A sensor watches one pond. For several ponds, each needs its own sensor. " \
           "Start with the free app and the test kit." in APP
    assert "Estimated component cost. Prices may change." in APP


def test_checkout_says_coming_soon_and_takes_nothing():
    panel = dialog("checkout-dialog")
    assert 'data-i18n="checkoutSoon"' in panel and 'id="copy-list"' in panel
    assert "Coming soon. Orders open after our pilot with farmers. " \
           "No payment is taken and no details are collected." in APP


def test_not_for_sale_wording_agrees_everywhere():
    # The More card, the Shop page and Checkout all say the same thing.
    assert "Not for sale yet." in APP and "Orders open after our pilot with farmers." in APP
    assert APP.count("Orders open after our pilot with farmers.") == 2      # shopNotForSale + checkoutSoon


def test_every_price_is_shown_as_an_estimate():
    assert "estWord: \"est.\"" in APP and "estWord: \"ಅಂದಾಜು\"" in APP
    # Prices are only ever written through formatPrice, which adds "est.".
    assert "₹" not in json.dumps(PRODUCTS, ensure_ascii=False), "products hold numbers, never price text"
    uses = re.findall(r"₹", SHOP_CODE)
    assert len(uses) == 1, "the only ₹ in shop.js is inside formatPrice"


def test_no_cheaper_than_claims():
    text = (APP + SHOP + SHOP_DATA + HTML).lower()
    for claim in ("cheaper", "cheapest", "lowest price", "best price", "best value"):
        assert claim not in text, claim


# ---------------------------------------------------------------- no personal data

def test_shop_has_no_form_and_no_inputs():
    html = shop_page() + dialog("cart-drawer") + dialog("checkout-dialog")
    for tag in ("<form", "<input", "<textarea", "<select"):
        assert tag not in html, tag


def test_shop_never_sends_anything_to_the_server():
    # The one download is the product list, a plain file. Nothing is ever sent.
    assert re.findall(r"fetch\(([^)]*)\)", SHOP_CODE) == ['"/shop-data.json"']
    for banned in ("XMLHttpRequest", "sendBeacon", "WebSocket", "EventSource", "/api/", "method:", "body:"):
        assert banned not in SHOP_CODE, banned


def test_cart_is_stored_only_in_this_browser_under_aquanexus_cart():
    assert 'STORAGE_KEY = "aquanexus_cart"' in SHOP
    assert SHOP_CODE.count("localStorage") == 1, "one guarded place gets localStorage"


def test_no_new_api_endpoints():
    routes = {(m, r.path) for r in main.app.routes if r.path.startswith("/api/")
              for m in (getattr(r, "methods", None) or set()) if m != "HEAD"}
    assert routes == KNOWN_API
    for _, path in routes:
        assert not re.search(r"order|checkout|cart|pay|shop|customer", path), path


def test_no_endpoint_accepts_personal_details():
    schemas = main.app.openapi().get("components", {}).get("schemas", {})
    fields = {f.lower() for schema in schemas.values() for f in schema.get("properties", {})}
    assert not fields & PERSONAL_FIELDS, fields & PERSONAL_FIELDS


def test_order_like_requests_are_refused():
    for path in ("/api/order", "/api/checkout", "/api/cart"):
        r = client.post(path, json={"name": "x", "phone": "9999999999", "address": "y"})
        assert r.status_code in (404, 405), path

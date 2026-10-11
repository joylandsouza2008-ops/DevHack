"""The Shop page (#/shop, frontend/shop.js): estimated prices, a cart kept only
in the browser, and a Checkout that only says "Coming soon".

These tests check that the page is wired into the app, that the honesty
wording is there, and that the shop collects no personal data: no form fields,
no calls to the server, and no new backend endpoint that could receive orders,
names, phone numbers or addresses.

Run from the project folder with:   python -m pytest tests/test_shop.py -v
"""

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
SHOP_DATA = (FRONTEND / "shop-data.js").read_text(encoding="utf-8")
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
    assert '"shop"' in ROUTER and "TAB_OF = { shop: \"more\" }" in ROUTER
    assert re.search(r'<section class="page" id="page-shop"[^>]*hidden>', HTML)
    assert 'id="page-shop-title" tabindex="-1"' in HTML


def test_more_page_links_to_the_shop():
    more = HTML[HTML.index('id="page-more"'):HTML.index('id="page-shop"')]
    assert 'href="#/shop"' in more


def test_status_strip_stays_outside_every_page():
    # The strip sits above <main>, so the Shop page shows it too.
    assert HTML.index('id="status-strip"') < HTML.index("<main>") < HTML.index('id="page-shop"')


def test_shop_page_is_served():
    r = client.get("/")
    assert r.status_code == 200 and 'id="page-shop"' in r.text
    for name in ("shop.js", "shop-data.js"):
        r = client.get(f"/{name}")
        assert r.status_code == 200, name
        assert "javascript" in r.headers["content-type"], name


def test_shop_scripts_load_before_the_app():
    order = [HTML.index(f'src="/{s}"') for s in ("shop-data.js", "shop.js", "app.js")]
    assert order == sorted(order)


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
    assert "₹" not in SHOP_DATA.split("const PRODUCTS")[1]
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


def test_shop_never_talks_to_the_server():
    for banned in ("fetch(", "XMLHttpRequest", "sendBeacon", "WebSocket", "EventSource", "/api/"):
        assert banned not in SHOP_CODE and banned not in SHOP_DATA, banned


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

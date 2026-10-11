"""
Tests for the list of places a pond can be in (backend/places.py, GET /api/places).

Run from the project folder with:   python -m pytest tests/test_places.py -v
"""

import re

from fastapi.testclient import TestClient

import backend.main as main
from backend import places, weather

KANNADA = re.compile("[ಀ-೿]")
client = TestClient(main.app)


def test_the_three_coastal_districts():
    assert [d["name"]["en"] for d in places.DISTRICTS] == ["Udupi", "Dakshina Kannada", "Uttara Kannada"]
    assert [d["name"]["kn"] for d in places.DISTRICTS] == ["ಉಡುಪಿ", "ದಕ್ಷಿಣ ಕನ್ನಡ", "ಉತ್ತರ ಕನ್ನಡ"]


def test_every_place_has_kannada_a_unique_name_and_coastal_karnataka_coordinates():
    names = []
    for district in places.DISTRICTS:
        for taluk in district["taluks"]:
            assert KANNADA.search(taluk["name"]["kn"]), taluk["name"]["en"]
            assert taluk["places"], taluk["name"]["en"]
            for en, kn, latitude, longitude in taluk["places"]:
                names.append(en)
                assert KANNADA.search(kn), en
                assert 12.4 <= latitude <= 15.1 and 74.0 <= longitude <= 75.6, en
    assert len(names) == len(set(names)) == len(places.BY_NAME)       # the name alone finds the place


def test_place_lookup():
    kota = places.place("Kota")
    assert kota["taluk"]["en"] == "Brahmavar" and kota["district"]["en"] == "Udupi"
    assert places.place("  Kota ")["village"] == "Kota"
    assert places.place("Paris") is None and places.place(None) is None and places.place("") is None


def test_mangaluru_in_the_list_is_the_demo_ponds_weather_point():
    m = places.place("Mangaluru")
    assert (m["latitude"], m["longitude"]) == (weather.MANGALURU["latitude"], weather.MANGALURU["longitude"])
    assert m["name"] == weather.MANGALURU["name"]


def test_api_lists_the_places_without_coordinates():
    body = client.get("/api/places").json()
    assert [d["name"]["en"] for d in body["districts"]] == ["Udupi", "Dakshina Kannada", "Uttara Kannada"]
    udupi = body["districts"][0]
    assert {"village": "Kota", "name": {"en": "Kota", "kn": "ಕೋಟ"}} in udupi["taluks"][2]["places"]
    assert "latitude" not in str(body)

"""
Tests for the fish disease guide (backend/diseases.py and its API).

Run from the project folder with:   python -m pytest tests/test_diseases.py -v
"""

import re
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from backend import diseases as D
from backend.main import app

client = TestClient(app)
DOC = (Path(__file__).resolve().parent.parent / "docs" / "diseases.md").read_text(encoding="utf-8")
KANNADA = re.compile("[ಀ-೿]")


def all_text(obj):
    """Every string inside the guide's data."""
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from all_text(v)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            yield from all_text(v)


def bilingual(obj):
    """Every {"en": ..., "kn": ...} pair inside the guide's data."""
    if isinstance(obj, dict):
        if "en" in obj and "kn" in obj:
            yield obj
        else:
            for v in obj.values():
                yield from bilingual(v)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            yield from bilingual(v)


# ----------------------------------------------------------------- the library

def test_the_nine_requested_diseases_are_in_the_library():
    assert set(D.DISEASES) == {"eus", "aeromoniasis", "gill_disease", "columnaris", "saprolegniasis",
                               "argulosis", "flukes", "white_spot", "anchor_worm"}


@pytest.mark.parametrize("disease_id", list(D.DISEASES))
def test_every_entry_is_complete_and_cited(disease_id):
    d = D.DISEASES[disease_id]
    for field in ("name", "body", "behaviour", "when"):
        assert d[field]["en"] and KANNADA.search(d[field]["kn"]), field
    assert d["cause"] in D.CAUSE_TYPES
    assert d["prevention"], "needs at least one prevention step"
    assert d["key_signs"], "needs a key sign for the checker"
    assert all(s in D.SIGNS for s in d["key_signs"] + d["other_signs"])
    assert d["sources"] and all(s in D.SOURCES for s in d["sources"])
    # Cited in docs/diseases.md: a section for the disease, naming each of its sources.
    section = DOC.split(f'<a id="{disease_id}"></a>')[1].split("<a id=")[0]
    for source in d["sources"]:
        assert f"[{source}]" in section, f"{disease_id}: {source} not cited in docs/diseases.md"


def test_every_source_has_a_full_reference_with_a_link_in_the_docs():
    for key in D.SOURCES:
        line = next((l for l in DOC.splitlines() if l.startswith(f"| [{key}]")), None)
        assert line, f"{key} missing from the reference table"
        assert "http" in line, f"{key} has no link"


def test_every_english_text_has_kannada():
    for pair in bilingual([D.DISEASES, D.SIGNS, D.CAUSE_TYPES, D.COMMON_STEPS, D.READING_LINKS,
                           D.TREATMENT_NOTE, D.NOT_A_DIAGNOSIS, D.NO_MATCH, D.GASPING_NOTE, D.LIKELY_NOTE]):
        assert pair["en"] and KANNADA.search(pair["kn"]), pair["en"]


def test_all_disease_kannada_is_in_the_review_sheet():
    sheet = (Path(__file__).resolve().parent.parent / "docs" / "kannada-review.md").read_text(encoding="utf-8")
    missing = [p["kn"] for p in bilingual([D.DISEASES, D.SIGNS, D.CAUSE_TYPES, D.COMMON_STEPS, D.READING_LINKS,
                                           D.TREATMENT_NOTE, D.NOT_A_DIAGNOSIS, D.NO_MATCH, D.GASPING_NOTE,
                                           D.LIKELY_NOTE]) if p["kn"].replace("|", "\\|") not in sheet]
    assert not missing, "re-run python tools/kannada_review.py"


BANNED = ["ppm", "kg/ha", "mg/kg", "g/kg", "dose", "dosage", "formalin", "malachite", "permanganate",
          "salt bath", "dipterex", "dylox", "malathion", "copper sulphate", "bleaching powder",
          "antibiotic", "oxytetracycline", "terramycin", "ivermectin", "emamectin"]


def test_no_chemical_treatments_medicines_or_doses():
    text = " ".join(all_text(D.library())).lower()
    for word in BANNED:
        assert word not in text, word


def test_treatment_note_sends_farmers_to_a_fisheries_officer_or_kvk():
    assert "fisheries officer or KVK" in D.TREATMENT_NOTE["en"]
    assert "KVK" in D.COMMON_STEPS[-1]["en"]


# ----------------------------------------------------------------- symptom checker

def test_white_spots_point_to_white_spot_disease():
    result = D.check(["white_spots", "rubbing"])
    assert result["matches"][0]["id"] == "white_spot"
    assert result["matches"][0]["matched_signs"] == ["white_spots", "rubbing"]


def test_swollen_belly_and_raised_scales_point_to_aeromonas():
    assert D.check(["swollen_belly", "raised_scales"])["matches"][0]["id"] == "aeromoniasis"


def test_lice_and_anchor_worm_are_told_apart():
    assert D.check(["lice"])["matches"][0]["id"] == "argulosis"
    assert D.check(["threads", "red_patches"])["matches"][0]["id"] == "anchor_worm"


def test_result_is_never_a_diagnosis_and_always_says_confirm_with_officer():
    for signs in (["white_spots"], ["red_sores", "fin_rot", "cotton", "much_mucus"], [], ["nonsense"]):
        result = D.check(signs)
        assert "Confirm with your fisheries officer" in result["message"]["en"]
        assert "fisheries officer" in result["treatment_note"]["en"]
        assert "diagnos" not in " ".join(m["name"]["en"] for m in result["matches"]).lower()
    assert "not a diagnosis" in D.check(["white_spots"])["message"]["en"]


def test_at_most_three_matches_and_unknown_signs_ignored():
    result = D.check(list(D.SIGNS) + ["made_up"])
    assert len(result["matches"]) == D.MAX_MATCHES
    assert result["more"] > 0
    assert "made_up" not in result["signs"]


def test_no_signs_means_no_matches():
    result = D.check([])
    assert result["matches"] == []
    assert result["message"] == D.NO_MATCH


def test_gasping_says_check_oxygen_first():
    assert D.check(["gasping"])["notes"] == [D.GASPING_NOTE]
    assert D.check(["white_spots"])["notes"] == []


def test_checker_api():
    r = client.post("/api/diseases/check", json={"signs": ["cotton"]})
    assert r.status_code == 200
    assert r.json()["matches"][0]["id"] == "saprolegniasis"
    assert client.post("/api/diseases/check", json={"signs": "cotton"}).status_code == 422


def test_guide_api_serves_the_library():
    body = client.get("/api/diseases").json()
    assert len(body["diseases"]) == 9
    assert body["signs"]["white_spots"]["group"] == "body"


# ----------------------------------------------------------------- link to readings

def likely(reading: dict) -> set[str]:
    return {d["id"] for d in client.post("/api/risk", json=reading).json()["likely_diseases"]}


def test_safe_reading_makes_no_disease_more_likely():
    assert likely({"dissolved_oxygen": 7.0, "ph": 7.4, "temperature": 28}) == set()


def test_low_oxygen_and_high_ammonia_link_to_aeromonas():
    assert likely({"dissolved_oxygen": 2.5, "ph": 7.4, "temperature": 28}) == {"aeromoniasis"}
    assert "aeromoniasis" in likely({"dissolved_oxygen": 7.0, "ph": 8.4, "temperature": 31, "ammonia": 2.0})


def test_cold_water_links_to_eus_and_white_spot_and_warm_water_to_columnaris():
    assert likely({"dissolved_oxygen": 7.0, "ph": 7.4, "temperature": 22}) == {"eus", "white_spot"}
    assert {"columnaris", "gill_disease"} <= likely({"dissolved_oxygen": 7.0, "ph": 7.4, "temperature": 33})


def test_acidic_water_links_to_eus_with_reason_and_sources():
    risk = client.post("/api/risk", json={"dissolved_oxygen": 7.0, "ph": 6.0, "temperature": 28}).json()
    (eus,) = risk["likely_diseases"]
    assert eus["id"] == "eus"
    assert "acidic" in eus["reasons"][0]["en"] and KANNADA.search(eus["reasons"][0]["kn"])
    assert eus["sources"] == ["fao2001"]


def test_every_reading_link_points_to_a_cited_disease():
    for links in D.READING_LINKS.values():
        for disease_id, _, sources in links:
            assert disease_id in D.DISEASES
            assert sources and all(s in D.SOURCES for s in sources)

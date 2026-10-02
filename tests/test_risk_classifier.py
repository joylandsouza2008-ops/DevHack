"""
Tests for the rule-based risk classifier.

Run from the project folder with:   python -m pytest
Each test feeds in sample sensor readings and checks the answer.
"""

import copy

import pytest

from backend.risk_classifier import classify, load_thresholds, unionized_ammonia

# A healthy pond: every reading inside the safe range.
HEALTHY = {
    "dissolved_oxygen": 6.5,   # mg/L
    "ph": 7.4,
    "temperature": 28.0,       # °C
    "ammonia": 0.05,           # mg/L total ammonia -> tiny amount of toxic NH3
    "nitrate": 20.0,           # mg/L NO3 -> 4.5 mg/L NO3-N
    "turbidity": 30.0,
}


def reading(**changes):
    """HEALTHY readings with some values changed."""
    return {**HEALTHY, **changes}


# --- Safe ---------------------------------------------------------------

def test_healthy_pond_is_safe():
    result = classify(HEALTHY)
    assert result.level == "safe"
    assert result.causes == []
    assert result.summary["en"] == "All readings are in the safe range."
    assert result.summary["kn"] == "ಎಲ್ಲಾ ಅಳತೆಗಳು ಸುರಕ್ಷಿತ ಮಟ್ಟದಲ್ಲಿವೆ."


def test_band_edges_count_as_safe():
    # 5.0 mg/L oxygen, pH 8.5 and 32 °C are the edges of the safe ranges.
    result = classify(reading(dissolved_oxygen=5.0, ph=8.5, temperature=32.0))
    assert result.level == "safe"


# --- Warning ------------------------------------------------------------

def test_low_oxygen_is_warning_and_explained():
    result = classify(reading(dissolved_oxygen=4.1))
    assert result.level == "warning"
    assert result.causes == ["dissolved_oxygen"]
    assert "Oxygen is low (4.1 mg/L)" in result.summary["en"]
    assert "ಆಮ್ಲಜನಕ ಕಡಿಮೆ ಇದೆ (4.1 mg/L)" in result.summary["kn"]


def test_high_ph_is_warning():
    # Low ammonia here: at pH 9 about 40% of total ammonia turns toxic, so the
    # HEALTHY sample's 0.05 mg/L would also (correctly) trigger an ammonia Warning.
    result = classify(reading(ph=9.0, ammonia=0.01))
    assert result.level == "warning"
    assert result.causes == ["ph"]
    assert "alkaline" in result.summary["en"]


def test_high_nitrate_is_only_ever_warning():
    # 500 mg/L NO3 = 113 mg/L NO3-N: far above the limit, but nitrate has no Danger level.
    result = classify(reading(nitrate=500.0))
    assert result.level == "warning"
    assert result.causes == ["nitrate"]


# --- Danger -------------------------------------------------------------

def test_very_low_oxygen_is_danger():
    result = classify(reading(dissolved_oxygen=2.5))
    assert result.level == "danger"
    assert result.causes == ["dissolved_oxygen"]
    assert "Fish can die" in result.summary["en"]
    assert "ಮೀನುಗಳು ಸಾಯಬಹುದು" in result.summary["kn"]


def test_35_degrees_is_danger():
    # Warning range is "20 up to but not including 35", so 35 °C is Danger.
    assert classify(reading(temperature=34.9)).level == "warning"
    assert classify(reading(temperature=35.0)).level == "danger"


def test_ammonia_danger_depends_on_ph_and_temperature():
    # Same 1.0 mg/L total ammonia: harmless in acidic water, deadly in alkaline warm water.
    assert classify(reading(ammonia=1.0, ph=6.5, temperature=27.0)).level == "safe"
    hot_alkaline = classify(reading(ammonia=1.0, ph=8.5, temperature=30.0))
    assert hot_alkaline.level == "danger"
    assert "ammonia" in hot_alkaline.causes


def test_overall_risk_is_the_worst_parameter():
    # Oxygen is only Warning, but pH is Danger -> overall Danger, caused by pH alone.
    result = classify(reading(dissolved_oxygen=4.0, ph=5.0))
    assert result.level == "danger"
    assert result.causes == ["ph"]
    levels = {p.parameter: p.level for p in result.parameters}
    assert levels["dissolved_oxygen"] == "warning"
    assert levels["ph"] == "danger"


def test_two_parameters_at_the_same_worst_level_are_both_reported():
    result = classify(reading(dissolved_oxygen=2.0, temperature=36.0))
    assert result.level == "danger"
    assert set(result.causes) == {"dissolved_oxygen", "temperature"}
    assert "Oxygen" in result.summary["en"] and "too hot" in result.summary["en"]


# --- Sensor faults and missing data -------------------------------------

def test_impossible_reading_is_a_sensor_error_not_danger():
    # The dataset contains TEMP = 0 °C rows; that is a broken sensor, not a frozen pond.
    result = classify(reading(temperature=0.0))
    assert result.level == "safe"
    assert [e["parameter"] for e in result.sensor_errors] == ["temperature"]
    assert "Check the sensor" in result.sensor_errors[0]["message"]["en"]


def test_ammonia_skipped_when_ph_missing():
    result = classify({"dissolved_oxygen": 6.0, "ammonia": 1.0, "temperature": 28.0})
    ammonia = next(p for p in result.parameters if p.parameter == "ammonia")
    assert ammonia.level == "unknown"
    assert result.level == "safe"  # judged only on what could be checked


def test_no_valid_readings_is_unknown():
    result = classify({"temperature": 0.0, "dissolved_oxygen": None})
    assert result.level == "unknown"


def test_turbidity_is_information_only():
    result = classify(reading(turbidity=900.0))
    assert result.level == "safe"
    assert [p.parameter for p in result.info] == ["turbidity"]


# --- Config and helpers -------------------------------------------------

def test_changing_the_config_changes_the_result():
    # Proves the numbers come from config/thresholds.toml, not the code.
    strict = copy.deepcopy(load_thresholds())
    strict["dissolved_oxygen"]["safe"]["min"] = 7.0
    assert classify(HEALTHY).level == "safe"
    assert classify(HEALTHY, thresholds=strict).level == "warning"


def test_unionized_ammonia_matches_hand_calculation():
    # pH 8.5, 30 °C: about 20% of total ammonia is toxic NH3.
    assert unionized_ammonia(1.0, 8.5, 30.0) == pytest.approx(0.202, abs=0.002)


def test_result_converts_to_plain_dict_for_the_api():
    data = classify(reading(dissolved_oxygen=2.5)).to_dict()
    assert data["level"] == "danger"
    assert data["level_name"] == {"en": "Danger", "kn": "ಅಪಾಯ"}

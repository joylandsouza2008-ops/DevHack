"""
SMS / WhatsApp alert text, for the PREVIEW on the dashboard.

No real messages are sent. This file only writes the text a farmer would
receive, built from the same messages the app shows (the risk summary and
"time until danger"), so the preview always matches the app.

    compose_alert(risk, time_to_danger, label, pond)
        -> {"send": True/False, "sms": {"en", "kn"}, "whatsapp": {"en", "kn"}}

An alert is only "sent" for Warning and Danger. When the pond is Safe the
preview says that no message would go out.
"""

from __future__ import annotations

POND_NAMES = {
    "station1": {"en": "Pond 1", "kn": "ಕೊಳ 1"},
    "station2": {"en": "Pond 2", "kn": "ಕೊಳ 2"},
    "station3": {"en": "Pond 3", "kn": "ಕೊಳ 3"},
}

APP_NAME = {"en": "AquaNexus", "kn": "AquaNexus"}
ICON = {"warning": "⚠️", "danger": "🚨"}

NO_ALERT = {
    "en": "No alert would be sent: the readings are not in Warning or Danger.",
    "kn": "ಯಾವುದೇ ಎಚ್ಚರಿಕೆ ಕಳುಹಿಸುವುದಿಲ್ಲ: ಅಳತೆಗಳು ಎಚ್ಚರಿಕೆ ಅಥವಾ ಅಪಾಯದ ಮಟ್ಟದಲ್ಲಿಲ್ಲ.",
}


def compose_alert(risk: dict, time_to_danger: dict | None = None,
                  label: dict | None = None, pond: dict | None = None) -> dict:
    """
    risk            the dictionary from RiskResult.to_dict()
    time_to_danger  from estimate_time_to_danger(); added only when danger is expected
    label           data label, e.g. "Simulated data"; always added so it can't be mistaken for a real pond
    pond            pond name {"en", "kn"}, or None for a test-kit reading
    """
    level = risk["level"]
    if level not in ICON:
        return {"send": False, "sms": dict(NO_ALERT), "whatsapp": dict(NO_ALERT)}

    sms, whatsapp = {}, {}
    for lang in ("en", "kn"):
        level_name = risk["level_name"][lang]
        where = f" - {pond[lang]}" if pond else ""
        extra = ""
        if time_to_danger and time_to_danger.get("status") == "danger_expected":
            extra = time_to_danger["message"][lang]
        tag = f"[{label[lang]}]" if label else ""

        sms[lang] = " ".join(part for part in [
            f"{APP_NAME[lang]}: {level_name.upper() if lang == 'en' else level_name}{where}.",
            risk["summary"][lang], extra, tag] if part)

        lines = [f"{ICON[level]} *{APP_NAME[lang]}*", f"*{level_name}*{where}", "", risk["summary"][lang]]
        if extra:
            lines += ["", extra]
        if tag:
            lines += ["", f"_{label[lang]}_"]
        whatsapp[lang] = "\n".join(lines)
    return {"send": True, "sms": sms, "whatsapp": whatsapp}

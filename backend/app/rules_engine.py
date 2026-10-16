"""Rule-based danger-sign triage.

Design principles (safety):
  * Rules live in rules.json so a clinician can review/edit them without code.
  * Any matched HIGH sign -> HIGH. The tier is the max over matched rules.
  * Unknown/unticked signs never lower a tier; "no signs ticked" is LOW only
    in the sense of "no listed danger sign reported", and the result says so.
  * The result always carries rules_reviewed so the UI can show a banner
    while the rule file is unreviewed.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

RULES_PATH = Path(__file__).parent / "rules.json"
TIER_ORDER = {"LOW": 0, "MEDIUM": 1, "HIGH": 2}


@dataclass
class TriageResult:
    tier: str
    matched_rule_ids: list[str] = field(default_factory=list)
    matched_labels: list[str] = field(default_factory=list)
    rules_reviewed: bool = False
    rules_version: str = ""
    note: str = ""


def load_rules(path: Path = RULES_PATH) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def known_signs(rules: dict | None = None) -> list[str]:
    rules = rules or load_rules()
    return [r["sign"] for r in rules["rules"]]


def assess(signs: Iterable[str], rules: dict | None = None) -> TriageResult:
    rules = rules or load_rules()
    reported = set(signs)
    matched = [r for r in rules["rules"] if r["sign"] in reported]

    tier = "LOW"
    for r in matched:
        if TIER_ORDER[r["tier"]] > TIER_ORDER[tier]:
            tier = r["tier"]

    note = ""
    if tier == "LOW":
        note = ("No listed danger sign was reported. This does not rule out a "
                "problem: if the woman feels unwell, refer her anyway.")
    if not rules.get("reviewed", False):
        note = (note + " " if note else "") + (
            "Rules are an unreviewed draft: for prototype/demo use only."
        )

    return TriageResult(
        tier=tier,
        matched_rule_ids=[r["id"] for r in matched],
        matched_labels=[r["label_en"] for r in matched],
        rules_reviewed=bool(rules.get("reviewed", False)),
        rules_version=rules.get("version", ""),
        note=note,
    )

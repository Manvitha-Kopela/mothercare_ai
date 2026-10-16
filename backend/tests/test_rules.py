import pytest

try:
    import rules_engine  # flat layout: files side by side
except ImportError:
    from app import rules_engine  # package layout

RULES = rules_engine.load_rules()
HIGH_SIGNS = [r["sign"] for r in RULES["rules"] if r["tier"] == "HIGH"]
MEDIUM_SIGNS = [r["sign"] for r in RULES["rules"] if r["tier"] == "MEDIUM"]


def test_no_signs_is_low_with_warning_note():
    res = rules_engine.assess([])
    assert res.tier == "LOW"
    assert "does not rule out" in res.note


@pytest.mark.parametrize("sign", HIGH_SIGNS)
def test_each_high_sign_alone_is_high(sign):
    assert rules_engine.assess([sign]).tier == "HIGH"


@pytest.mark.parametrize("sign", MEDIUM_SIGNS)
def test_each_medium_sign_alone_is_medium(sign):
    assert rules_engine.assess([sign]).tier == "MEDIUM"


def test_tier_is_max_of_matched():
    res = rules_engine.assess([MEDIUM_SIGNS[0], HIGH_SIGNS[0]])
    assert res.tier == "HIGH"
    assert len(res.matched_rule_ids) == 2


def test_unknown_sign_never_lowers_or_raises():
    assert rules_engine.assess(["not_a_real_sign"]).tier == "LOW"
    assert rules_engine.assess(["not_a_real_sign", HIGH_SIGNS[0]]).tier == "HIGH"


def test_duplicate_signs_ok():
    assert rules_engine.assess([HIGH_SIGNS[0], HIGH_SIGNS[0]]).tier == "HIGH"


def test_unreviewed_rules_are_flagged():
    res = rules_engine.assess([HIGH_SIGNS[0]])
    assert res.rules_reviewed is False
    assert "unreviewed" in res.note.lower()


def test_every_rule_has_valid_tier_and_unique_id():
    ids = [r["id"] for r in RULES["rules"]]
    assert len(ids) == len(set(ids))
    assert all(r["tier"] in rules_engine.TIER_ORDER for r in RULES["rules"])

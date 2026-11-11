"""Strict, deterministic and explainable college matching."""
import re
from course_catalog import CATEGORIES, COURSE_CATALOG, resolve_course
from geo_data import normalise_city

CAREER_FIELDS = CATEGORIES
COURSE_OPTIONS = {item["name"]: item["aliases"] for item in COURSE_CATALOG}

def clean(value):
    return re.sub(r"[^a-z0-9]+", " ", (value or "").lower()).strip()

LEGACY_ALIASES = {
    "b tech cse": "B.Tech Computer Science Engineering", "btech cse": "B.Tech Computer Science Engineering",
    "b tech computer science": "B.Tech Computer Science Engineering", "btech computer science": "B.Tech Computer Science Engineering",
    "computer science": "Computer Science", "artificial intelligence": "Artificial Intelligence",
    "ai and ml": "B.Tech Artificial Intelligence and Machine Learning", "ai ml": "B.Tech Artificial Intelligence and Machine Learning",
    "mechanical engineering": "Mechanical Engineering", "engineering": "Engineering",
    "mbbs": "MBBS", "medicine": "Medicine", "b des": "B.Des", "bdes": "B.Des", "design": "Design",
    "bba": "BBA", "business administration": "Business Administration", "business": "Business",
    "life sciences": "Life Sciences", "science": "Science", "psychology": "Psychology", "education": "Education",
}
PROGRAM_EQUIVALENTS = {
    "B.Tech Computer Science Engineering": {"B.Tech Computer Science", "Computer Science"},
    "B.Tech Artificial Intelligence and Machine Learning": {"Artificial Intelligence"},
    "B.Tech Artificial Intelligence": {"Artificial Intelligence"},
    "B.Tech Mechanical Engineering": {"Mechanical Engineering"},
    "Bachelor of Medicine and Bachelor of Surgery": {"MBBS", "Medicine"},
    "Bachelor of Design": {"B.Des", "Design"},
    "Bachelor of Business Administration": {"BBA", "Business Administration"},
    "Business Administration": {"BBA"},
    "Bachelor of Science": {"Science"}, "Bachelor of Computer Science": {"Computer Science"},
    "B.Sc Computer Science": {"Computer Science"}, "B.Sc Artificial Intelligence": {"Artificial Intelligence"},
    "B.Sc Data Science": {"Data Science"}, "B.Sc Psychology": {"Psychology"}, "BA Psychology": {"Psychology"},
}

def canonical_course(value):
    row = resolve_course(value)
    return row["name"] if row else LEGACY_ALIASES.get(clean(value), (value or "").strip())

def accepted_programmes(requested):
    canonical = canonical_course(requested)
    return {clean(value) for value in {canonical, *PROGRAM_EQUIVALENTS.get(canonical, set())} if value}

def course_matches(college, requested):
    if not requested:
        return True, ""
    accepted = accepted_programmes(requested)
    for offered in college.get("courses", []):
        if clean(offered) in accepted:
            return True, offered
    return False, ""

def field_matches(college, requested):
    return not requested or clean(requested) in {clean(field) for field in college.get("career_fields", [])}

def _selected(value):
    return clean(value) not in {"", "any", "any state", "any city", "any country", "either"}

def location_tier(college, preference):
    country, state, city = (preference.get(key, "") for key in ("preferred_country", "preferred_state", "preferred_city"))
    same_country = not _selected(country) or clean(college["country"]) == clean(country)
    same_state = not _selected(state) or clean(college["state"]) == clean(state)
    same_city = not _selected(city) or normalise_city(college["city"]) == normalise_city(city)
    if same_country and same_state and same_city:
        return 0, "Exact selected location"
    if same_country and same_state:
        return 1, "Outside selected city (same state/province)"
    if same_country:
        return 2, "Outside selected state/province (same country)"
    return 3, "Outside selected country"

def budget_status(college, preference):
    budget, currency = preference.get("budget_amount"), preference.get("budget_currency")
    amount, fee_currency = college.get("annual_fee_amount"), college.get("fee_currency")
    if not budget:
        return "Budget not supplied", 0
    if amount is None or not fee_currency:
        return "Fees not verified", 0
    if fee_currency != currency:
        return f"Not compared ({fee_currency} vs {currency})", 0
    return ("Confirmed within budget", 15) if amount <= budget else ("Verified fee is above budget", -25)

def matches_study_scope(college, preference):
    scope = preference.get("study_scope", "Both")
    return not ((scope == "India" and college["country"] != "India") or (scope == "Abroad" and college["country"] == "India"))

def recommend(colleges, preference, include_alternatives=False):
    """Return strict exact-location matches; broader locations require opt-in."""
    results, institution_type = [], preference.get("institution_type", "Either")
    strict_budget = preference.get("budget_mode") == "strict"
    for college in colleges:
        if not matches_study_scope(college, preference):
            continue
        country = preference.get("preferred_country", "")
        if _selected(country) and clean(college["country"]) != clean(country):
            continue
        if institution_type not in {"", "Either"} and clean(college["ownership"]) != clean(institution_type):
            continue
        matched, matched_course = course_matches(college, preference.get("preferred_course", ""))
        if not matched or not field_matches(college, preference.get("career_field", "")):
            continue
        tier, tier_label = location_tier(college, preference)
        if (not include_alternatives and tier != 0) or (include_alternatives and tier == 0):
            continue
        status, budget_score = budget_status(college, preference)
        if strict_budget and preference.get("budget_amount") and status != "Confirmed within budget":
            continue
        item, rank = dict(college), college.get("rank_value")
        rank_score = max(0, 21 - min(int(rank), 20)) if rank else 0
        item.update({"matched_course": matched_course or preference.get("preferred_course") or "Multiple programmes",
                     "location_tier": tier, "location_label": tier_label, "budget_status": status,
                     "match_score": 100 + budget_score + rank_score,
                     "match_reasons": [f"verified catalogue programme: {matched_course}" if matched_course else "no course filter selected", tier_label, status] + ([item["ranking_info"]] if item.get("ranking_info") else [])})
        results.append(item)
    return results

def sort_results(results, sort_by="relevance"):
    if sort_by == "ranking":
        return sorted(results, key=lambda c: (c.get("rank_value") is None, c.get("rank_value") or 99999, c["location_tier"], c["name"]))
    if sort_by == "tuition":
        return sorted(results, key=lambda c: (c.get("annual_fee_amount") is None, c.get("annual_fee_amount") or 10**20, c["name"]))
    if sort_by == "location":
        return sorted(results, key=lambda c: (c["location_tier"], c["state"], c["city"], c["name"]))
    return sorted(results, key=lambda c: (-c["match_score"], c["name"]))

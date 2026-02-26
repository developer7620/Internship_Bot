"""
eligibility.py — Strict Internship Eligibility Engine
All regex compiled once at module load. Single entry point: is_valid_internship(job)
"""

import re
import logging

log = logging.getLogger("Eligibility")

# ═══════════════════════════════════════════════════════════════════════
# COMPILED REGEX — loaded once at import
# ═══════════════════════════════════════════════════════════════════════

# ── 1. Experience requirement blockers ─────────────────────────────────
RE_EXPERIENCE = re.compile(r"""
    \b[2-9]\+\s*years?                              # 2+ years, 5+ years
  | \b1[0-9]\+\s*years?                             # 10+ years
  | \b[2-9]\s*[-–]\s*\d+\s*years?                  # 2-4 years, 3–6 years
  | minimum\s+[2-9]\s*years?                        # minimum 2 years
  | at\s+least\s+[2-9]\s*years?                     # at least 3 years
  | \b[2-9]\s*years?\s*(of\s+)?(exp(erience)?|work) # 3 years of experience
  | \b[2-9]\s*years?\s+industry                     # 2 years industry
  | industry\s+experience                            # industry experience
  | proven\s+track\s+record                          # proven track record
  | extensive\s+experience                           # extensive experience
  | strong\s+professional\s+experience               # strong professional exp
  | production\s+experience                          # production experience
  | system\s+design\s+experience                     # system design exp
  | deep\s+(expertise|experience|knowledge)          # deep expertise
  | significant\s+experience                         # significant experience
  | \bseasoned\b                                     # seasoned professional
""", re.VERBOSE | re.IGNORECASE)

# ── 2. Seniority level blockers ────────────────────────────────────────
RE_SENIORITY = re.compile(r"""
    \bsenior\b
  | \bstaff\b
  | \bprincipal\b
  | \blead\s*(software|backend|frontend|full|data|ml|sre|devops|platform|engineer|developer)?\b
  | \bdirector\b
  | \bmanager\b
  | \bvp\b | vice\s+president
  | \bhead\s+of\b
  | \barchitect\b
  | \bsde[\s\-]?[2-9]\b | \bsde[\s\-]?ii+\b        # SDE2, SDE3, SDE-II, SDE-III
  | \bswe[\s\-]?[2-9]\b | \bswe[\s\-]?ii+\b        # SWE2, SWE-II
  | \bl[\s\-]?[4-9]\b                               # L4, L5, L-4
  | \be[\s\-]?[4-9]\b                               # E4, E5
  | \bic[\s\-]?[3-9]\b                              # IC3, IC4
  | \blevel\s+[4-9]\b                               # Level 4
  | \bgrade\s+[4-9]\b                               # Grade 5
  | \bband\s+[5-9]\b                                # Band 6
""", re.VERBOSE | re.IGNORECASE)

# ── 3. Internship positive signals ─────────────────────────────────────
RE_INTERNSHIP = re.compile(r"""
    \bintern(ship)?\b
  | \btrainee\b
  | \bapprentice(ship)?\b
  | \bco[\s\-]?op\b
  | \bpracticum\b
  | summer\s+(intern|program|position|role|opportunity)
  | winter\s+(intern|program|position|role|opportunity)
  | intern\s*(to\s*)?(ppo|full[\s\-]?time\s+conversion|convert)
  | full[\s\-]?time\s+intern\s+conversion
  | \bplaccement\b                                   # placement year
""", re.VERBOSE | re.IGNORECASE)

# ── 4. Hard reject even if "intern" appears ────────────────────────────
RE_HARD_REJECT = re.compile(r"""
    \bnew\s+grad(uate)?\b                            # New Grad = full-time
  | graduate\s+(program|hire|recruitment|role)\b    # Graduate Program
  | campus\s+(hire|recruitment|program)
  | full[\s\-]?time\s+only
  | no\s+freshers?\b
  | no\s+students?\b
  | not\s+(open\s+to\s+)?freshers?
  | experienced\s+(professional|candidate|engineer|developer)
  | (\b0\s*[-–]\s*2\s*years?\b(?!.*intern))         # 0-2 years unless intern
  | no\s+internship                                   # "no internship" negation
  | not\s+(a\s+)?internship                          # "not an internship"
  | this\s+is\s+not\s+(a\s+)?intern                # explicit negation
""", re.VERBOSE | re.IGNORECASE)

# ── 4b. Negation context: intern/ship preceded by no/not/isn't ─────────
RE_INTERN_NEGATION = re.compile(
    r"(no|not|isn't|is not|without|non)[\s\-]+internship",
    re.IGNORECASE
)

# ── 5. Location: explicitly allowed ────────────────────────────────────
RE_LOC_ALLOWED = re.compile(r"""
    \bindia\b
  | \bremote\b
  | work[\s\-]from[\s\-]home | \bwfh\b
  | \banywhere\b | \bworldwide\b | \bglobal(ly)?\b
  | bengaluru | bangalore | \bblr\b
  | mumbai | delhi | \bncr\b | new\s+delhi
  | hyderabad | pune | chennai | noida
  | gurugram | gurgaon | kolkata | ahmedabad | kochi
  | kottayam | trivandrum | thiruvananthapuram
  | indore | jaipur | bhopal | coimbatore | nagpur
""", re.VERBOSE | re.IGNORECASE)

# ── 6. Location: explicitly blocked ────────────────────────────────────
RE_LOC_BLOCKED = re.compile(r"""
    \busa\b | \bus\b\s+only | united\s+states | \bamerica\b
  | \buk\b  | united\s+kingdom | \bbritain\b | \bengland\b
  | \bcanada\b | \baustralia\b | \bsingapore\b
  | \bgermany\b | \bfrance\b | \bnetherlands\b
  | \beurope\b | \bemea\b | \blatam\b | \bapac\b
  | san\s+francisco | \bsf\b\s+bay | new\s+york | \bnyc\b
  | \bseattle\b | \baustin\b | \bboston\b | \bchicago\b
  | \blondon\b | \btoronto\b | \bvancouver\b | \bdubai\b
  | \bhybrid\b                                       # hybrid blocked
  | visa\s+sponsorship | work\s+authoriz
  | authorized\s+to\s+work\s+in\s+the\s+us
  | must\s+be\s+(based|located|residing)\s+in\s+(?!india)
  | onsite\s+(required|only|mandatory)(?!.*india)
""", re.VERBOSE | re.IGNORECASE)

# ── 7. Degree requirement blockers ─────────────────────────────────────
RE_DEGREE_BLOCKED = re.compile(r"""
    \bph\.?d\b | doctorate | doctoral\s+degree
  | masters?\s+(degree\s+)?(required|preferred|must|only)
  | must\s+have\s+(a\s+)?masters?
  | postgraduate | post[\s\-]graduate
  | \bmba\b
  | graduating\s+in\s+2024\b
  | 2024\s+graduates?\s+only
""", re.VERBOSE | re.IGNORECASE)

# ── 8. Non-technical role blockers ─────────────────────────────────────
RE_NON_TECH = re.compile(r"""
    \b(hr|human\s+resources?)\s*(intern|role|position)?\b
  | \bmarketing\s*(intern|role|position)?\b
  | \bsales\s*(intern|role|position|development)?\b
  | \bcontent\s*(writer|intern|marketing|creator)\b
  | \bgrowth\s*(intern|hacker|marketing)\b
  | \bseo\s*(intern|specialist)?\b
  | \bsocial\s+media\b
  | \bui[\s/]ux\b(?!.*engineer)                     # UI/UX but NOT UI/UX engineer
  | \bux\s+(design(er)?|research(er)?)\b
  | \bgraphic\s+design(er)?\b
  | \bproduct\s+design(er)?\b(?!.*engineer)         # Product design NOT product engineer
  | \bcopywriter\b | \bcopywrit(er|ing)\b
  | \bbusiness\s+development\b
  | \bfinance\s+intern\b | \baccounting\s+intern\b
  | \brecruiter\b | \btalent\s+acquisition\b
  | \bcustomer\s+success\b | \baccount\s+manager\b
""", re.VERBOSE | re.IGNORECASE)

# ── 9. Technical role signals ──────────────────────────────────────────
RE_TECH_ROLE = re.compile(r"""
    backend | back[\s\-]end
  | software\s+(engineer|developer|dev)
  | \bsde\b | \bswe\b
  | full[\s\-]?stack | fullstack
  | \bapi\b | \brest(ful)?\b
  | \bnode(\.?js)?\b | \bpython\b | \bjava\b(?!\s*script\s*only)
  | \bgo(lang)?\b | \brust\b | \bc\+\+\b | \bc#\b
  | \bdjango\b | \bflask\b | \bfastapi\b | \bspring\b | \brails\b
  | \bdevops\b | \bcloud\s+(engineer|intern)\b
  | platform\s+engineer | \bsre\b | site\s+reliability
  | data\s+engineer | \bml\s+engineer\b | mlops
  | \binfrastructure\b | systems?\s+engineer
  | \bdatabase\b | \bpostgres\b | \bmongodb\b
  | \bmicroservices?\b | \bdocker\b | \bkubernetes\b | \bk8s\b
""", re.VERBOSE | re.IGNORECASE)


# ═══════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════

def _build_combined(job: dict) -> str:
    """Merge title + location + description + tags into one lowercase string."""
    return " ".join(filter(None, [
        job.get("title", ""),
        job.get("location", ""),
        job.get("description", ""),
        job.get("tags", ""),
    ])).lower()


def _get_title(job: dict) -> str:
    return job.get("title", "").lower()


def _get_location(job: dict) -> str:
    return job.get("location", "").lower().strip()


# ── Individual checks (each returns bool + optional reason) ──────────

def check_technical_role(title: str, combined: str) -> tuple[bool, str]:
    if RE_NON_TECH.search(title):
        return False, "non-technical role in title"
    if not RE_TECH_ROLE.search(title) and not RE_TECH_ROLE.search(combined):
        return False, "no technical engineering signal found"
    return True, ""


def check_internship(title: str, combined: str) -> tuple[bool, str]:
    if RE_HARD_REJECT.search(combined):
        return False, "hard reject signal (new grad / graduate program / no freshers)"
    if RE_INTERN_NEGATION.search(combined):
        return False, "internship negated in description"
    # Check title first (strongest signal)
    if RE_INTERNSHIP.search(title):
        return True, ""
    # Check full combined text
    if RE_INTERNSHIP.search(combined):
        return True, ""
    return False, "no internship signal in title or description"


def check_location(location: str, combined: str) -> tuple[bool, str]:
    # Unknown location → check only for blocked signals in description
    if not location or location in ("check listing", "not mentioned", "n/a"):
        if RE_LOC_BLOCKED.search(combined):
            return False, "blocked location found in description"
        return True, ""

    if RE_LOC_BLOCKED.search(location):
        return False, f"blocked location field: {location}"
    if RE_LOC_BLOCKED.search(combined):
        return False, "blocked location found in description"
    if not RE_LOC_ALLOWED.search(location) and not RE_LOC_ALLOWED.search(combined):
        return False, f"no allowed location signal found: {location}"
    return True, ""


def check_experience(combined: str) -> tuple[bool, str]:
    if RE_EXPERIENCE.search(combined):
        return False, "experience requirement found"
    return True, ""


def check_seniority(combined: str) -> tuple[bool, str]:
    if RE_SENIORITY.search(combined):
        return False, "seniority level found (senior/staff/lead/SDE3+/L4+)"
    return True, ""


def check_degree(combined: str) -> tuple[bool, str]:
    if RE_DEGREE_BLOCKED.search(combined):
        return False, "advanced degree required (Masters/PhD)"
    return True, ""


# ═══════════════════════════════════════════════════════════════════════
# MASTER VALIDATION FUNCTION
# ═══════════════════════════════════════════════════════════════════════

def is_valid_internship(job: dict) -> bool:
    """
    Returns True only if ALL conditions pass:
      1. Technical engineering role
      2. Clearly internship/trainee (not new-grad/full-time)
      3. Location is India / Remote / WFH / Worldwide
      4. No 2+ years experience requirement
      5. No senior/staff/lead/SDE3+/L4+ seniority
      6. No PhD/Masters degree requirement
    """
    combined = _build_combined(job)
    title    = _get_title(job)
    location = _get_location(job)

    checks = [
        check_technical_role(title, combined),
        check_internship(title, combined),
        check_location(location, combined),
        check_experience(combined),
        check_seniority(combined),
        check_degree(combined),
    ]

    for passed, reason in checks:
        if not passed:
            log.debug(f"FILTERED [{job.get('company','?')}] {job.get('title','?')} — {reason}")
            return False

    return True


def filter_eligible(jobs: list[dict]) -> list[dict]:
    """Filter jobs list using is_valid_internship(). Returns only eligible jobs."""
    eligible = [job for job in jobs if is_valid_internship(job)]
    log.info(f"Eligibility filter: {len(eligible)}/{len(jobs)} jobs passed")
    return eligible
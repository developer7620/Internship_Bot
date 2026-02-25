"""
💰 Stipend Parser
Extracts numeric stipend value from messy strings like:
  "₹ 40,000/month", "40k", "Rs. 50000 per month", "$500", "Not mentioned"
Returns value in INR per month (int) or None if unparseable.
"""

import re

USD_TO_INR = 83  # approximate

def parse_stipend(text: str) -> int | None:
    if not text:
        return None

    text = text.lower().strip()

    # Clearly unpaid / not mentioned
    unpaid_markers = ["unpaid", "no stipend", "not mentioned", "not disclosed",
                      "n/a", "na", "none", "performance based", "equity only"]
    for marker in unpaid_markers:
        if marker in text:
            return None

    # Extract all numbers (handles commas, decimals)
    numbers = re.findall(r"[\d,]+(?:\.\d+)?", text.replace(",", ""))
    if not numbers:
        return None

    value = float(numbers[0])

    # Handle "k" suffix  e.g. "40k" or "40,000"
    if re.search(r"\d\s*k\b", text):
        value *= 1000

    # USD → INR
    if "$" in text or "usd" in text or "dollar" in text:
        value *= USD_TO_INR

    # Per week → per month
    if "week" in text or "/wk" in text:
        value *= 4

    # Per day → per month
    if "per day" in text or "/day" in text:
        value *= 22

    # Per annum → per month (lakh)
    if "lpa" in text or "per annum" in text or "per year" in text or "/yr" in text:
        if "lakh" in text or "lpa" in text:
            value = (value * 100000) / 12
        else:
            value = value / 12

    return int(value)


def stipend_passes_filter(stipend_text: str, min_stipend: int) -> bool:
    """Returns True if stipend meets minimum OR is unknown (give benefit of doubt)."""
    if min_stipend <= 0:
        return True
    value = parse_stipend(stipend_text)
    if value is None:
        return True   # Unknown stipend → include it (don't miss high-paying unlisted ones)
    return value >= min_stipend


def format_stipend(stipend_text: str) -> str:
    """Returns a clean display string with parsed value."""
    value = parse_stipend(stipend_text)
    if value is None:
        return stipend_text or "Not mentioned"
    if value >= 100000:
        return f"₹{value/100000:.1f}L/month 🔥"
    if value >= 40000:
        return f"₹{value:,}/month ✅"
    return f"₹{value:,}/month"

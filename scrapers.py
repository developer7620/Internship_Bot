"""
🔍 Scrapers v2
Sources: Internshala, LinkedIn, Naukri, Unstop, Wellfound,
         Greenhouse API, Lever API, Direct Career Pages
"""

import logging
import re
import httpx
from bs4 import BeautifulSoup
from config import KEYWORDS, EXCLUDE_KEYWORDS, CAREER_PAGES, ALLOWED_LOCATIONS, EXPERIENCE_BLOCKLIST, EXPERIENCE_ALLOWLIST

log = logging.getLogger("Scrapers")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


def is_eligible(title: str, location: str = "", description: str = "") -> bool:
    """
    Strict eligibility check:
    1. Location must be India / Remote / WFH (hybrid is BLOCKED)
    2. Must be intern/fresher/entry-level role
    3. Must not require experience
    """
    combined = (title + " " + location + " " + description).lower()
    title_lower  = title.lower()
    loc_lower    = location.lower().strip()

    # ── Location check ──────────────────────────────────────────
    BLOCKED_LOCATIONS = [
        "usa", "united states", "us only", "uk", "united kingdom",
        "canada", "australia", "singapore", "germany", "france",
        "europe", "emea", "latam", "us-based", "uk-based",
        "san francisco", "new york", "london", "toronto",
        "hybrid",  # blocked — requires physical presence
    ]

    # If location clearly says a blocked region → skip
    if loc_lower and loc_lower not in ["check listing", "not mentioned", ""]:
        for blocked in BLOCKED_LOCATIONS:
            if blocked in loc_lower:
                return False
        # If no allowed location keyword found either → skip
        location_ok = any(allowed in loc_lower for allowed in ALLOWED_LOCATIONS)
        if not location_ok:
            return False

    # ── Experience blocklist — check title + description ────────
    STRONG_BLOCKERS = [
        r"[2-9]\+\s*years?",          # 2+ years, 3+ years etc
        r"[2-9]\s*-\s*\d+\s*years?", # 2-4 years experience
        r"minimum [2-9] years?",
        r"at least [2-9] years?",
        r"senior",
        r"lead\s+(engineer|developer|backend)",
        r"staff\s+engineer",
        r"principal\s+engineer",
        r"director",
        r"manager",
        r"vp",
        r"full.?time only",
        r"no freshers?",
        r"no students?",
    ]
    for pattern in STRONG_BLOCKERS:
        if re.search(pattern, combined):
            return False

    # ── Must be intern/fresher friendly ─────────────────────────
    # Title says intern → always pass
    if re.search(r"(intern(ship)?|trainee|apprentice)", title_lower):
        return True

    # Description or title has fresher/entry-level signals → pass
    FRESHER_SIGNALS = [
        r"fresher", r"entry.?level", r"0.?1 year",
        r"no experience required", r"undergraduate",
        r"student", r"new grad", r"recent graduate",
        r"batch (of )?20(25|26|27)", r"class of 20(25|26|27)",
    ]
    for pattern in FRESHER_SIGNALS:
        if re.search(pattern, combined):
            return True

    # If no fresher signal found but also no blocker → include it
    # Better to see a few extra jobs than miss real opportunities
    return True


def matches_keywords(title: str) -> bool:
    title_lower = title.lower()
    for ex in EXCLUDE_KEYWORDS:
        if ex in title_lower:
            return False
    for kw in KEYWORDS:
        if kw in title_lower:
            return True
    return False


def is_internship(title: str, text: str = "") -> bool:
    combined = (title + " " + text).lower()
    return any(w in combined for w in ["intern", "internship", "trainee", "apprentice"])


# ─────────────────────────────────────────────
# JOB BOARD SCRAPERS
# ─────────────────────────────────────────────

async def scrape_internshala(client: httpx.AsyncClient) -> list[dict]:
    jobs = []
    categories = ["software-development", "web-development", "computer-science"]
    for cat in categories:
        try:
            url = f"https://internshala.com/internships/{cat}-internship/"
            r = await client.get(url, headers=HEADERS, timeout=15)
            soup = BeautifulSoup(r.text, "html.parser")
            for card in soup.select(".internship_meta"):
                try:
                    title_el   = card.select_one(".job-internship-name")
                    company_el = card.select_one(".company-name")
                    link_el    = card.select_one("a.view_detail_button")
                    stipend_el = card.select_one(".stipend")
                    location_el= card.select_one(".locations")
                    if not (title_el and company_el):
                        continue
                    title   = title_el.get_text(strip=True)
                    company = company_el.get_text(strip=True)
                    href    = link_el["href"] if link_el else ""
                    link    = f"https://internshala.com{href}" if href.startswith("/") else href
                    stipend = stipend_el.get_text(strip=True) if stipend_el else "Not mentioned"
                    location= location_el.get_text(strip=True) if location_el else "Remote/WFH"
                    if matches_keywords(title):
                        jobs.append({"title": title, "company": company, "link": link,
                                     "apply_url": link, "stipend": stipend, "location": location,
                                     "source": "Internshala"})
                except Exception:
                    continue
        except Exception as e:
            log.warning(f"Internshala error [{cat}]: {e}")
    return jobs


async def scrape_linkedin(client: httpx.AsyncClient) -> list[dict]:
    jobs = []
    searches = [
        "backend developer intern",
        "software engineer intern",
        "sde intern",
        "backend engineer internship",
    ]
    for keyword in searches:
        try:
            url = (
                f"https://www.linkedin.com/jobs/search/?"
                f"keywords={keyword.replace(' ', '%20')}"
                f"&location=India&f_TP=1&f_E=1"
            )
            r = await client.get(url, headers=HEADERS, timeout=20)
            soup = BeautifulSoup(r.text, "html.parser")
            for card in soup.select("li.result-card, li[class*='job']"):
                try:
                    title_el   = card.select_one("h3")
                    company_el = card.select_one("h4")
                    link_el    = card.select_one("a")
                    location_el= card.select_one("[class*='location']")
                    if not title_el:
                        continue
                    title   = title_el.get_text(strip=True)
                    company = company_el.get_text(strip=True) if company_el else "Company"
                    link    = link_el["href"].split("?")[0] if link_el else ""
                    location= location_el.get_text(strip=True) if location_el else "India"
                    if matches_keywords(title):
                        jobs.append({"title": title, "company": company, "link": link,
                                     "apply_url": link, "stipend": "Check listing",
                                     "location": location, "source": "LinkedIn"})
                except Exception:
                    continue
        except Exception as e:
            log.warning(f"LinkedIn error [{keyword}]: {e}")
    return jobs


async def scrape_naukri(client: httpx.AsyncClient) -> list[dict]:
    jobs = []
    queries = ["backend-developer-internship", "software-engineer-internship", "sde-internship"]
    for q in queries:
        try:
            url = f"https://www.naukri.com/{q}-jobs?jobAge=1"
            r = await client.get(url, headers=HEADERS, timeout=15)
            soup = BeautifulSoup(r.text, "html.parser")
            for card in soup.select("article.jobTuple, .cust-job-tuple"):
                try:
                    title_el   = card.select_one("a.title, .title")
                    company_el = card.select_one(".companyInfo a, .company-name")
                    stipend_el = card.select_one(".salary, [class*='salary']")
                    location_el= card.select_one(".location, [class*='location']")
                    if not title_el:
                        continue
                    title   = title_el.get_text(strip=True)
                    company = company_el.get_text(strip=True) if company_el else "Company"
                    link    = title_el.get("href", "https://naukri.com")
                    stipend = stipend_el.get_text(strip=True) if stipend_el else "Not mentioned"
                    location= location_el.get_text(strip=True) if location_el else "India"
                    if matches_keywords(title):
                        jobs.append({"title": title, "company": company, "link": link,
                                     "apply_url": link, "stipend": stipend,
                                     "location": location, "source": "Naukri"})
                except Exception:
                    continue
        except Exception as e:
            log.warning(f"Naukri error [{q}]: {e}")
    return jobs


async def scrape_unstop(client: httpx.AsyncClient) -> list[dict]:
    jobs = []
    try:
        url = "https://unstop.com/internships?oppstatus=open&domain=tech"
        r = await client.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")
        for card in soup.select(".opp-card, [class*='single_profile']"):
            try:
                title_el  = card.select_one("h2, .name")
                company_el= card.select_one(".org_name, h3")
                link_el   = card.select_one("a")
                stipend_el= card.select_one("[class*='stipend'], [class*='salary']")
                if not title_el:
                    continue
                title  = title_el.get_text(strip=True)
                company= company_el.get_text(strip=True) if company_el else "Company"
                href   = link_el["href"] if link_el else ""
                link   = f"https://unstop.com{href}" if href.startswith("/") else href
                stipend= stipend_el.get_text(strip=True) if stipend_el else "Not mentioned"
                if matches_keywords(title):
                    jobs.append({"title": title, "company": company, "link": link,
                                 "apply_url": link, "stipend": stipend,
                                 "location": "Check listing", "source": "Unstop"})
            except Exception:
                continue
    except Exception as e:
        log.warning(f"Unstop error: {e}")
    return jobs


async def scrape_wellfound(client: httpx.AsyncClient) -> list[dict]:
    jobs = []
    try:
        url = "https://wellfound.com/jobs?jobType=intern&role=Backend+Engineer&role=Software+Engineer"
        r = await client.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")
        for card in soup.select("[data-test='StartupResult']"):
            try:
                title_el  = card.select_one("a[data-test='job-title'], h2")
                company_el= card.select_one("a[data-test='startup-link'], h3")
                if not (title_el and company_el):
                    continue
                title  = title_el.get_text(strip=True)
                company= company_el.get_text(strip=True)
                href   = title_el.get("href", "")
                link   = f"https://wellfound.com{href}" if href.startswith("/") else href
                if matches_keywords(title):
                    jobs.append({"title": title, "company": company, "link": link,
                                 "apply_url": link, "stipend": "Check listing",
                                 "location": "Check listing", "source": "Wellfound"})
            except Exception:
                continue
    except Exception as e:
        log.warning(f"Wellfound error: {e}")
    return jobs


# ─────────────────────────────────────────────
# GREENHOUSE API
# ─────────────────────────────────────────────

async def scrape_greenhouse_board(client: httpx.AsyncClient, company: str, url: str) -> list[dict]:
    jobs = []
    try:
        r = await client.get(url, headers={**HEADERS, "Accept": "application/json"}, timeout=15)
        data = r.json()
        for job in data.get("jobs", []):
            title = job.get("title", "")
            location = job.get("location", {}).get("name", "Remote")
            apply_url = job.get("absolute_url", "")
            if (matches_keywords(title) and is_internship(title)):
                jobs.append({
                    "title": title, "company": company,
                    "link": apply_url, "apply_url": apply_url,
                    "stipend": "Check listing", "location": location,
                    "source": "Greenhouse",
                    "description": job.get("content", "")[:500],
                })
    except Exception as e:
        log.warning(f"Greenhouse error [{company}]: {e}")
    return jobs


# ─────────────────────────────────────────────
# LEVER API
# ─────────────────────────────────────────────

async def scrape_lever_board(client: httpx.AsyncClient, company: str, url: str) -> list[dict]:
    jobs = []
    try:
        r = await client.get(url, headers={**HEADERS, "Accept": "application/json"}, timeout=15)
        data = r.json()
        postings = data if isinstance(data, list) else data.get("postings", [])
        for job in postings:
            title    = job.get("text", "")
            location = job.get("categories", {}).get("location", "Remote")
            apply_url= job.get("applyUrl", job.get("hostedUrl", ""))
            desc     = job.get("descriptionPlain", "")[:500]
            if (matches_keywords(title) and is_internship(title, desc)):
                jobs.append({
                    "title": title, "company": company,
                    "link": apply_url, "apply_url": apply_url,
                    "stipend": "Check listing", "location": location,
                    "source": "Lever", "description": desc,
                })
    except Exception as e:
        log.warning(f"Lever error [{company}]: {e}")
    return jobs


# ─────────────────────────────────────────────
# DIRECT CAREER PAGES
# ─────────────────────────────────────────────

async def scrape_career_page(client: httpx.AsyncClient, page_config: dict) -> list[dict]:
    """Scrape a direct company career page."""
    jobs = []
    company = page_config["company"]
    url     = page_config["url"]

    # Route to API scrapers if applicable
    if page_config.get("greenhouse"):
        return await scrape_greenhouse_board(client, company, url)
    if page_config.get("lever") and "api.lever.co" in url:
        return await scrape_lever_board(client, company, url)

    try:
        r = await client.get(url, headers=HEADERS, timeout=20)
        soup = BeautifulSoup(r.text, "html.parser")
        selector = page_config.get("selector", "a[href*='job'], a[href*='career']")

        for link_el in soup.select(selector):
            try:
                title = link_el.get_text(strip=True)
                href  = link_el.get("href", "")
                if not title or len(title) < 5:
                    continue
                # Make absolute URL
                if href.startswith("/"):
                    from urllib.parse import urlparse
                    base = urlparse(url)
                    href = f"{base.scheme}://{base.netloc}{href}"
                elif not href.startswith("http"):
                    continue
                if matches_keywords(title) and is_internship(title):
                    jobs.append({
                        "title": title, "company": company,
                        "link": href, "apply_url": href,
                        "stipend": "Check listing", "location": "Check listing",
                        "source": f"Career Page ({company})",
                    })
            except Exception:
                continue
    except Exception as e:
        log.warning(f"Career page error [{company}]: {e}")
    return jobs


# ─────────────────────────────────────────────
# MASTER SCRAPE FUNCTION
# ─────────────────────────────────────────────

async def scrape_all(client: httpx.AsyncClient) -> list[dict]:
    import asyncio

    # Run all job board scrapers
    board_tasks = [
        scrape_internshala(client),
        scrape_linkedin(client),
        scrape_naukri(client),
        scrape_unstop(client),
        scrape_wellfound(client),
    ]

    # Run all career page scrapers
    career_tasks = [scrape_career_page(client, cfg) for cfg in CAREER_PAGES]

    all_tasks = board_tasks + career_tasks
    results = await asyncio.gather(*all_tasks, return_exceptions=True)

    jobs = []
    for r in results:
        if isinstance(r, Exception):
            log.debug(f"Scraper exception: {r}")
        else:
            jobs.extend(r)

    return jobs


def filter_eligible(jobs: list[dict]) -> list[dict]:
    """Filter jobs by location and experience eligibility."""
    eligible = []
    for job in jobs:
        location    = job.get("location", "")
        title       = job.get("title", "")
        description = job.get("description", "")
        if is_eligible(title, location, description):
            eligible.append(job)
        else:
            log.debug(f"Filtered out (not eligible): {job['company']} — {title} @ {location}")
    return eligible
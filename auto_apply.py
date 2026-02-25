"""
🤖 Auto-Apply Engine
Uses Playwright to automatically fill and submit internship applications.
Supports: Internshala, Greenhouse, Lever, and generic forms.
"""

import asyncio
import logging
import os
from pathlib import Path

from config import PROFILE
from cover_letter import generate_cover_letter

log = logging.getLogger("AutoApply")

# Track applied jobs this session
_applied_log = Path("applied_jobs.txt")


def mark_applied(job_id: str, job_title: str, company: str, url: str):
    with open(_applied_log, "a") as f:
        f.write(f"{job_id} | {company} | {job_title} | {url}\n")


def already_applied(job_id: str) -> bool:
    if not _applied_log.exists():
        return False
    return job_id in _applied_log.read_text()


async def apply_to_job(job: dict) -> str:
    """
    Master apply function. Routes to the right handler based on source.
    Returns: "applied", "skipped", or "failed"
    """
    source = job.get("source", "")
    apply_url = job.get("apply_url") or job.get("link", "")

    if already_applied(job.get("id", apply_url)):
        return "skipped"

    try:
        from playwright.async_api import async_playwright

        if source == "Internshala":
            result = await _apply_internshala(job, apply_url)
        elif source in ("Greenhouse",):
            result = await _apply_greenhouse(job, apply_url)
        elif source in ("Lever",):
            result = await _apply_lever(job, apply_url)
        else:
            result = await _apply_generic(job, apply_url)

        if result == "applied":
            mark_applied(
                job.get("id", apply_url),
                job.get("title", ""),
                job.get("company", ""),
                apply_url
            )
        return result

    except ImportError:
        log.error("Playwright not installed. Run: playwright install chromium")
        return "failed"
    except Exception as e:
        log.error(f"Auto-apply error for {job.get('company')}: {e}")
        return "failed"


async def _apply_internshala(job: dict, url: str) -> str:
    """Apply on Internshala — fills cover letter + submits."""
    from playwright.async_api import async_playwright

    cover = await generate_cover_letter(job["title"], job["company"])

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        )
        page = await context.new_page()

        try:
            await page.goto(url, timeout=20000)
            await page.wait_for_load_state("networkidle", timeout=15000)

            # Click Apply button
            apply_btn = page.locator("button:has-text('Apply'), a:has-text('Apply Now')")
            if await apply_btn.count() > 0:
                await apply_btn.first.click()
                await page.wait_for_timeout(2000)

            # Fill cover letter / "Why should we hire you"
            textarea = page.locator("textarea[name*='cover'], textarea[placeholder*='cover'], textarea[placeholder*='why'], #cover_letter_text")
            if await textarea.count() > 0:
                await textarea.first.fill(cover)

            # Availability field
            availability = page.locator("input[name*='availability'], select[name*='availability']")
            if await availability.count() > 0:
                await availability.first.fill("Immediately")

            # Submit
            submit_btn = page.locator("button[type='submit']:has-text('Submit'), button:has-text('Submit Application')")
            if await submit_btn.count() > 0:
                await submit_btn.first.click()
                await page.wait_for_timeout(3000)
                log.info(f"✅ Applied to {job['company']} - {job['title']} on Internshala")
                return "applied"
            else:
                log.warning(f"Could not find submit button for {job['company']}")
                return "failed"

        finally:
            await browser.close()


async def _apply_greenhouse(job: dict, url: str) -> str:
    """Apply via Greenhouse application form."""
    from playwright.async_api import async_playwright

    cover = await generate_cover_letter(
        job["title"], job["company"], job.get("description", "")
    )
    resume_path = Path(PROFILE["resume_path"]).resolve()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        try:
            await page.goto(url, timeout=20000)
            await page.wait_for_load_state("networkidle", timeout=15000)

            # First name
            first_name = page.locator("input[name='first_name'], input[id='first_name']")
            if await first_name.count() > 0:
                await first_name.first.fill(PROFILE["name"].split()[0])

            # Last name
            last_name = page.locator("input[name='last_name'], input[id='last_name']")
            if await last_name.count() > 0:
                parts = PROFILE["name"].split()
                await last_name.first.fill(parts[-1] if len(parts) > 1 else ".")

            # Email
            email = page.locator("input[name='email'], input[type='email']")
            if await email.count() > 0:
                await email.first.fill(PROFILE["email"])

            # Phone
            phone = page.locator("input[name='phone'], input[type='tel']")
            if await phone.count() > 0:
                await phone.first.fill(PROFILE["phone"])

            # Resume upload
            if resume_path.exists():
                resume_input = page.locator("input[type='file'][name*='resume'], input[type='file'][id*='resume']")
                if await resume_input.count() > 0:
                    await resume_input.first.set_input_files(str(resume_path))

            # LinkedIn
            linkedin_field = page.locator("input[name*='linkedin'], input[placeholder*='LinkedIn']")
            if await linkedin_field.count() > 0:
                await linkedin_field.first.fill(PROFILE["linkedin"])

            # GitHub
            github_field = page.locator("input[name*='github'], input[placeholder*='GitHub']")
            if await github_field.count() > 0:
                await github_field.first.fill(PROFILE["github"])

            # Cover letter
            cover_field = page.locator("textarea[name*='cover'], textarea[id*='cover']")
            if await cover_field.count() > 0:
                await cover_field.first.fill(cover)

            # Website / portfolio
            website_field = page.locator("input[name*='website'], input[name*='portfolio']")
            if await website_field.count() > 0:
                await website_field.first.fill(PROFILE["github"])

            # Submit
            submit_btn = page.locator("input[type='submit'], button[type='submit']")
            if await submit_btn.count() > 0:
                await submit_btn.first.click()
                await page.wait_for_timeout(4000)
                log.info(f"✅ Applied to {job['company']} - {job['title']} on Greenhouse")
                return "applied"

            return "failed"

        finally:
            await browser.close()


async def _apply_lever(job: dict, url: str) -> str:
    """Apply via Lever application form."""
    from playwright.async_api import async_playwright

    cover = await generate_cover_letter(
        job["title"], job["company"], job.get("description", "")
    )
    resume_path = Path(PROFILE["resume_path"]).resolve()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        try:
            await page.goto(url, timeout=20000)
            await page.wait_for_load_state("networkidle", timeout=15000)

            # Full name
            name_field = page.locator("input[name='name'], input[placeholder*='name' i]")
            if await name_field.count() > 0:
                await name_field.first.fill(PROFILE["name"])

            # Email
            email_field = page.locator("input[name='email'], input[type='email']")
            if await email_field.count() > 0:
                await email_field.first.fill(PROFILE["email"])

            # Phone
            phone_field = page.locator("input[name='phone'], input[type='tel']")
            if await phone_field.count() > 0:
                await phone_field.first.fill(PROFILE["phone"])

            # Resume
            if resume_path.exists():
                file_input = page.locator("input[type='file']")
                if await file_input.count() > 0:
                    await file_input.first.set_input_files(str(resume_path))
                    await page.wait_for_timeout(1500)

            # LinkedIn
            li_field = page.locator("input[placeholder*='LinkedIn' i], input[name*='linkedin' i]")
            if await li_field.count() > 0:
                await li_field.first.fill(PROFILE["linkedin"])

            # GitHub / Portfolio
            gh_field = page.locator("input[placeholder*='GitHub' i], input[placeholder*='portfolio' i]")
            if await gh_field.count() > 0:
                await gh_field.first.fill(PROFILE["github"])

            # Cover letter / additional info
            cl_field = page.locator("textarea[name*='comments'], textarea[name*='cover'], textarea[placeholder*='cover' i]")
            if await cl_field.count() > 0:
                await cl_field.first.fill(cover)

            # Submit
            submit = page.locator("button[type='submit'], input[type='submit']")
            if await submit.count() > 0:
                await submit.first.click()
                await page.wait_for_timeout(4000)
                log.info(f"✅ Applied to {job['company']} - {job['title']} on Lever")
                return "applied"

            return "failed"

        finally:
            await browser.close()


async def _apply_generic(job: dict, url: str) -> str:
    """
    Generic form filler — tries common field names.
    Works for many custom career pages.
    """
    from playwright.async_api import async_playwright

    cover = await generate_cover_letter(
        job["title"], job["company"], job.get("description", "")
    )
    resume_path = Path(PROFILE["resume_path"]).resolve()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        try:
            await page.goto(url, timeout=20000)
            await page.wait_for_load_state("networkidle", timeout=15000)

            # Try to find and fill common fields
            field_map = {
                "name":     PROFILE["name"],
                "email":    PROFILE["email"],
                "phone":    PROFILE["phone"],
                "linkedin": PROFILE["linkedin"],
                "github":   PROFILE["github"],
            }

            for key, value in field_map.items():
                field = page.locator(f"input[name*='{key}' i], input[placeholder*='{key}' i], input[id*='{key}' i]")
                if await field.count() > 0:
                    await field.first.fill(value)

            # Cover letter textarea
            textarea = page.locator("textarea")
            if await textarea.count() > 0:
                await textarea.first.fill(cover)

            # Resume file upload
            if resume_path.exists():
                file_input = page.locator("input[type='file']")
                if await file_input.count() > 0:
                    await file_input.first.set_input_files(str(resume_path))
                    await page.wait_for_timeout(1500)

            # Submit
            submit = page.locator("button[type='submit'], input[type='submit'], button:has-text('Submit'), button:has-text('Apply')")
            if await submit.count() > 0:
                await submit.first.click()
                await page.wait_for_timeout(3000)
                log.info(f"✅ Auto-applied to {job['company']} - {job['title']}")
                return "applied"

            return "failed"

        finally:
            await browser.close()

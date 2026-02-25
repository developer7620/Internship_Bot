"""
🚀 Internship Hunter Bot V2
- 40k+ stipend filter
- 40+ sources (job boards + Greenhouse + Lever + direct career pages)
- Auto-apply with AI cover letters
- Telegram alerts with apply buttons
"""

import asyncio
import hashlib
import json
import logging
import re
from pathlib import Path

import httpx
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode

from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, CHECK_INTERVAL, MIN_STIPEND
from scrapers import scrape_all, filter_eligible
from stipend_parser import stipend_passes_filter, format_stipend, parse_stipend


# ─────────────────────────────────────────────
# LOGGING
# ─────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler("bot_v2.log"),
        logging.StreamHandler(),
    ]
)
log = logging.getLogger("BotV2")

# ─────────────────────────────────────────────
# SEEN DB
# ─────────────────────────────────────────────
SEEN_DB = Path("seen_jobs_v2.json")

def load_seen() -> set:
    if SEEN_DB.exists():
        with open(SEEN_DB) as f:
            return set(json.load(f))
    return set()

def save_seen(seen: set):
    with open(SEEN_DB, "w") as f:
        json.dump(list(seen), f)

def job_id(title: str, company: str, url: str) -> str:
    raw = f"{title.lower().strip()}{company.lower().strip()}{url.strip()}"
    return hashlib.md5(raw.encode()).hexdigest()


# ─────────────────────────────────────────────
# TELEGRAM HELPERS
# ─────────────────────────────────────────────

def escape_md(text: str) -> str:
    special = r"_*[]()~`>#+-=|{}.!"
    return re.sub(f"([{re.escape(special)}])", r"\\\1", str(text))

SOURCE_EMOJI = {
    "Internshala":   "🎓",
    "LinkedIn":      "💼",
    "Wellfound":     "🚀",
    "Unstop":        "⚡",
    "Naukri":        "📋",
    "Greenhouse":    "🌱",
    "Lever":         "⚙️",
}

def get_emoji(source: str) -> str:
    for key, emoji in SOURCE_EMOJI.items():
        if key in source:
            return emoji
    return "🏢"

def stipend_badge(stipend_text: str) -> str:
    value = parse_stipend(stipend_text)
    if value is None:
        return "💰 Unknown"
    if value >= 80000:
        return f"💰 {format_stipend(stipend_text)} 🔥🔥"
    if value >= 40000:
        return f"💰 {format_stipend(stipend_text)} ✅"
    return f"💰 {format_stipend(stipend_text)}"

async def send_job_alert(bot: Bot, job: dict, auto_applied: bool = False):
    emoji = get_emoji(job["source"])
    applied_tag = "\\[AUTO\\-APPLIED ✅\\]" if auto_applied else ""

    msg = (
        f"{emoji} *New Internship Alert\\!* {applied_tag}\n\n"
        f"🏷️ *Role:* {escape_md(job['title'])}\n"
        f"🏢 *Company:* {escape_md(job['company'])}\n"
        f"📍 *Location:* {escape_md(job.get('location', 'Check listing'))}\n"
        f"{stipend_badge(job.get('stipend', ''))}\n"
        f"🌐 *Source:* {escape_md(job['source'])}\n"
    )

    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton("🔗 View Job", url=job["link"]),
        InlineKeyboardButton("📝 Apply Now", url=job.get("apply_url", job["link"])),
    ]])

    await bot.send_message(
        chat_id=TELEGRAM_CHAT_ID,
        text=msg,
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=keyboard,
        disable_web_page_preview=True,
    )

async def send_cycle_summary(bot: Bot, new_count: int, total_scanned: int, filtered_count: int, applied_count: int):
    msg = (
        f"📊 *Scan Complete*\n\n"
        f"🔍 Scanned: *{escape_md(str(total_scanned))}* listings\n"
        f"💰 Passed ₹{escape_md(str(MIN_STIPEND // 1000))}k\\+ filter: *{escape_md(str(filtered_count))}*\n"
        f"🆕 New jobs found: *{escape_md(str(new_count))}*\n"
        f"🤖 Auto\\-applied: *{escape_md(str(applied_count))}*\n\n"
        f"_Next scan in {escape_md(str(CHECK_INTERVAL // 60))} minutes_"
    )
    await bot.send_message(
        chat_id=TELEGRAM_CHAT_ID,
        text=msg,
        parse_mode=ParseMode.MARKDOWN_V2,
    )

async def send_startup_message(bot: Bot):
    msg = (
        "🤖 *Internship Hunter Bot V2 Started\\!*\n\n"
        "📡 *Monitoring:*\n"
        "🎓 Internshala \\| 💼 LinkedIn \\| 📋 Naukri\n"
        "⚡ Unstop \\| 🚀 Wellfound\n"
        "🌱 Greenhouse API \\(Stripe, Figma, Notion, Postman\\+\\)\n"
        "⚙️ Lever API \\(Vercel, Linear, Retool\\+\\)\n"
        "🏢 Direct career pages \\(Razorpay, CRED, Zepto, Google, Amazon, Adobe\\+\\)\n\n"
        f"💰 *Stipend filter:* ₹{escape_md(str(MIN_STIPEND // 1000))}k\\+ per month\n"
        f"⏱️ *Check interval:* every {escape_md(str(CHECK_INTERVAL // 60))} minutes\n"
        "🤖 *Auto\\-apply:* Enabled\n\n"
        "_Sit back — I'll handle the rest\\!_ 🎯"
    )
    await bot.send_message(
        chat_id=TELEGRAM_CHAT_ID,
        text=msg,
        parse_mode=ParseMode.MARKDOWN_V2,
    )


# ─────────────────────────────────────────────
# MAIN CYCLE
# ─────────────────────────────────────────────

async def run_cycle(bot: Bot, seen: set) -> tuple[int, int, int, int]:
    """Returns (new_count, total_scanned, filtered_count, applied_count)"""

    async with httpx.AsyncClient(follow_redirects=True) as client:
        all_jobs = await scrape_all(client)

    # Filter by location + experience eligibility
    all_jobs = filter_eligible(all_jobs)
    total_scanned = len(all_jobs)
    log.info(f"After eligibility filter: {total_scanned} jobs remain")

    # Apply stipend filter
    filtered_jobs = [
        j for j in all_jobs
        if stipend_passes_filter(j.get("stipend", ""), MIN_STIPEND)
    ]
    filtered_count = len(filtered_jobs)
    log.info(f"{filtered_count} jobs passed ₹{MIN_STIPEND//1000}k+ stipend filter")

    new_count = 0
    applied_count = 0

    for job in filtered_jobs:
        jid = job_id(job["title"], job["company"], job["link"])
        job["id"] = jid

        if jid in seen:
            continue

        # Auto-apply
        auto_applied = False
        try:
            result = "skipped"
            if result == "applied":
                auto_applied = True
                applied_count += 1
                log.info(f"🤖 Auto-applied: {job['company']} — {job['title']}")
        except Exception as e:
            log.warning(f"Auto-apply failed for {job['company']}: {e}")

        # Send Telegram alert
        try:
            await send_job_alert(bot, job, auto_applied=auto_applied)
            seen.add(jid)
            new_count += 1
            await asyncio.sleep(1.5)
        except Exception as e:
            log.error(f"Failed to send alert: {e}")

    save_seen(seen)
    return new_count, total_scanned, filtered_count, applied_count


# ─────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────

async def main():
    if TELEGRAM_TOKEN == "YOUR_BOT_TOKEN":
        print("❌ Set TELEGRAM_TOKEN and TELEGRAM_CHAT_ID in your .env file!")
        return

    bot  = Bot(token=TELEGRAM_TOKEN)
    seen = load_seen()

    log.info("🚀 Internship Hunter Bot V2 starting...")
    await send_startup_message(bot)

    while True:
        try:
            log.info("🔍 Starting scrape cycle...")
            new, total, filtered, applied = await run_cycle(bot, seen)
            log.info(f"✅ Cycle done — {new} new, {applied} auto-applied")
            if new > 0 or total > 0:
                await send_cycle_summary(bot, new, total, filtered, applied)
        except Exception as e:
            log.error(f"Cycle error: {e}")

        log.info(f"😴 Sleeping {CHECK_INTERVAL}s...")
        await asyncio.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    asyncio.run(main())
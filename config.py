"""
⚙️ INTERNSHIP BOT V2 — CONFIGURATION
Filled as per resume.
"""

# ─────────────────────────────────────────────
# YOUR PROFILE
# ─────────────────────────────────────────────
PROFILE = {
    "name":       "Aditya Anil Bhimanwar",
    "email":      "adityabhimanwar123@gmail.com",
    "phone":      "+91 7620862837",
    "linkedin":   "https://www.linkedin.com/in/aditya-bhimanwar-7209072a2/",
    "github":     "https://github.com/developer7620",
    "resume_path": "resume.pdf",
    
    "college":    "Indian Institute of Information Technology Kottayam",
    "degree":     "B.Tech Electronics and Communication Engineering",
    "grad_year":  "2027",
    
    "skills": (
        "C, C++, JavaScript, "
        "React.js, HTML5, CSS3, Tailwind CSS, Bootstrap, "
        "Node.js, Express.js, Prisma ORM, "
        "MongoDB, SQL, "
        "Git, GitHub, Postman, VS Code"
    ),
    
    "about": (
        "3rd year B.Tech ECE student at IIIT Kottayam (CGPA 8.65) "
        "with hands-on backend experience. Worked as a Software Engineering "
        "Intern at Granville Tech where I owned backend API development for "
        "a live education platform (ALETU), building production-grade APIs "
        "including scheduling, lessons, sessions, authentication, role-based "
        "access control, and admin systems using Node.js and Prisma. "
        "Solved 350+ DSA problems and built full-stack MERN applications."
    ),
}

# ─────────────────────────────────────────────
# TELEGRAM
# ─────────────────────────────────────────────
import os
from dotenv import load_dotenv
load_dotenv()

TELEGRAM_TOKEN   = os.getenv("TELEGRAM_TOKEN", "YOUR_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "YOUR_CHAT_ID")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# ─────────────────────────────────────────────
# FILTERS
# ─────────────────────────────────────────────
MIN_STIPEND = 40000
CHECK_INTERVAL = 3600

KEYWORDS = [
    "backend", "backend developer", "backend engineer",
    "software engineer intern", "sde intern", "software developer intern",
    "full stack intern", "node.js intern",
    "api developer intern", "platform engineer intern",
    "express intern", "mongodb intern",
]

EXCLUDE_KEYWORDS = [
    "frontend only", "react only", "ui/ux", "graphic design",
    "content writer", "marketing", "hr intern", "sales intern",
    "unpaid", "no stipend",
]

# ─────────────────────────────────────────────
# ELIGIBILITY FILTERS
# ─────────────────────────────────────────────
ALLOWED_LOCATIONS = [
    "india", "remote", "work from home", "wfh", "anywhere",
    "worldwide", "bengaluru", "bangalore", "mumbai", "delhi",
    "hyderabad", "pune", "chennai", "noida", "gurugram",
    "gurgaon", "kolkata", "ahmedabad", "kochi", "hybrid",
]

EXPERIENCE_BLOCKLIST = [
    "3+ years", "4+ years", "5+ years", "senior", "lead engineer",
    "manager", "director", "principal", "full time only", "no freshers",
    "minimum 2 years", "2+ years experience",
]

EXPERIENCE_ALLOWLIST = [
    "intern", "internship", "fresher", "0-1 year", "entry level",
    "entry-level", "trainee", "student", "undergraduate",
    "new grad", "recent graduate", "no experience required",
    "2026", "2027",
]

# ─────────────────────────────────────────────
# COMPANY CAREER PAGES (Direct monitoring)
# ─────────────────────────────────────────────
CAREER_PAGES = [

    # ════════════════════════════════════════
    # 🇮🇳 INDIAN UNICORNS & TOP STARTUPS
    # ════════════════════════════════════════
    {"company": "Razorpay",     "url": "https://razorpay.com/jobs/",                          "selector": "a[href*='job']",      "greenhouse": False},
    {"company": "CRED",         "url": "https://careers.cred.club/openings",                  "selector": "a[href*='opening']",  "greenhouse": False},
    {"company": "Groww",        "url": "https://groww.in/p/careers",                          "selector": "a[href*='job']",      "greenhouse": False},
    {"company": "PhonePe",      "url": "https://www.phonepe.com/en/careers.html",             "selector": "a[href*='job']",      "greenhouse": False},
    {"company": "Swiggy",       "url": "https://careers.swiggy.com/#/",                       "selector": "a[href*='career']",   "greenhouse": False},
    {"company": "Zomato",       "url": "https://www.zomato.com/careers",                      "selector": "a[href*='job']",      "greenhouse": False},
    {"company": "Ola",          "url": "https://www.olacabs.com/careers",                     "selector": "a[href*='job']",      "greenhouse": False},
    {"company": "Dream11",      "url": "https://www.dream11.com/careers",                     "selector": "a[href*='job']",      "greenhouse": False},
    {"company": "BrowserStack", "url": "https://www.browserstack.com/careers",                "selector": "a[href*='job']",      "greenhouse": False},
    {"company": "CleverTap",    "url": "https://clevertap.com/careers/",                      "selector": "a[href*='job']",      "greenhouse": False},
    {"company": "Zepto",        "url": "https://boards-api.greenhouse.io/v1/boards/zepto/jobs?content=true",       "greenhouse": True},
    {"company": "Meesho",       "url": "https://boards-api.greenhouse.io/v1/boards/meesho/jobs?content=true",      "greenhouse": True},
    {"company": "Nykaa",        "url": "https://boards-api.greenhouse.io/v1/boards/nykaa/jobs?content=true",       "greenhouse": True},
    {"company": "Paytm",        "url": "https://boards-api.greenhouse.io/v1/boards/paytm/jobs?content=true",       "greenhouse": True},
    {"company": "Dunzo",        "url": "https://boards-api.greenhouse.io/v1/boards/dunzo/jobs?content=true",       "greenhouse": True},
    {"company": "Slice",        "url": "https://boards-api.greenhouse.io/v1/boards/sliceit/jobs?content=true",     "greenhouse": True},
    {"company": "Jupiter",      "url": "https://boards-api.greenhouse.io/v1/boards/jupiter/jobs?content=true",     "greenhouse": True},
    {"company": "Cashfree",     "url": "https://boards-api.greenhouse.io/v1/boards/cashfree/jobs?content=true",    "greenhouse": True},
    {"company": "Darwinbox",    "url": "https://boards-api.greenhouse.io/v1/boards/darwinbox/jobs?content=true",   "greenhouse": True},
    {"company": "Setu",         "url": "https://boards-api.greenhouse.io/v1/boards/setu/jobs?content=true",        "greenhouse": True},
    {"company": "Smallcase",    "url": "https://boards-api.greenhouse.io/v1/boards/smallcase/jobs?content=true",   "greenhouse": True},
    {"company": "Khatabook",    "url": "https://boards-api.greenhouse.io/v1/boards/khatabook/jobs?content=true",   "greenhouse": True},
    {"company": "Leadsquared",  "url": "https://boards-api.greenhouse.io/v1/boards/leadsquared/jobs?content=true", "greenhouse": True},
    {"company": "Chargebee",    "url": "https://boards-api.greenhouse.io/v1/boards/chargebee/jobs?content=true",   "greenhouse": True},
    {"company": "Hasura",       "url": "https://boards-api.greenhouse.io/v1/boards/hasura/jobs?content=true",      "greenhouse": True},
    {"company": "Appsmith",     "url": "https://boards-api.greenhouse.io/v1/boards/appsmith/jobs?content=true",    "greenhouse": True},
    {"company": "Lenskart",     "url": "https://boards-api.greenhouse.io/v1/boards/lenskart/jobs?content=true",    "greenhouse": True},
    {"company": "UrbanCompany", "url": "https://boards-api.greenhouse.io/v1/boards/urbancompany/jobs?content=true","greenhouse": True},
    {"company": "Unacademy",    "url": "https://boards-api.greenhouse.io/v1/boards/unacademy/jobs?content=true",   "greenhouse": True},
    {"company": "Vedantu",      "url": "https://boards-api.greenhouse.io/v1/boards/vedantu/jobs?content=true",     "greenhouse": True},
    {"company": "Innovaccer",   "url": "https://boards-api.greenhouse.io/v1/boards/innovaccer/jobs?content=true",  "greenhouse": True},
    {"company": "Postman",      "url": "https://boards-api.greenhouse.io/v1/boards/postman/jobs?content=true",     "greenhouse": True},

    # ════════════════════════════════════════
    # 🌏 BIG TECH — INDIA OFFICES
    # ════════════════════════════════════════
    {"company": "Google",      "url": "https://www.google.com/about/careers/applications/jobs/results/?q=intern&location=India&employment_type=INTERN", "selector": "a[href*='/jobs/results/']", "greenhouse": False},
    {"company": "Microsoft",   "url": "https://careers.microsoft.com/v2/global/en/home.html?q=intern&lc=India&p=Software%20Engineering", "selector": "a[href*='job']", "greenhouse": False},
    {"company": "Amazon",      "url": "https://www.amazon.jobs/en/search?base_query=intern&loc_query=India&job_type=intern", "selector": "a.job-link", "greenhouse": False},
    {"company": "Adobe",       "url": "https://careers.adobe.com/us/en/search-results?keywords=intern&country=India", "selector": "a[href*='job']", "greenhouse": False},
    {"company": "Atlassian",   "url": "https://www.atlassian.com/company/careers/all-jobs?team=Engineering&location=India&search=intern", "selector": "a[href*='job']", "greenhouse": False},
    {"company": "Salesforce",  "url": "https://salesforce.wd12.myworkdayjobs.com/en-US/External_Career_Site?q=intern&locationCountry=IN", "selector": "a[href*='job']", "workday": True},
    {"company": "Cisco",       "url": "https://boards-api.greenhouse.io/v1/boards/cisco/jobs?content=true",        "greenhouse": True},
    {"company": "Nvidia",      "url": "https://boards-api.greenhouse.io/v1/boards/nvidia/jobs?content=true",       "greenhouse": True},
    {"company": "Cloudflare",  "url": "https://boards-api.greenhouse.io/v1/boards/cloudflare/jobs?content=true",   "greenhouse": True},
    {"company": "Datadog",     "url": "https://boards-api.greenhouse.io/v1/boards/datadog/jobs?content=true",      "greenhouse": True},
    {"company": "Hubspot",     "url": "https://boards-api.greenhouse.io/v1/boards/hubspot/jobs?content=true",      "greenhouse": True},
    {"company": "Twilio",      "url": "https://boards-api.greenhouse.io/v1/boards/twilio/jobs?content=true",       "greenhouse": True},
    {"company": "MongoDB",     "url": "https://boards-api.greenhouse.io/v1/boards/mongodb/jobs?content=true",      "greenhouse": True},
    {"company": "Elastic",     "url": "https://boards-api.greenhouse.io/v1/boards/elastic/jobs?content=true",      "greenhouse": True},
    {"company": "Okta",        "url": "https://boards-api.greenhouse.io/v1/boards/okta/jobs?content=true",         "greenhouse": True},
    {"company": "PagerDuty",   "url": "https://boards-api.greenhouse.io/v1/boards/pagerduty/jobs?content=true",    "greenhouse": True},
    {"company": "Zendesk",     "url": "https://boards-api.greenhouse.io/v1/boards/zendesk/jobs?content=true",      "greenhouse": True},
    {"company": "Squarespace", "url": "https://boards-api.greenhouse.io/v1/boards/squarespace/jobs?content=true",  "greenhouse": True},
    {"company": "Duolingo",    "url": "https://boards-api.greenhouse.io/v1/boards/duolingo/jobs?content=true",     "greenhouse": True},
    {"company": "Robinhood",   "url": "https://boards-api.greenhouse.io/v1/boards/robinhood/jobs?content=true",    "greenhouse": True},
    {"company": "Rippling",    "url": "https://boards-api.greenhouse.io/v1/boards/rippling/jobs?content=true",     "greenhouse": True},

    # ════════════════════════════════════════
    # 🚀 TOP GLOBAL PRODUCT STARTUPS (Greenhouse)
    # ════════════════════════════════════════
    {"company": "Stripe",      "url": "https://boards-api.greenhouse.io/v1/boards/stripe/jobs?content=true",       "greenhouse": True},
    {"company": "Figma",       "url": "https://boards-api.greenhouse.io/v1/boards/figma/jobs?content=true",        "greenhouse": True},
    {"company": "Notion",      "url": "https://boards-api.greenhouse.io/v1/boards/notion/jobs?content=true",       "greenhouse": True},
    {"company": "Airbnb",      "url": "https://boards-api.greenhouse.io/v1/boards/airbnb/jobs?content=true",       "greenhouse": True},
    {"company": "Coinbase",    "url": "https://boards-api.greenhouse.io/v1/boards/coinbase/jobs?content=true",     "greenhouse": True},
    {"company": "Brex",        "url": "https://boards-api.greenhouse.io/v1/boards/brex/jobs?content=true",         "greenhouse": True},
    {"company": "Scale AI",    "url": "https://boards-api.greenhouse.io/v1/boards/scaleai/jobs?content=true",      "greenhouse": True},
    {"company": "Plaid",       "url": "https://boards-api.greenhouse.io/v1/boards/plaid/jobs?content=true",        "greenhouse": True},
    {"company": "Deel",        "url": "https://boards-api.greenhouse.io/v1/boards/deel/jobs?content=true",         "greenhouse": True},
    {"company": "Airtable",    "url": "https://boards-api.greenhouse.io/v1/boards/airtable/jobs?content=true",     "greenhouse": True},
    {"company": "Intercom",    "url": "https://boards-api.greenhouse.io/v1/boards/intercom/jobs?content=true",     "greenhouse": True},
    {"company": "Asana",       "url": "https://boards-api.greenhouse.io/v1/boards/asana/jobs?content=true",        "greenhouse": True},
    {"company": "Miro",        "url": "https://boards-api.greenhouse.io/v1/boards/miro/jobs?content=true",         "greenhouse": True},
    {"company": "Grammarly",   "url": "https://boards-api.greenhouse.io/v1/boards/grammarly/jobs?content=true",    "greenhouse": True},
    {"company": "Canva",       "url": "https://boards-api.greenhouse.io/v1/boards/canva/jobs?content=true",        "greenhouse": True},
    {"company": "Calendly",    "url": "https://boards-api.greenhouse.io/v1/boards/calendly/jobs?content=true",     "greenhouse": True},
    {"company": "Loom",        "url": "https://boards-api.greenhouse.io/v1/boards/loom/jobs?content=true",         "greenhouse": True},
    {"company": "Lattice",     "url": "https://boards-api.greenhouse.io/v1/boards/lattice/jobs?content=true",      "greenhouse": True},
    {"company": "Gusto",       "url": "https://boards-api.greenhouse.io/v1/boards/gusto/jobs?content=true",        "greenhouse": True},
    {"company": "Front",       "url": "https://boards-api.greenhouse.io/v1/boards/front/jobs?content=true",        "greenhouse": True},
    {"company": "Mixpanel",    "url": "https://boards-api.greenhouse.io/v1/boards/mixpanel/jobs?content=true",     "greenhouse": True},
    {"company": "Amplitude",   "url": "https://boards-api.greenhouse.io/v1/boards/amplitude/jobs?content=true",    "greenhouse": True},
    {"company": "Segment",     "url": "https://boards-api.greenhouse.io/v1/boards/segment/jobs?content=true",      "greenhouse": True},
    {"company": "Contentful",  "url": "https://boards-api.greenhouse.io/v1/boards/contentful/jobs?content=true",   "greenhouse": True},
    {"company": "Snyk",        "url": "https://boards-api.greenhouse.io/v1/boards/snyk/jobs?content=true",         "greenhouse": True},
    {"company": "Sentry",      "url": "https://boards-api.greenhouse.io/v1/boards/sentry/jobs?content=true",       "greenhouse": True},
    {"company": "LaunchDarkly","url": "https://boards-api.greenhouse.io/v1/boards/launchdarkly/jobs?content=true", "greenhouse": True},
    {"company": "Figma",       "url": "https://boards-api.greenhouse.io/v1/boards/figma/jobs?content=true",        "greenhouse": True},
    {"company": "Netlify",     "url": "https://boards-api.greenhouse.io/v1/boards/netlify/jobs?content=true",      "greenhouse": True},
    {"company": "Weights & Biases", "url": "https://boards-api.greenhouse.io/v1/boards/wandb/jobs?content=true",  "greenhouse": True},
    {"company": "Hugging Face","url": "https://boards-api.greenhouse.io/v1/boards/huggingface/jobs?content=true",  "greenhouse": True},
    {"company": "Cohere",      "url": "https://boards-api.greenhouse.io/v1/boards/cohere/jobs?content=true",       "greenhouse": True},
    {"company": "Anthropic",   "url": "https://boards-api.greenhouse.io/v1/boards/anthropic/jobs?content=true",    "greenhouse": True},
    {"company": "OpenAI",      "url": "https://boards-api.greenhouse.io/v1/boards/openai/jobs?content=true",       "greenhouse": True},
    {"company": "Mistral AI",  "url": "https://boards-api.greenhouse.io/v1/boards/mistral/jobs?content=true",      "greenhouse": True},
    {"company": "Perplexity",  "url": "https://boards-api.greenhouse.io/v1/boards/perplexity/jobs?content=true",   "greenhouse": True},
    {"company": "Cursor",      "url": "https://boards-api.greenhouse.io/v1/boards/anysphere/jobs?content=true",    "greenhouse": True},

    # ════════════════════════════════════════
    # ⚙️ LEVER API — TOP COMPANIES
    # ════════════════════════════════════════
    {"company": "Vercel",      "url": "https://api.lever.co/v0/postings/vercel?mode=json",     "lever": True},
    {"company": "Linear",      "url": "https://api.lever.co/v0/postings/linear?mode=json",     "lever": True},
    {"company": "Retool",      "url": "https://api.lever.co/v0/postings/retool?mode=json",     "lever": True},
    {"company": "Supabase",    "url": "https://api.lever.co/v0/postings/supabase?mode=json",   "lever": True},
    {"company": "PlanetScale", "url": "https://api.lever.co/v0/postings/planetscale?mode=json","lever": True},
    {"company": "Deno",        "url": "https://api.lever.co/v0/postings/deno?mode=json",       "lever": True},
    {"company": "Railway",     "url": "https://api.lever.co/v0/postings/railway?mode=json",    "lever": True},
    {"company": "Render",      "url": "https://api.lever.co/v0/postings/render?mode=json",     "lever": True},
    {"company": "Neon",        "url": "https://api.lever.co/v0/postings/neondatabase?mode=json","lever": True},
    {"company": "Turso",       "url": "https://api.lever.co/v0/postings/turso?mode=json",      "lever": True},
    {"company": "Temporal",    "url": "https://api.lever.co/v0/postings/temporal?mode=json",   "lever": True},
    {"company": "Grafana",     "url": "https://api.lever.co/v0/postings/grafana?mode=json",    "lever": True},
    {"company": "Sourcegraph", "url": "https://api.lever.co/v0/postings/sourcegraph?mode=json","lever": True},
    {"company": "Zepto",       "url": "https://api.lever.co/v0/postings/zepto?mode=json",      "lever": True},
    {"company": "Meesho",      "url": "https://api.lever.co/v0/postings/meesho?mode=json",     "lever": True},
    {"company": "Razorpay",    "url": "https://api.lever.co/v0/postings/razorpay?mode=json",   "lever": True},
    {"company": "CRED",        "url": "https://api.lever.co/v0/postings/cred?mode=json",       "lever": True},
    {"company": "Groww",       "url": "https://api.lever.co/v0/postings/groww?mode=json",      "lever": True},
    {"company": "Swiggy",      "url": "https://api.lever.co/v0/postings/swiggy?mode=json",     "lever": True},
    {"company": "BrowserStack","url": "https://api.lever.co/v0/postings/browserstack?mode=json","lever": True},

    # ════════════════════════════════════════
    # 💰 FINTECH & CRYPTO
    # ════════════════════════════════════════
    {"company": "Zerodha",     "url": "https://zerodha.com/careers/",                          "selector": "a[href*='job']",     "greenhouse": False},
    {"company": "AngelOne",    "url": "https://www.angelone.in/careers",                       "selector": "a[href*='job']",     "greenhouse": False},
    {"company": "Fi Money",    "url": "https://boards-api.greenhouse.io/v1/boards/epifi/jobs?content=true",   "greenhouse": True},
    {"company": "Open Money",  "url": "https://boards-api.greenhouse.io/v1/boards/openmoney/jobs?content=true","greenhouse": True},
    {"company": "Polygon",     "url": "https://boards-api.greenhouse.io/v1/boards/polygon/jobs?content=true", "greenhouse": True},
    {"company": "Alchemy",     "url": "https://boards-api.greenhouse.io/v1/boards/alchemy/jobs?content=true", "greenhouse": True},

    # ════════════════════════════════════════
    # 🤖 AI / ML COMPANIES
    # ════════════════════════════════════════
    {"company": "Sarvam AI",   "url": "https://boards-api.greenhouse.io/v1/boards/sarvamai/jobs?content=true",  "greenhouse": True},
    {"company": "Krutrim",     "url": "https://boards-api.greenhouse.io/v1/boards/krutrim/jobs?content=true",   "greenhouse": True},
    {"company": "Together AI", "url": "https://boards-api.greenhouse.io/v1/boards/togetherai/jobs?content=true","greenhouse": True},
    {"company": "Replicate",   "url": "https://boards-api.greenhouse.io/v1/boards/replicate/jobs?content=true", "greenhouse": True},
    {"company": "Modal",       "url": "https://boards-api.greenhouse.io/v1/boards/modal/jobs?content=true",     "greenhouse": True},
    {"company": "Langchain",   "url": "https://boards-api.greenhouse.io/v1/boards/langchain/jobs?content=true", "greenhouse": True},

    # ════════════════════════════════════════
    # 🛒 E-COMMERCE & CONSUMER
    # ════════════════════════════════════════
    {"company": "Flipkart",    "url": "https://boards-api.greenhouse.io/v1/boards/flipkart/jobs?content=true",  "greenhouse": True},
    {"company": "Myntra",      "url": "https://boards-api.greenhouse.io/v1/boards/myntra/jobs?content=true",    "greenhouse": True},
    {"company": "Blinkit",     "url": "https://boards-api.greenhouse.io/v1/boards/blinkit/jobs?content=true",   "greenhouse": True},
    {"company": "BigBasket",   "url": "https://boards-api.greenhouse.io/v1/boards/bigbasket/jobs?content=true", "greenhouse": True},
    {"company": "Shopify",     "url": "https://boards-api.greenhouse.io/v1/boards/shopify/jobs?content=true",   "greenhouse": True},

    # ════════════════════════════════════════
    # 🏗️ INFRASTRUCTURE & DEVTOOLS
    # ════════════════════════════════════════
    {"company": "HashiCorp",   "url": "https://boards-api.greenhouse.io/v1/boards/hashicorp/jobs?content=true", "greenhouse": True},
    {"company": "Pulumi",      "url": "https://boards-api.greenhouse.io/v1/boards/pulumi/jobs?content=true",    "greenhouse": True},
    {"company": "Cockroach DB","url": "https://boards-api.greenhouse.io/v1/boards/cockroachlabs/jobs?content=true","greenhouse": True},
    {"company": "Redpanda",    "url": "https://boards-api.greenhouse.io/v1/boards/redpanda/jobs?content=true",  "greenhouse": True},
    {"company": "Clickhouse",  "url": "https://boards-api.greenhouse.io/v1/boards/clickhouse/jobs?content=true","greenhouse": True},
    {"company": "Novu",        "url": "https://boards-api.greenhouse.io/v1/boards/novu/jobs?content=true",      "greenhouse": True},
    {"company": "Resend",      "url": "https://api.lever.co/v0/postings/resend?mode=json",     "lever": True},
    {"company": "Upstash",     "url": "https://api.lever.co/v0/postings/upstash?mode=json",    "lever": True},
]















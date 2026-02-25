"""
⚙️ INTERNSHIP BOT V2 — CONFIGURATION
Edit this file with your details before running.
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
        "3rd year B.Tech student at IIIT Kottayam (CGPA 8.65) with hands-on backend experience. "
        "Worked as a Software Engineering Intern at Granville Tech where I owned backend API "
        "development for a live education platform (ALETU), building production-grade APIs "
        "including scheduling, lessons, sessions, quizzes, authentication, and admin systems "
        "using Node.js and Prisma. Strong foundation in DSA (200+ problems solved) and "
        "experienced in full-stack development with MERN."
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
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")  # For AI cover letters (optional)

# ─────────────────────────────────────────────
# FILTERS
# ─────────────────────────────────────────────
MIN_STIPEND = 40000   # Minimum monthly stipend in INR (0 = no filter)
CHECK_INTERVAL = 1800 # Seconds between scrape cycles (1800 = 30 min)

KEYWORDS = [
    "backend", "backend developer", "backend engineer",
    "software engineer intern", "sde intern", "software developer intern",
    "full stack intern", "node.js intern", "python intern",
    "java intern", "golang intern", "django intern", "flask intern",
    "fastapi intern", "devops intern", "platform engineer intern",
    "api developer intern", "cloud intern",
]

EXCLUDE_KEYWORDS = [
    "frontend only", "react only", "ui/ux", "graphic design",
    "content writer", "marketing", "hr intern", "sales intern",
    "unpaid", "no stipend",
]

# ─────────────────────────────────────────────
# COMPANY CAREER PAGES (Direct monitoring)
# ─────────────────────────────────────────────
CAREER_PAGES = [
    # ── Indian Unicorns ──────────────────────
    {
        "company": "Razorpay",
        "url": "https://razorpay.com/jobs/",
        "selector": "a[href*='job']",
        "greenhouse": False,
    },
    {
        "company": "CRED",
        "url": "https://careers.cred.club/openings",
        "selector": "a[href*='opening']",
        "greenhouse": False,
    },
    {
        "company": "Zepto",
        "url": "https://jobs.lever.co/zepto",
        "selector": "a.posting-title",
        "lever": True,
    },
    {
        "company": "Groww",
        "url": "https://groww.in/p/careers",
        "selector": "a[href*='job']",
        "greenhouse": False,
    },
    {
        "company": "Meesho",
        "url": "https://meesho.io/jobs",
        "selector": "a[href*='job']",
        "greenhouse": False,
    },
    {
        "company": "PhonePe",
        "url": "https://www.phonepe.com/en/careers.html",
        "selector": "a[href*='job']",
        "greenhouse": False,
    },
    {
        "company": "Swiggy",
        "url": "https://careers.swiggy.com/#/",
        "selector": "a[href*='career']",
        "greenhouse": False,
    },
    {
        "company": "Zomato",
        "url": "https://www.zomato.com/careers",
        "selector": "a[href*='job']",
        "greenhouse": False,
    },
    {
        "company": "Paytm",
        "url": "https://jobs.lever.co/paytm",
        "selector": "a.posting-title",
        "lever": True,
    },
    {
        "company": "Ola",
        "url": "https://www.olacabs.com/careers",
        "selector": "a[href*='job']",
        "greenhouse": False,
    },
    {
        "company": "Dream11",
        "url": "https://www.dream11.com/careers",
        "selector": "a[href*='job']",
        "greenhouse": False,
    },
    {
        "company": "Nykaa",
        "url": "https://jobs.lever.co/nykaa",
        "selector": "a.posting-title",
        "lever": True,
    },
    {
        "company": "BrowserStack",
        "url": "https://www.browserstack.com/careers",
        "selector": "a[href*='job']",
        "greenhouse": False,
    },
    {
        "company": "Clevertap",
        "url": "https://clevertap.com/careers/",
        "selector": "a[href*='job']",
        "greenhouse": False,
    },

    # ── Big Tech (India offices) ─────────────
    {
        "company": "Google",
        "url": "https://careers.google.com/jobs/results/?q=intern&location=India&employment_type=INTERN",
        "selector": "a[href*='/jobs/results/']",
        "greenhouse": False,
    },
    {
        "company": "Microsoft",
        "url": "https://jobs.careers.microsoft.com/global/en/search?q=intern&lc=India&p=Software%20Engineering&exp=Students%20and%20graduates",
        "selector": "a[href*='job']",
        "greenhouse": False,
    },
    {
        "company": "Amazon",
        "url": "https://www.amazon.jobs/en/search?base_query=intern&loc_query=India&job_type=intern",
        "selector": "a.job-link",
        "greenhouse": False,
    },
    {
        "company": "Adobe",
        "url": "https://careers.adobe.com/us/en/search-results?keywords=intern&country=India",
        "selector": "a[href*='job']",
        "greenhouse": False,
    },
    {
        "company": "Atlassian",
        "url": "https://www.atlassian.com/company/careers/all-jobs?team=Engineering&location=India&search=intern",
        "selector": "a[href*='job']",
        "greenhouse": False,
    },
    {
        "company": "Uber",
        "url": "https://www.uber.com/us/en/careers/list/?query=intern&department=Engineering",
        "selector": "a[href*='job']",
        "greenhouse": False,
    },
    {
        "company": "Salesforce",
        "url": "https://salesforce.wd12.myworkdayjobs.com/en-US/External_Career_Site?q=intern&locationCountry=IN",
        "selector": "a[href*='job']",
        "workday": True,
    },

    # ── Greenhouse API targets ───────────────
    {
        "company": "Postman",
        "url": "https://boards-api.greenhouse.io/v1/boards/postman/jobs?content=true",
        "greenhouse": True,
    },
    {
        "company": "Notion",
        "url": "https://boards-api.greenhouse.io/v1/boards/notion/jobs?content=true",
        "greenhouse": True,
    },
    {
        "company": "Figma",
        "url": "https://boards-api.greenhouse.io/v1/boards/figma/jobs?content=true",
        "greenhouse": True,
    },
    {
        "company": "Stripe",
        "url": "https://boards-api.greenhouse.io/v1/boards/stripe/jobs?content=true",
        "greenhouse": True,
    },
    {
        "company": "Airbnb",
        "url": "https://boards-api.greenhouse.io/v1/boards/airbnb/jobs?content=true",
        "greenhouse": True,
    },
    {
        "company": "Coinbase",
        "url": "https://boards-api.greenhouse.io/v1/boards/coinbase/jobs?content=true",
        "greenhouse": True,
    },
    {
        "company": "Rippling",
        "url": "https://boards-api.greenhouse.io/v1/boards/rippling/jobs?content=true",
        "greenhouse": True,
    },
    {
        "company": "Deel",
        "url": "https://boards-api.greenhouse.io/v1/boards/deel/jobs?content=true",
        "greenhouse": True,
    },
    {
        "company": "Scale AI",
        "url": "https://boards-api.greenhouse.io/v1/boards/scaleai/jobs?content=true",
        "greenhouse": True,
    },
    {
        "company": "Plaid",
        "url": "https://boards-api.greenhouse.io/v1/boards/plaid/jobs?content=true",
        "greenhouse": True,
    },
    {
        "company": "Brex",
        "url": "https://boards-api.greenhouse.io/v1/boards/brex/jobs?content=true",
        "greenhouse": True,
    },

    # ── Lever API targets ────────────────────
    {
        "company": "Vercel",
        "url": "https://api.lever.co/v0/postings/vercel?mode=json",
        "lever": True,
    },
    {
        "company": "Linear",
        "url": "https://api.lever.co/v0/postings/linear?mode=json",
        "lever": True,
    },
    {
        "company": "Retool",
        "url": "https://api.lever.co/v0/postings/retool?mode=json",
        "lever": True,
    },
    {
        "company": "Loom",
        "url": "https://api.lever.co/v0/postings/loom?mode=json",
        "lever": True,
    },
]

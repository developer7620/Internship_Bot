"""
✍️ AI Cover Letter Generator
Uses Claude API to generate personalized cover letters for each job.
Falls back to a template if no API key is set.
"""

import httpx
from config import PROFILE, ANTHROPIC_API_KEY


TEMPLATE = """Dear Hiring Team,

I am {name}, a {degree} student at {college} (Class of {grad_year}), writing to express my strong interest in the {title} position at {company}.

I have hands-on experience with {skills}, and I am particularly excited about {company}'s work in building products at scale. As a backend-focused developer, I thrive on solving complex infrastructure and API challenges.

I would love to contribute to {company}'s engineering team as an intern and grow through the experience. I have attached my resume for your review.

GitHub: {github}
LinkedIn: {linkedin}

Thank you for your time and consideration.

Best regards,
{name}
{email} | {phone}
"""


async def generate_cover_letter(job_title: str, company: str, job_description: str = "") -> str:
    """Generate a personalized cover letter. Uses Claude API if key is set, else template."""

    if ANTHROPIC_API_KEY:
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                resp = await client.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={
                        "x-api-key": ANTHROPIC_API_KEY,
                        "anthropic-version": "2023-06-01",
                        "content-type": "application/json",
                    },
                    json={
                        "model": "claude-haiku-4-5-20251001",
                        "max_tokens": 600,
                        "messages": [{
                            "role": "user",
                            "content": f"""Write a concise, professional cover letter for this internship application.

Applicant profile:
- Name: {PROFILE['name']}
- College: {PROFILE['college']}, {PROFILE['degree']}, Graduating {PROFILE['grad_year']}
- Skills: {PROFILE['skills']}
- About: {PROFILE['about']}
- GitHub: {PROFILE['github']}
- LinkedIn: {PROFILE['linkedin']}

Job: {job_title} at {company}
Job description snippet: {job_description[:500] if job_description else 'Not provided'}

Instructions:
- 3 short paragraphs max
- Sound enthusiastic but not desperate
- Mention 2-3 specific relevant skills
- End with a call to action
- Do NOT use placeholders like [Your Name] — use the actual values above
- Plain text only, no markdown
"""
                        }]
                    }
                )
                data = resp.json()
                return data["content"][0]["text"].strip()
        except Exception as e:
            print(f"Claude API error, using template: {e}")

    # Fallback template
    return TEMPLATE.format(
        name=PROFILE["name"],
        degree=PROFILE["degree"],
        college=PROFILE["college"],
        grad_year=PROFILE["grad_year"],
        title=job_title,
        company=company,
        skills=PROFILE["skills"],
        github=PROFILE["github"],
        linkedin=PROFILE["linkedin"],
        email=PROFILE["email"],
        phone=PROFILE["phone"],
    )

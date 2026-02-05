from typing import Union, List, Dict, Any
from mcp.server.fastmcp import FastMCP
from src.job_api import fetch_linkedin_jobs
from src.helper import ask_openai  # <-- uses your Groq model

mcp = FastMCP("Job Recommender")

@mcp.tool()
async def fetchlinkedin_from_cv(
    resume_text: str,
    location: str = "Germany",
    rows_per_keyword: int = 15,
    max_roles: int = 5
) -> List[Dict[str, Any]]:
    """
    1) Read resume
    2) Infer best job titles using Groq
    3) Fetch LinkedIn jobs for those titles
    """

    # ---- STEP 1: Ask Groq to infer roles from YOUR CV ----
    roles_text = ask_openai(
        f"""
        Based on this resume, suggest the best {max_roles} job titles 
        that fit this candidate in Germany.
        Return ONLY a comma-separated list, no explanations.

        Resume:
        {resume_text}
        """,
        max_tokens=100
    )

    # Convert LLM output into a clean list
    keyword_list = [r.strip() for r in roles_text.split(",") if r.strip()]
    keyword_list = keyword_list[:max_roles]

    print("ROLES GENERATED FROM CV:", keyword_list)

    # ---- STEP 2: Search LinkedIn for each role ----
    all_jobs: List[Dict[str, Any]] = []
    seen_links = set()

    for title in keyword_list:
        jobs = fetch_linkedin_jobs(title, location=location, rows=rows_per_keyword)

        for job in jobs:
            link = job.get("link") or job.get("url")
            if link and link in seen_links:
                continue
            if link:
                seen_links.add(link)

            all_jobs.append(job)

    return all_jobs


if __name__ == "__main__":
    mcp.run(transport="stdio")

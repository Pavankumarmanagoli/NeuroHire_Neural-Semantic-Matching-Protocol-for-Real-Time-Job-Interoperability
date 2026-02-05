from apify_client import ApifyClient
import os
from dotenv import load_dotenv

load_dotenv()

apify_client = ApifyClient(os.getenv("APIFY_API_TOKEN"))

def fetch_linkedin_jobs(search_query, location="Germany", rows=60):
    run_input = {
        "title": search_query,
        "location": location,
        "rows": rows,
        # ✅ simpler proxy (more reliable)
        "proxy": {"useApifyProxy": True},
    }

    run = apify_client.actor("BHzefUZlZRKWxkTck").call(run_input=run_input)

    # ✅ Debug output shows in your terminal
    print("APIFY RUN STATUS:", run.get("status"))
    print("APIFY STATUS MESSAGE:", run.get("statusMessage"))
    print("APIFY ERROR:", run.get("errorMessage"))

    jobs = list(apify_client.dataset(run["defaultDatasetId"]).iterate_items())
    print("JOBS RETURNED:", len(jobs))
    return jobs

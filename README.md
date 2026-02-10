# NeuroHire: Neural Semantic Matching Protocol for Real-Time Job Interoperability

NeuroHire is an AI-powered job matching project that analyzes a candidate’s resume, gives overview of it and recommends relevant roles in Germany.

It provides two interfaces:

- **Streamlit Web App** (`app.py`) for interactive resume upload, analysis, and job recommendations.
- **MCP Tool Server** (`mcp_server.py`) exposing a tool that can infer job roles from CV text and fetch LinkedIn jobs programmatically.

---

## Features

- Upload a **PDF resume** and extract text with **PyMuPDF**.
- Generate:
  - Resume summary
  - Skill-gap analysis (Germany market oriented)
  - 3‑month preparation roadmap
- Infer the best matching job title(s) via **Groq LLM**.
- Fetch LinkedIn job listings via **Apify** actor integration.
- Query job recommendations directly through an **MCP tool**.

---

## Project Structure

```text
.
├── app.py                  # Streamlit UI for resume analysis + job recommendations
├── mcp_server.py           # MCP server exposing CV→LinkedIn jobs tool
├── src/
│   ├── helper.py           # PDF extraction + Groq completion helper
│   └── job_api.py          # Apify LinkedIn job fetcher
├── pyproject.toml          # Project metadata and dependencies
├── requirements.txt        # Pip-friendly dependency list
└── README.md
```

---

## Tech Stack

- **Python 3.11+**
- **Streamlit** for UI
- **Groq SDK** for LLM-based resume understanding and role inference
- **Apify Client** for LinkedIn jobs scraping actor calls
- **PyMuPDF** for PDF parsing
- **python-dotenv** for local secret management

---

## Prerequisites

Before running the project, ensure you have:

1. Python `>=3.11`
2. A Groq API key
3. An Apify API token

---

## Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
APIFY_API_TOKEN=your_apify_api_token
```

The app loads these variables automatically using `python-dotenv`.

---

## Installation

### Option A: pip + requirements.txt

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Option B: uv (if you use uv in your workflow)

```bash
uv sync
```

---

## Run the Streamlit App

```bash
streamlit run app.py
```

Then open the local URL shown by Streamlit (typically `http://localhost:8501`).

### App Flow

1. Upload resume (PDF)
2. Choose location (Germany/Berlin/Munich/etc.)
3. View:
   - Resume summary
   - Skill gaps
   - Roadmap
4. Click **Get Job Recommendations** to fetch matching LinkedIn roles

---

## Run the MCP Server

```bash
python mcp_server.py
```

This starts the MCP server over `stdio` transport and exposes the tool:

- `fetchlinkedin_from_cv(resume_text, location="Germany", rows_per_keyword=15, max_roles=5)`

### MCP Tool Behavior

- Uses the LLM to infer the top role titles from resume text
- Searches LinkedIn jobs for each inferred role via Apify
- De-duplicates results by job link
- Returns aggregated job objects

---

## Notes and Limitations

- LinkedIn results quality/availability depends on the configured Apify actor and current platform response.
- LLM output may vary between runs (temperature-based generation).
- API keys are required for both Groq and Apify functionality.
- This project currently targets **Germany-focused** role matching by default.

---

## Troubleshooting

- **No jobs returned**
  - Verify `APIFY_API_TOKEN`
  - Try location = `Germany` or a major city (e.g., Berlin)
  - Check terminal logs for actor status/error messages

- **LLM calls fail**
  - Verify `GROQ_API_KEY`
  - Confirm internet connectivity

- **PDF parsing issues**
  - Ensure uploaded file is a valid, text-readable PDF

---

## Future Improvements

- Add caching for repeated LLM/API requests
- Add unit/integration tests for `src/helper.py` and `src/job_api.py`
- Add configurable model and actor IDs via environment variables
- Add support for additional countries and multilingual resumes
- Improve ranking/scoring of returned jobs against extracted CV skills

---

## License

This repository is licensed under the terms in `MIT LICENSE`.


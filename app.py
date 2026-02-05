import streamlit as st
from src.helper import extract_text_from_pdf, ask_openai
from src.job_api import fetch_linkedin_jobs

st.set_page_config(page_title="Job Recommender (Germany)", layout="wide")
st.title("📄 AI Job Recommender (Germany)")
st.markdown("Upload your resume and get job recommendations from LinkedIn for Germany.")

uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

# ✅ Use simple location strings (works better with this actor)
location = st.selectbox(
    "Select location",
    ["Germany", "Berlin", "Munich", "Hamburg", "Frankfurt", "Cologne", "Remote"],
    index=0
)

if uploaded_file:
    with st.spinner("Extracting text from your resume..."):
        resume_text = extract_text_from_pdf(uploaded_file)

    with st.spinner("Summarizing your resume..."):
        summary = ask_openai(
            f"Summarize this resume highlighting skills, education, and experience in 6 bullet points:\n\n{resume_text}",
            max_tokens=300
        )

    # ✅ Cheaper + more stable: use summary for next steps (not full resume again)
    with st.spinner("Finding skill gaps..."):
        gaps = ask_openai(
            f"Based on this summary, list skill gaps for Germany job market (tools, cloud, data engineering, BI). Use bullets:\n\n{summary}",
            max_tokens=250
        )

    with st.spinner("Creating future roadmap..."):
        roadmap = ask_openai(
            f"Based on this summary, create a 3-month roadmap for Germany jobs (skills, projects, certs). Use bullets:\n\n{summary}",
            max_tokens=250
        )

    st.markdown("---")
    st.header("📑 Resume Summary")
    st.markdown(
        f"<div style='background-color:#000000; padding:15px; border-radius:10px; font-size:16px; color:white;'>{summary}</div>",
        unsafe_allow_html=True
    )

    st.markdown("---")
    st.header("🛠️ Skill Gaps & Missing Areas")
    st.markdown(
        f"<div style='background-color:#000000; padding:15px; border-radius:10px; font-size:16px; color:white;'>{gaps}</div>",
        unsafe_allow_html=True
    )

    st.markdown("---")
    st.header("🚀 Future Roadmap & Preparation Strategy")
    st.markdown(
        f"<div style='background-color:#000000; padding:15px; border-radius:10px; font-size:16px; color:white;'>{roadmap}</div>",
        unsafe_allow_html=True
    )

    st.success("✅ Analysis Completed Successfully!")

    if st.button("🔎 Get Job Recommendations (Germany)"):
        with st.spinner("Choosing ONE best job title for your profile..."):
            # ✅ ONE title only (not comma list)
            job_title = ask_openai(
                f"Based on this summary, give ONLY ONE best job title to search on LinkedIn in Germany. "
                f"Return only the job title text, nothing else.\n\nSummary:\n{summary}",
                max_tokens=20
            ).strip()

        st.success(f"Using Job Title: {job_title}")

        # ✅ Map Remote -> Germany
        search_location = "Germany" if location == "Remote" else location

        with st.spinner(f"Fetching jobs from LinkedIn for: {search_location} ..."):
            linkedin_jobs = fetch_linkedin_jobs(
                job_title,
                location=search_location,
                rows=60
            )

        st.markdown("---")
        st.header(f"🇩🇪 Top LinkedIn Jobs in {search_location}")

        if linkedin_jobs:
            for job in linkedin_jobs:
                st.markdown(f"**{job.get('title')}** at *{job.get('companyName')}*")
                st.markdown(f"- 📍 {job.get('location')}")
                st.markdown(f"- 🔗 [View Job]({job.get('link')})")
                st.markdown("---")
        else:
            st.warning(
                "No LinkedIn jobs found. Check your terminal logs for Apify run status/errors. "
                "Try changing location to 'Germany' or 'Berlin'."
            )

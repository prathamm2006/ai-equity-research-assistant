import streamlit as st
from tools.scraper import search_company_info, scrape_url_text
from tools.pdf_reader import read_pdf, chunk_text
from tools.swot import get_llm, generate_swot, generate_competitor_summary, generate_ppt_content

st.set_page_config(page_title="AI-Powered Equity & Business Research Assistant", layout="wide")
st.title("📊 AI-Powered Equity & Business Research Assistant")

with st.sidebar:
    api_key = st.text_input("Gemini API Key", type="password")
    company = st.text_input("Company Name", "Tata Motors")
    uploaded_pdf = st.file_uploader("Upload Annual Report (PDF)", type="pdf")
    run_btn = st.button("Run Research")

if run_btn:
    if not api_key:
        st.error("Enter your free Gemini API key (get one at aistudio.google.com)")
        st.stop()

    llm = get_llm(api_key)

    # Step 1: Web scraping
    with st.spinner("Searching company info..."):
        results = search_company_info(f"{company} company overview competitors business")
        web_context = "\n".join([f"{r['title']}: {r['body']}" for r in results])

    # Step 2: PDF context
    pdf_context = ""
    if uploaded_pdf:
        with st.spinner("Reading annual report..."):
            text = read_pdf(uploaded_pdf)
            pdf_context = text[:6000]  # use first chunk for context

    full_context = web_context + "\n\n" + pdf_context

    st.subheader("🔍 Source Data")
    with st.expander("View scraped/PDF context"):
        st.text(full_context[:3000])

    # Step 3: SWOT
    with st.spinner("Generating SWOT analysis..."):
        swot = generate_swot(llm, company, full_context)
    st.subheader("📈 SWOT Analysis")
    st.markdown(swot)

    # Step 4: Competitors
    with st.spinner("Analyzing competitors..."):
        competitors = generate_competitor_summary(llm, company, full_context)
    st.subheader("🏢 Competitor Summary")
    st.markdown(competitors)

    # Step 5: PPT-ready content
    with st.spinner("Generating PPT content..."):
        ppt_content = generate_ppt_content(llm, company, swot, competitors)
    st.subheader("📑 PPT-Ready Insights")
    st.text(ppt_content)

    st.download_button("Download PPT Content (.txt)", ppt_content, file_name=f"{company}_ppt_content.txt")
import streamlit as st
from tools.scraper import search_company_info
from tools.pdf_reader import read_pdf
from tools.swot import get_llm, generate_full_report
from tools.financials import build_financial_comparison
from tools.report_pdf import markdown_to_pdf

st.set_page_config(page_title="AI-Powered Equity & Business Research Assistant", layout="wide")
st.title("📊 AI-Powered Equity & Business Research Assistant")

with st.sidebar:
    api_key = st.text_input("Gemini API Key (optional if set in secrets)", type="password")
    if not api_key:
        try:
            api_key = st.secrets.get("GEMINI_API_KEY", "")
        except Exception:
            api_key = ""

    company = st.text_input("Company Name", "Tata Motors")

    st.markdown("**Financial Data (Yahoo Finance Tickers)**")
    main_ticker = st.text_input("Company Ticker (e.g., TATAMOTORS.NS, AAPL)", "TATAMOTORS.NS")
    competitor_tickers_raw = st.text_input(
        "Competitor Tickers (comma-separated)",
        "M&M.NS, MARUTI.NS"
    )

    uploaded_pdf = st.file_uploader("Upload Annual Report (PDF)", type="pdf")
    run_btn = st.button("Run Deep Research")

st.caption(
    "Tip: Find tickers on [finance.yahoo.com](https://finance.yahoo.com) — "
    "Indian stocks use suffix `.NS` (NSE) or `.BO` (BSE). US stocks use plain symbols (e.g., AAPL, MSFT)."
)

if run_btn:
    if not api_key:
        st.error("Enter your free Gemini API key (get one at aistudio.google.com)")
        st.stop()

    llm = get_llm(api_key)

    # Step 1: Web scraping
    with st.spinner("Searching company info..."):
        results = search_company_info(f"{company} company overview competitors business strategy")
        web_context = "\n".join([f"{r['title']}: {r['body']}" for r in results])

    # Step 2: PDF context
    pdf_context = ""
    if uploaded_pdf:
        with st.spinner("Reading annual report..."):
            text = read_pdf(uploaded_pdf)
            pdf_context = text[:8000]

    # Step 3: Financial data via yfinance
    financial_context = ""
    with st.spinner("Fetching financial data from Yahoo Finance..."):
        competitor_tickers = [t.strip() for t in competitor_tickers_raw.split(",") if t.strip()]
        try:
            financial_context = build_financial_comparison(main_ticker.strip(), competitor_tickers)
        except Exception as e:
            financial_context = f"Could not fetch financial data: {e}"
            st.warning("Financial data fetch failed — proceeding with web/PDF context only.")

    st.subheader("📐 Financial Data Snapshot")
    with st.expander("View raw financial comparison data"):
        st.markdown(financial_context)

    st.subheader("🔍 Source Context")
    with st.expander("View scraped web/PDF context"):
        st.text((web_context + "\n\n" + pdf_context)[:3000])

    # Step 4: Single combined deep research report
    with st.spinner("Generating deep research report (this may take 30-60s)..."):
        report = generate_full_report(llm, company, web_context, pdf_context, financial_context)

    st.subheader("📑 Deep Research Report")
    st.markdown(report)

    # Step 5: PDF download
    with st.spinner("Preparing PDF report..."):
        try:
            pdf_bytes = markdown_to_pdf(report, company)
            st.download_button(
                "📥 Download Full Report (PDF)",
                data=bytes(pdf_bytes),
                file_name=f"{company.replace(' ', '_')}_Research_Report.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"PDF generation failed: {e}")

    # Markdown download as backup
    st.download_button(
        "📥 Download Report (Markdown)",
        data=report,
        file_name=f"{company.replace(' ', '_')}_Research_Report.md",
        mime="text/markdown"
    )
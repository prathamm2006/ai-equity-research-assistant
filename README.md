# 📊 AI-Powered Equity & Business Research Assistant

An AI agent that automates equity and business research — scraping live company information, reading annual reports, summarizing competitors, generating SWOT analysis, and producing PPT-ready insights using LLMs.

🔗 **Live Demo:** [ai-equity-research.streamlit.app](https://ai-equity-research.streamlit.app/)

---

## 🚀 Features

- **Live Company Research** — scrapes up-to-date web information about any company
- **Annual Report Analysis** — upload a PDF annual report for the AI to incorporate into its analysis
- **SWOT Analysis Generator** — produces a structured Strengths, Weaknesses, Opportunities, Threats breakdown
- **Competitor Summary** — identifies and summarizes key competitors and their market positioning
- **PPT-Ready Insights** — converts research into slide-ready bullet points, downloadable as a text file

---

## 🛠️ Tech Stack

- **Python**
- **Streamlit** — interactive web UI
- **LangChain** — orchestration of prompts and LLM chains
- **Google Gemini API** (`gemini-2.5-flash`) — LLM-powered analysis
- **DuckDuckGo Search** — free web scraping/search
- **BeautifulSoup** — HTML parsing
- **PyPDF** — annual report (PDF) text extraction

---

## 📂 Project Structure

```
ai-equity-research-assistant/
├── app.py                 # Streamlit app entry point
├── tools/
│   ├── scraper.py          # Web search & scraping
│   ├── pdf_reader.py        # PDF text extraction
│   └── swot.py              # LLM prompts & chains (SWOT, competitors, PPT content)
├── requirements.txt
└── .streamlit/
    └── secrets.toml         # API key (not committed)
```

---

## ⚙️ How It Works

1. User enters a company name (and optionally uploads an annual report PDF)
2. The agent searches the web for live company and competitor information
3. Extracted text from the PDF (if provided) is added as context
4. LangChain prompts the Gemini LLM to generate:
   - A detailed SWOT analysis
   - A competitor landscape summary
   - PPT-ready slide content for presentations
5. Results are displayed in the app and available for download

---

## 🖥️ Running Locally

```bash
git clone https://github.com/<your-username>/ai-equity-research-assistant.git
cd ai-equity-research-assistant
pip install -r requirements.txt
streamlit run app.py
```

Get a free Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey) and enter it in the sidebar, or add it to `.streamlit/secrets.toml`:

```toml
GEMINI_API_KEY = "your_api_key_here"
```

---

## 📌 Use Case

Built as a portfolio project demonstrating how LLM-powered agents can assist equity research analysts and business strategists by automating time-consuming research, competitor analysis, and presentation prep — reducing hours of manual work to minutes.

---

## 📄 License

This project is for educational and portfolio purposes.

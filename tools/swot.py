from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate


def get_llm(api_key):
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key,
        temperature=0.3
    )


DEEP_RESEARCH_PROMPT = PromptTemplate(
    input_variables=["company", "web_context", "pdf_context", "financial_context"],
    template="""
You are a senior equity research analyst preparing a professional research report for institutional investors.
Write in a formal, analytical tone — avoid generic/superficial statements. Use the data provided to ground every claim.

Company: {company}

=== WEB RESEARCH CONTEXT ===
{web_context}

=== ANNUAL REPORT EXTRACT (if provided) ===
{pdf_context}

=== FINANCIAL DATA (Company vs Competitors) ===
{financial_context}

Produce a structured report in Markdown with these EXACT sections:

## 1. Company Overview
2-3 paragraphs covering business model, key segments, and recent strategic developments.

## 2. Financial Performance Analysis
Analyze the financial data provided above. Compare the company's revenue, net income (PAT), margins (gross/operating/profit), ROE, P/E ratio, and debt levels against its competitors. Highlight which company is financially stronger and why, citing specific numbers.

## 3. Competitive Landscape
For each competitor, summarize positioning, market share/strategy, and how they stack up financially against the main company based on the data above.

## 4. SWOT Analysis
### Strengths (4-5 bullets, grounded in financial/business data above)
### Weaknesses (4-5 bullets)
### Opportunities (4-5 bullets)
### Threats (4-5 bullets)

## 5. Investment Recommendation
A balanced 2-3 paragraph view (Buy/Hold/Watch-style commentary) based on financial comparison and SWOT — frame as analyst opinion, not financial advice.

## 6. PPT-Ready Slide Summary
Convert the above into slide titles + max 6 bullet points each, for slides:
- Slide 1: Company Overview
- Slide 2: Financial Snapshot (with key numbers)
- Slide 3: Competitive Positioning
- Slide 4: SWOT Analysis
- Slide 5: Recommendation

Be specific, data-driven, and avoid vague filler statements like "the company has good potential". Cite actual figures from the financial data wherever possible.
"""
)


def generate_full_report(llm, company, web_context, pdf_context, financial_context):
    chain = DEEP_RESEARCH_PROMPT | llm
    result = chain.invoke({
        "company": company,
        "web_context": web_context,
        "pdf_context": pdf_context if pdf_context else "Not provided.",
        "financial_context": financial_context if financial_context else "Not available."
    })
    return result.content
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

def get_llm(api_key):
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key,
        temperature=0.3
    )

SWOT_PROMPT = PromptTemplate(
    input_variables=["company", "context"],
    template="""
You are a senior equity research analyst. Based on the following information about {company}, 
generate a detailed SWOT analysis (Strengths, Weaknesses, Opportunities, Threats) — 4-5 bullet points each.

Context:
{context}

Format output in clean markdown with headers.
"""
)

COMPETITOR_PROMPT = PromptTemplate(
    input_variables=["company", "context"],
    template="""
Based on this information, identify the top competitors of {company} and summarize 
each competitor's positioning, strengths, and market share in 2-3 lines.

Context:
{context}
"""
)

PPT_PROMPT = PromptTemplate(
    input_variables=["company", "swot", "competitors"],
    template="""
Convert the following research into PPT-ready bullet points (max 6 bullets per slide).
Create slides for: 1) Company Overview, 2) SWOT Analysis, 3) Competitive Landscape, 4) Key Recommendations.

Company: {company}
SWOT: {swot}
Competitors: {competitors}

Output as slide titles with bullet points, plain text format.
"""
)

def generate_swot(llm, company, context):
    chain = SWOT_PROMPT | llm
    return chain.invoke({"company": company, "context": context}).content

def generate_competitor_summary(llm, company, context):
    chain = COMPETITOR_PROMPT | llm
    return chain.invoke({"company": company, "context": context}).content

def generate_ppt_content(llm, company, swot, competitors):
    chain = PPT_PROMPT | llm
    return chain.invoke({"company": company, "swot": swot, "competitors": competitors}).content
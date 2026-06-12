import yfinance as yf
import pandas as pd


def get_financial_summary(ticker_symbol):
    """Fetch key financials for a company using yfinance."""
    try:
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info

        data = {
            "Company Name": info.get("longName", ticker_symbol),
            "Sector": info.get("sector", "N/A"),
            "Industry": info.get("industry", "N/A"),
            "Market Cap": info.get("marketCap", "N/A"),
            "Revenue (TTM)": info.get("totalRevenue", "N/A"),
            "Net Income (PAT)": info.get("netIncomeToCommon", "N/A"),
            "Profit Margin": info.get("profitMargins", "N/A"),
            "Operating Margin": info.get("operatingMargins", "N/A"),
            "EBITDA": info.get("ebitda", "N/A"),
            "Gross Margin": info.get("grossMargins", "N/A"),
            "PE Ratio": info.get("trailingPE", "N/A"),
            "Debt to Equity": info.get("debtToEquity", "N/A"),
            "ROE": info.get("returnOnEquity", "N/A"),
            "Current Price": info.get("currentPrice", "N/A"),
            "52W High": info.get("fiftyTwoWeekHigh", "N/A"),
            "52W Low": info.get("fiftyTwoWeekLow", "N/A"),
        }
        return data
    except Exception as e:
        return {"Error": f"Could not fetch data for {ticker_symbol}: {e}"}


def format_financial_table(data_dict, label):
    """Format a single company's financials as a markdown row set."""
    lines = [f"### {label} ({data_dict.get('Company Name', '')})"]
    for k, v in data_dict.items():
        if k == "Company Name":
            continue
        if isinstance(v, float):
            if "Margin" in k or k == "ROE":
                v = f"{v * 100:.2f}%"
            else:
                v = f"{v:,.2f}"
        elif isinstance(v, int):
            v = f"{v:,}"
        lines.append(f"- **{k}**: {v}")
    return "\n".join(lines)


def build_financial_comparison(main_ticker, competitor_tickers):
    """Build a combined financial comparison block for main company + competitors."""
    sections = []

    main_data = get_financial_summary(main_ticker)
    sections.append(format_financial_table(main_data, "Main Company"))

    for i, comp_ticker in enumerate(competitor_tickers, 1):
        comp_data = get_financial_summary(comp_ticker.strip())
        sections.append(format_financial_table(comp_data, f"Competitor {i}"))

    return "\n\n".join(sections)
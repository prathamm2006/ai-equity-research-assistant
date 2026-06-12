from fpdf import FPDF
import re


class ReportPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(30, 30, 30)
        self.cell(0, 10, self.title_text, ln=True, align="C")
        self.ln(2)
        self.set_draw_color(180, 180, 180)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")


def clean_text(text):
    """Remove markdown symbols not handled and ensure latin-1 safe characters."""
    text = text.replace("**", "")
    text = text.replace("*", "-")
    text = text.replace("#", "")
    # Replace common unicode chars with ascii equivalents
    replacements = {
        "\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"',
        "\u2013": "-", "\u2014": "-", "\u2022": "-", "\u2026": "...",
        "\u20b9": "Rs.", "\u00a0": " "
    }
    for uni, ascii_eq in replacements.items():
        text = text.replace(uni, ascii_eq)
    # Strip any remaining non-latin-1 characters
    text = text.encode("latin-1", "ignore").decode("latin-1")

    # Break up very long unbroken "words" (URLs, long tickers, etc.)
    # that fpdf2 cannot wrap, by inserting spaces every 40 chars.
    words = text.split(" ")
    safe_words = []
    for w in words:
        if len(w) > 40:
            chunks = [w[i:i+40] for i in range(0, len(w), 40)]
            safe_words.append(" ".join(chunks))
        else:
            safe_words.append(w)
    return " ".join(safe_words)


def markdown_to_pdf(markdown_text, company_name):
    pdf = ReportPDF()
    pdf.title_text = f"Equity Research Report - {company_name}"
    pdf.set_margins(left=12, top=15, right=12)
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    lines = markdown_text.split("\n")

    for line in lines:
        line = line.rstrip()
        if not line.strip():
            pdf.ln(2)
            continue

        line_clean = clean_text(line)
        if not line_clean.strip():
            pdf.ln(2)
            continue
        pdf.set_x(pdf.l_margin)

        if line.startswith("## "):
            pdf.ln(3)
            pdf.set_x(pdf.l_margin)
            pdf.set_font("Helvetica", "B", 13)
            pdf.set_text_color(20, 60, 120)
            pdf.multi_cell(0, 8, line_clean.replace("## ", ""))
            pdf.set_text_color(0, 0, 0)
            pdf.ln(1)
        elif line.startswith("### "):
            pdf.set_font("Helvetica", "B", 11)
            pdf.set_text_color(50, 90, 150)
            pdf.multi_cell(0, 7, line_clean.replace("### ", ""))
            pdf.set_text_color(0, 0, 0)
        elif line.startswith("- ") or line.startswith("* "):
            pdf.set_font("Helvetica", "", 10)
            pdf.multi_cell(0, 6, "- " + line_clean[2:])
        elif re.match(r"^\d+\.\s", line):
            pdf.set_font("Helvetica", "", 10)
            pdf.multi_cell(0, 6, line_clean)
        else:
            pdf.set_font("Helvetica", "", 10)
            pdf.multi_cell(0, 6, line_clean)

    return pdf.output(dest="S")
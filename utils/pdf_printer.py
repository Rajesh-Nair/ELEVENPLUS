from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def save_text_to_pdf(text: str, filename: str = "styled_output.pdf"):
    # Create PDF document
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=1*inch,
        bottomMargin=1*inch,
    )

    # Define custom style
    custom_style = ParagraphStyle(
        name="Custom",
        fontName="Helvetica",     # Options: 'Times-Roman', 'Courier', 'Helvetica'
        fontSize=16,              # Font size
        leading=22,               # Line spacing (usually 120-140% of font size)
        spaceAfter=12,            # Space after each paragraph
    )

    # Split text into paragraphs
    paragraphs = text.split("\n")
    flowables = [Paragraph(p, custom_style) for p in paragraphs if p.strip()]

    # Build PDF
    doc.build(flowables)
    print(f"PDF saved as {filename}")



from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors

def save_text_to_pdf(text: str, filename: str = "styled_output.pdf", title: str = None):
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

    # Prepare content for PDF
    flowables = []
    
    # Add title if provided
    if title:
        title_style = ParagraphStyle(
            name="Title",
            fontName="Helvetica-Bold",
            fontSize=20,
            alignment=1,  # Center alignment
            spaceAfter=20,
        )
        title_paragraph = Paragraph(title, title_style)
        flowables.append(title_paragraph)

    # Split text into paragraphs
    paragraphs = text.split("\n")
    text_paragraphs = [Paragraph(p, custom_style) for p in paragraphs if p.strip()]
    flowables.extend(text_paragraphs)

    # Build PDF
    doc.build(flowables)
    print(f"PDF saved as {filename}")


def save_dict_list_to_pdf(data: list[dict], filename: str = "table_output.pdf", title: str = None):
    """
    Create a PDF table from a list of dictionaries with 2 keys.
    
    Args:
        data: List of dictionaries, each containing exactly 2 keys
        filename: Output PDF filename
        title: Optional title to display at the top of the PDF
    """
    if not data:
        print("No data provided")
        return
    
    # Get the two keys from the first dictionary
    keys = list(data[0].keys())
    if len(keys) != 2:
        print("Error: Each dictionary must contain exactly 2 keys")
        return
    
    # Create PDF document
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=1*inch,
        bottomMargin=1*inch,
    )
    
    # Calculate available width for table (A4 width minus margins)
    page_width = A4[0]
    available_width = page_width - (0.75 * 2 * inch)  # Subtract left and right margins
    
    # Define column widths (split available width between two columns)
    col_widths = [available_width * 0.4, available_width * 0.6]  # 40% and 60% of available width
    
    # Create paragraph style for wrapped text
    text_style = ParagraphStyle(
        name="TableText",
        fontName="Helvetica",
        fontSize=12,
        leading=14,
        alignment=0,  # Left alignment
    )
    
    # Prepare table data with wrapped text
    table_data = []
    
    # Add header row with wrapped text
    header_row = []
    for key in keys:
        header_style = ParagraphStyle(
            name="TableHeader",
            fontName="Helvetica-Bold",
            fontSize=14,
            leading=16,
            alignment=1,  # Center alignment
        )
        header_row.append(Paragraph(str(key), header_style))
    table_data.append(header_row)
    
    # Add data rows with wrapped text
    for item in data:
        row = []
        for key in keys:
            row.append(Paragraph(str(item[key]), text_style))
        table_data.append(row)
    
    # Create table with specified column widths
    table = Table(table_data, colWidths=col_widths)
    
    # Prepare content for PDF
    content = []
    
    # Add title if provided
    if title:
        title_style = ParagraphStyle(
            name="Title",
            fontName="Helvetica-Bold",
            fontSize=18,
            alignment=1,  # Center alignment
            spaceAfter=20,
        )
        title_paragraph = Paragraph(title, title_style)
        content.append(title_paragraph)
    
    # Add table to content
    content.append(table)
    
    # Define table style
    table_style = TableStyle([
        # Header row styling - white background, black text
        ('BACKGROUND', (0, 0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Left align for better text wrapping
        
        # Data rows styling - white background
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        
        # Grid lines
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        
        # Padding
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),  # Top align for better text wrapping
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ])
    
    table.setStyle(table_style)
    
    # Build PDF
    doc.build(content)
    print(f"Table PDF saved as {filename}")


if __name__ == "__main__":
    # Test data for the table function
    test_data = [
        {"Word": "1.abundant", "Definition": "1. existing in large quantities; plentiful"},
        {"Word": "2.benevolent", "Definition": "2. well meaning and kindly"},
        {"Word": "3.cryptic", "Definition": "3. having a meaning that is mysterious or obscure"},
        {"Word": "4.diligent", "Definition": "4. having or showing care and conscientiousness"},
        {"Word": "5.eloquent", "Definition": "5. fluent or persuasive in speaking or writing"},
        {"Word": "6.frugal", "Definition": "6. sparing or economical with regard to money or food"},
        {"Word": "7.gregarious", "Definition": "7. fond of the company of others; sociable"},
        {"Word": "8.humble", "Definition": "8. having or showing a modest or low estimate of one's importance"},
        {"Word": "9.intrepid", "Definition": "9. fearless; adventurous"},
        {"Word": "10.jovial", "Definition": "10. cheerful and friendly"}
    ]
    
    # Test the table function
    print("Testing save_dict_list_to_pdf function...")
    save_dict_list_to_pdf(test_data, "data/vocabulary_table.pdf", "Vocabulary Test - Words and Definitions")
    
    # Test with different data structure
    test_data2 = [
        {"Student": "Alice", "Score": 95},
        {"Student": "Bob", "Score": 87},
        {"Student": "Charlie", "Score": 92},
        {"Student": "Diana", "Score": 78}
    ]
    
    save_dict_list_to_pdf(test_data2, "data/student_scores.pdf", "Student Test Scores")
    print("Test completed! Check the generated PDF files.")



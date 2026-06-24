import html
import re
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    KeepTogether
)
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)
from reportlab.lib import colors

def format_markdown_for_pdf(text):
    """
    Safely escapes text for ReportLab's XML parser and converts basic markdown
    (bolding, bullet points, headers, newlines) into ReportLab-compatible HTML tags.
    This prevents SAXParseException crashes from unescaped characters.
    """
    if not text:
        return ""
        
    # 1. Escape HTML special characters (handles &, <, >, etc. safely)
    escaped_text = html.escape(str(text))
    
    # 2. Convert markdown bold (**text**) to <b>text</b>
    escaped_text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', escaped_text)
    
    # 3. Convert markdown italic (*text*) to <i>text</i>
    escaped_text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', escaped_text)
    
    # 4. Handle headers (lines starting with #)
    lines = escaped_text.split('\n')
    formatted_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('###'):
            formatted_lines.append(f"<font size=11 color='#5b21b6'><b>{stripped[3:].strip()}</b></font>")
        elif stripped.startswith('##'):
            formatted_lines.append(f"<font size=12 color='#4c1d95'><b>{stripped[2:].strip()}</b></font>")
        elif stripped.startswith('#'):
            formatted_lines.append(f"<font size=14 color='#1e3a8a'><b>{stripped[1:].strip()}</b></font>")
        elif stripped.startswith('-') or stripped.startswith('*') or stripped.startswith('•'):
            # Convert list item to bullet format
            item_text = stripped[1:].strip()
            formatted_lines.append(f"&bull; {item_text}")
        else:
            formatted_lines.append(line)
            
    # 5. Join with line breaks
    return "<br/>".join(formatted_lines)

def generate_pdf(filename, results):
    """
    Generates a beautifully styled, crash-proof PDF report using ReportLab.
    """
    # Create the document with standard page size and margins
    doc = SimpleDocTemplate(
        filename,
        rightMargin=54,
        leftMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Define custom styles for a premium professional look
    primary_color = colors.HexColor("#1e3a8a")  # Deep Blue
    secondary_color = colors.HexColor("#4c1d95")  # Deep Violet
    text_color = colors.HexColor("#1f2937")  # Dark Slate
    
    title_style = ParagraphStyle(
        'ReportTitle',
        parent=styles['Title'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=primary_color,
        spaceAfter=15,
        alignment=0  # Left align
    )
    
    subtitle_style = ParagraphStyle(
        'ReportSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#4b5563"),
        spaceAfter=30
    )
    
    section_title_style = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=secondary_color,
        spaceBefore=18,
        spaceAfter=8,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'ReportBody',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=10.5,
        leading=15,
        textColor=text_color,
        spaceAfter=10
    )
    
    story = []
    
    # Title & Subtitle Header
    story.append(Paragraph("InterviewPilot AI — Evaluation Report", title_style))
    story.append(Paragraph("AI-Powered Multi-Agent Resume Analysis & Interview Preparation Roadmap", subtitle_style))
    story.append(Spacer(1, 10))
    
    # Process each section of the report
    for key, content in results.items():
        # Clean and style section headers
        section_name = key.replace("_", " ").title()
        
        # Add section title and body content
        section_header = Paragraph(section_name, section_title_style)
        
        # Format markdown body to ReportLab-safe HTML
        formatted_content = format_markdown_for_pdf(content)
        section_body = Paragraph(formatted_content, body_style)
        
        # Wrap in KeepTogether so headers don't get orphaned at the bottom of a page
        story.append(KeepTogether([
            section_header,
            section_body,
            Spacer(1, 10)
        ]))
        
    doc.build(story)
    return filename
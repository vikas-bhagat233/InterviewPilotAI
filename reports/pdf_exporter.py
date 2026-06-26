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
    (bolding, bullet points, headers, inline code, newlines) into ReportLab-compatible HTML tags.
    This prevents SAXParseException and ValueError crashes from mismatched or unescaped characters.
    """
    if not text:
        return ""
        
    # Split into lines to process structural elements first, preventing interference with inline formatting
    lines = str(text).split('\n')
    formatted_lines = []
    
    for line in lines:
        stripped = line.strip()
        if not stripped:
            formatted_lines.append("")
            continue
            
        # Detect line type (headers and bullet points)
        is_header = False
        is_bullet = False
        header_level = 0
        
        if stripped.startswith('###'):
            is_header = True
            header_level = 3
            content = stripped[3:].strip()
        elif stripped.startswith('##'):
            is_header = True
            header_level = 2
            content = stripped[2:].strip()
        elif stripped.startswith('#'):
            is_header = True
            header_level = 1
            content = stripped[1:].strip()
        elif stripped.startswith('- ') or stripped.startswith('* ') or stripped.startswith('• '):
            is_bullet = True
            content = stripped[2:].strip()
        elif stripped.startswith('-') or stripped.startswith('*') or stripped.startswith('•'):
            # Fallback for bullets without trailing space, or if they are single chars
            if len(stripped) > 1:
                is_bullet = True
                content = stripped[1:].strip()
            else:
                content = line
        else:
            content = line
            
        # 1. Escape HTML special characters in the text content safely
        escaped_content = html.escape(content)
        
        # 2. Convert markdown bold (**text**) to <b>text</b>
        escaped_content = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', escaped_content)
        
        # 3. Convert markdown italic (*text*) to <i>text</i>
        # Make sure it only matches if there's no space immediately inside the asterisks,
        # to avoid matching things like multiplication or single asterisks.
        escaped_content = re.sub(r'\*(?=\S)(.+?)(?<=\S)\*', r'<i>\1</i>', escaped_content)
        
        # 4. Handle inline code backticks (`code`) by converting to Courier font
        escaped_content = re.sub(r'`(.*?)`', r'<font face="Courier">\1</font>', escaped_content)
        
        # Reconstruct the line with its block-level formatting
        if is_header:
            if header_level == 3:
                formatted_lines.append(f"<font size=11 color='#5b21b6'><b>{escaped_content}</b></font>")
            elif header_level == 2:
                formatted_lines.append(f"<font size=12 color='#4c1d95'><b>{escaped_content}</b></font>")
            else:
                formatted_lines.append(f"<font size=14 color='#1e3a8a'><b>{escaped_content}</b></font>")
        elif is_bullet:
            formatted_lines.append(f"&bull; {escaped_content}")
        else:
            formatted_lines.append(escaped_content)
            
    # Join lines with <br/> for ReportLab paragraphs
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
        
        try:
            section_body = Paragraph(formatted_content, body_style)
        except Exception as e:
            # Fallback level 1: Clean out formatting tags (like <b>, <i>, <font>) but keep <br/> and &bull;
            print(f"[WARNING] ReportLab paragraph parsing failed: {e}. Cleaning styling tags and retrying.")
            cleaned_content = re.sub(r'<(?!br\s*/?|/br)[^>]+>', '', formatted_content)
            try:
                section_body = Paragraph(cleaned_content, body_style)
            except Exception as e2:
                # Fallback level 2: Absolute safety fallback with only plain escaped text and line breaks
                print(f"[ERROR] Cleaned ReportLab paragraph parsing also failed: {e2}. Falling back to plain text.")
                plain_text = html.escape(str(content)).replace('\n', '<br/>')
                section_body = Paragraph(plain_text, body_style)
        
        # Wrap in KeepTogether so headers don't get orphaned at the bottom of a page
        story.append(KeepTogether([
            section_header,
            section_body,
            Spacer(1, 10)
        ]))
        
    doc.build(story)
    return filename
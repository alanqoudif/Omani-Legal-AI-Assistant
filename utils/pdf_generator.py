import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO
import tempfile
import arabic_reshaper
from bidi.algorithm import get_display

class PDFGenerator:
    """Class to generate PDF documents"""
    
    def __init__(self, language="English"):
        """
        Initialize the PDF generator.
        
        Args:
            language: Document language (English or Arabic)
        """
        self.language = language
        
        # Set up font for Arabic text if needed
        if language == "Arabic":
            # Try to register Arabic font if available
            try:
                # First check if we already registered the font
                if "Arabic" not in pdfmetrics.getRegisteredFontNames():
                    # Try to find an Arabic font from the system
                    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"  # Common path on Linux
                    if os.path.exists(font_path):
                        pdfmetrics.registerFont(TTFont("Arabic", font_path))
                    else:
                        # Fallback to default font if Arabic font not found
                        print("Arabic font not found, using default font")
            except Exception as e:
                print(f"Error registering Arabic font: {e}")
    
    def generate_legal_document(self, document_title, document_content, author=None):
        """
        Generate a legal document PDF.
        
        Args:
            document_title: Title of the document
            document_content: Content text of the document
            author: Author information (optional)
            
        Returns:
            BytesIO object containing the PDF
        """
        # Create a BytesIO buffer for the PDF
        buffer = BytesIO()
        
        # Create the PDF document
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Get styles
        styles = getSampleStyleSheet()
        
        # Create custom styles for Arabic if needed
        if self.language == "Arabic":
            # Right-to-left paragraph style for Arabic
            rtl_style = ParagraphStyle(
                "RTL",
                parent=styles["Normal"],
                alignment=2,  # Right alignment
                fontName="Arabic" if "Arabic" in pdfmetrics.getRegisteredFontNames() else "Helvetica"
            )
            
            # Right-to-left heading style
            rtl_heading = ParagraphStyle(
                "RTLHeading",
                parent=styles["Heading1"],
                alignment=2,  # Right alignment
                fontName="Arabic" if "Arabic" in pdfmetrics.getRegisteredFontNames() else "Helvetica-Bold",
                fontSize=18
            )
            
            # Process Arabic text with reshaper
            document_title = get_display(arabic_reshaper.reshape(document_title))
            document_content = get_display(arabic_reshaper.reshape(document_content))
            
            title_style = rtl_heading
            content_style = rtl_style
        else:
            # Standard left-to-right styles for English
            title_style = styles["Heading1"]
            content_style = styles["Normal"]
        
        # Create document elements
        elements = []
        
        # Add title
        elements.append(Paragraph(document_title, title_style))
        elements.append(Spacer(1, 12))
        
        # Add author if provided
        if author:
            author_style = content_style
            author_text = f"Prepared by: {author}" if self.language == "English" else f"أعده: {author}"
            if self.language == "Arabic":
                author_text = get_display(arabic_reshaper.reshape(author_text))
            elements.append(Paragraph(author_text, author_style))
            elements.append(Spacer(1, 12))
        
        # Add content
        # Split by newlines and create paragraphs
        for paragraph in document_content.split('\n'):
            if paragraph.strip():
                elements.append(Paragraph(paragraph, content_style))
                elements.append(Spacer(1, 6))
        
        # Build the PDF
        doc.build(elements)
        
        # Get the PDF content
        buffer.seek(0)
        return buffer
    
    def generate_legal_report(self, title, sections):
        """
        Generate a structured legal report PDF.
        
        Args:
            title: Report title
            sections: Dictionary of section titles and their content
            
        Returns:
            BytesIO object containing the PDF
        """
        # Create a BytesIO buffer for the PDF
        buffer = BytesIO()
        
        # Create the PDF document
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Get styles
        styles = getSampleStyleSheet()
        
        # Create custom styles for Arabic if needed
        if self.language == "Arabic":
            # Right-to-left styles for Arabic
            rtl_style = ParagraphStyle(
                "RTL",
                parent=styles["Normal"],
                alignment=2,  # Right alignment
                fontName="Arabic" if "Arabic" in pdfmetrics.getRegisteredFontNames() else "Helvetica"
            )
            
            rtl_heading = ParagraphStyle(
                "RTLHeading",
                parent=styles["Heading1"],
                alignment=2,  # Right alignment
                fontName="Arabic" if "Arabic" in pdfmetrics.getRegisteredFontNames() else "Helvetica-Bold",
                fontSize=18
            )
            
            rtl_subheading = ParagraphStyle(
                "RTLSubHeading",
                parent=styles["Heading2"],
                alignment=2,  # Right alignment
                fontName="Arabic" if "Arabic" in pdfmetrics.getRegisteredFontNames() else "Helvetica-Bold",
                fontSize=14
            )
            
            # Process Arabic text
            title = get_display(arabic_reshaper.reshape(title))
            
            title_style = rtl_heading
            section_title_style = rtl_subheading
            content_style = rtl_style
        else:
            # Standard left-to-right styles for English
            title_style = styles["Heading1"]
            section_title_style = styles["Heading2"]
            content_style = styles["Normal"]
        
        # Create document elements
        elements = []
        
        # Add title
        elements.append(Paragraph(title, title_style))
        elements.append(Spacer(1, 20))
        
        # Add sections
        for section_title, section_content in sections.items():
            # Process Arabic text if needed
            if self.language == "Arabic":
                section_title = get_display(arabic_reshaper.reshape(section_title))
                section_content = get_display(arabic_reshaper.reshape(section_content))
            
            # Add section title
            elements.append(Paragraph(section_title, section_title_style))
            elements.append(Spacer(1, 10))
            
            # Add section content
            # Split by newlines and create paragraphs
            for paragraph in section_content.split('\n'):
                if paragraph.strip():
                    elements.append(Paragraph(paragraph, content_style))
                    elements.append(Spacer(1, 6))
            
            elements.append(Spacer(1, 15))
        
        # Build the PDF
        doc.build(elements)
        
        # Get the PDF content
        buffer.seek(0)
        return buffer

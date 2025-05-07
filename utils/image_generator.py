from PIL import Image, ImageDraw, ImageFont
import io
import os
import base64
import arabic_reshaper
from bidi.algorithm import get_display

class ImageGenerator:
    """Class to create certificate and document images"""
    
    def __init__(self, language="English"):
        """
        Initialize the image generator.
        
        Args:
            language: Document language (English or Arabic)
        """
        self.language = language
        
        # Try to find appropriate fonts
        self.title_font = None
        self.content_font = None
        
        # Common font paths on Linux
        font_paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
        ]
        
        # Find available fonts
        for path in font_paths:
            if os.path.exists(path):
                if "Bold" in path and self.title_font is None:
                    self.title_font = path
                elif "Bold" not in path and self.content_font is None:
                    self.content_font = path
                
                # If we found both fonts, break
                if self.title_font and self.content_font:
                    break
        
        # Fall back to default if no fonts found
        if not self.title_font:
            print("Warning: Could not find title font. Using fallback.")
        if not self.content_font:
            print("Warning: Could not find content font. Using fallback.")
    
    def create_certificate(self, title, recipient_name, date, additional_info=None):
        """
        Create a certificate image.
        
        Args:
            title: Certificate title
            recipient_name: Name of the recipient
            date: Date of issuance
            additional_info: Additional information to include
            
        Returns:
            BytesIO object containing the image
        """
        # Create a blank certificate image (A4 size at 150 DPI)
        width, height = 1240, 1754  # A4 at 150 DPI
        image = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(image)
        
        # Draw border
        border_width = 10
        draw.rectangle(
            [(border_width, border_width), (width - border_width, height - border_width)],
            outline=(28, 77, 146),
            width=border_width
        )
        
        # Draw decorative elements
        draw.rectangle(
            [(0, 0), (width, 100)],
            fill=(28, 77, 146)
        )
        draw.rectangle(
            [(0, height - 100), (width, height)],
            fill=(28, 77, 146)
        )
        
        # Process text for Arabic if needed
        if self.language == "Arabic":
            title = get_display(arabic_reshaper.reshape(title))
            recipient_name = get_display(arabic_reshaper.reshape(recipient_name))
            date = get_display(arabic_reshaper.reshape(date))
            if additional_info:
                additional_info = get_display(arabic_reshaper.reshape(additional_info))
        
        # Load fonts
        try:
            title_font_size = 60
            name_font_size = 72
            content_font_size = 36
            
            # Use found fonts or fall back to default
            title_font_obj = ImageFont.truetype(self.title_font, title_font_size) if self.title_font else ImageFont.load_default()
            name_font_obj = ImageFont.truetype(self.title_font, name_font_size) if self.title_font else ImageFont.load_default()
            content_font_obj = ImageFont.truetype(self.content_font, content_font_size) if self.content_font else ImageFont.load_default()
            
            # Calculate text positions
            title_text_width = draw.textlength(title, font=title_font_obj)
            title_position = ((width - title_text_width) // 2, 200)
            
            name_text_width = draw.textlength(recipient_name, font=name_font_obj)
            name_position = ((width - name_text_width) // 2, height // 2 - 50)
            
            date_text_width = draw.textlength(date, font=content_font_obj)
            date_position = ((width - date_text_width) // 2, height - 200)
            
            # Add text to the image
            draw.text(title_position, title, fill=(28, 77, 146), font=title_font_obj)
            draw.text(name_position, recipient_name, fill=(0, 0, 0), font=name_font_obj)
            draw.text(date_position, date, fill=(0, 0, 0), font=content_font_obj)
            
            # Add additional info if provided
            if additional_info:
                info_position = (100, height // 2 + 100)
                draw.text(info_position, additional_info, fill=(0, 0, 0), font=content_font_obj)
        
        except Exception as e:
            # Fallback to simple text if font rendering fails
            print(f"Error rendering text with fancy fonts: {e}. Using fallback method.")
            draw.text((100, 200), title, fill=(28, 77, 146))
            draw.text((100, height // 2 - 50), recipient_name, fill=(0, 0, 0))
            draw.text((100, height - 200), date, fill=(0, 0, 0))
            if additional_info:
                draw.text((100, height // 2 + 100), additional_info, fill=(0, 0, 0))
        
        # Save the image to a BytesIO object
        image_io = io.BytesIO()
        image.save(image_io, format='PNG')
        image_io.seek(0)
        
        return image_io
    
    def create_document_preview(self, title, content_preview):
        """
        Create a preview image for a document.
        
        Args:
            title: Document title
            content_preview: Short preview of the document content
            
        Returns:
            BytesIO object containing the image
        """
        # Create a blank document image (A4 size at 72 DPI)
        width, height = 595, 842  # A4 at 72 DPI
        image = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(image)
        
        # Draw page outline
        draw.rectangle(
            [(10, 10), (width - 10, height - 10)],
            outline=(200, 200, 200),
            width=1
        )
        
        # Add header
        draw.rectangle(
            [(10, 10), (width - 10, 60)],
            fill=(240, 240, 240)
        )
        
        # Process text for Arabic if needed
        if self.language == "Arabic":
            title = get_display(arabic_reshaper.reshape(title))
            content_preview = get_display(arabic_reshaper.reshape(content_preview))
        
        # Limit content preview length
        max_preview_length = 500
        if len(content_preview) > max_preview_length:
            content_preview = content_preview[:max_preview_length] + "..."
        
        # Load fonts
        try:
            title_font_size = 24
            content_font_size = 12
            
            # Use found fonts or fall back to default
            title_font_obj = ImageFont.truetype(self.title_font, title_font_size) if self.title_font else ImageFont.load_default()
            content_font_obj = ImageFont.truetype(self.content_font, content_font_size) if self.content_font else ImageFont.load_default()
            
            # Add text to the image
            # For RTL language (Arabic), align text to the right
            if self.language == "Arabic":
                title_position = (width - 30, 25)  # Right-aligned
                content_position = (width - 30, 80)  # Right-aligned
                
                # Add text with right alignment
                draw.text(title_position, title, fill=(0, 0, 0), font=title_font_obj, anchor="ra")
                
                # Wrap and draw content text
                y_position = 80
                max_width = width - 60
                words = content_preview.split()
                line = ""
                
                for word in words:
                    test_line = line + " " + word if line else word
                    test_line_width = draw.textlength(test_line, font=content_font_obj)
                    
                    if test_line_width <= max_width:
                        line = test_line
                    else:
                        draw.text((width - 30, y_position), line, fill=(0, 0, 0), font=content_font_obj, anchor="ra")
                        y_position += content_font_size + 4
                        line = word
                
                if line:
                    draw.text((width - 30, y_position), line, fill=(0, 0, 0), font=content_font_obj, anchor="ra")
            else:
                # For LTR language (English), align text to the left
                title_position = (30, 25)
                content_position = (30, 80)
                
                # Add title
                draw.text(title_position, title, fill=(0, 0, 0), font=title_font_obj)
                
                # Wrap and draw content text
                y_position = 80
                max_width = width - 60
                words = content_preview.split()
                line = ""
                
                for word in words:
                    test_line = line + " " + word if line else word
                    test_line_width = draw.textlength(test_line, font=content_font_obj)
                    
                    if test_line_width <= max_width:
                        line = test_line
                    else:
                        draw.text(content_position, line, fill=(0, 0, 0), font=content_font_obj)
                        y_position += content_font_size + 4
                        content_position = (30, y_position)
                        line = word
                
                if line:
                    draw.text(content_position, line, fill=(0, 0, 0), font=content_font_obj)
        
        except Exception as e:
            # Fallback to simple text if font rendering fails
            print(f"Error rendering text with fancy fonts: {e}. Using fallback method.")
            draw.text((30, 25), title, fill=(0, 0, 0))
            draw.text((30, 80), content_preview[:100] + "...", fill=(0, 0, 0))
        
        # Add footer with page number
        draw.line([(30, height - 50), (width - 30, height - 50)], fill=(200, 200, 200), width=1)
        page_text = "Page 1" if self.language == "English" else "١ صفحة"
        draw.text((width // 2, height - 30), page_text, fill=(150, 150, 150))
        
        # Save the image to a BytesIO object
        image_io = io.BytesIO()
        image.save(image_io, format='PNG')
        image_io.seek(0)
        
        return image_io
    
    def image_to_base64(self, image_io):
        """
        Convert an image BytesIO to base64 for embedding in HTML.
        
        Args:
            image_io: BytesIO object containing the image
            
        Returns:
            Base64 encoded string
        """
        image_io.seek(0)
        image_data = image_io.read()
        encoded = base64.b64encode(image_data).decode('utf-8')
        return encoded

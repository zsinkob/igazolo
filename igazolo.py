#!/usr/bin/env python3
"""
Igazolas Image Date Replacement Tool
Replaces dates in igazolas.jpg with handwritten-style text.
"""

from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import sys
import os


def generate_handwritten_text(draw, text, position, font_size=80):
    """
    Generate handwritten-style text on the image.
    
    Args:
        draw: PIL ImageDraw object
        text: Text to write
        position: Tuple of (x1, y1, x2, y2) coordinates for text box
        font_size: Font size for the text
    """
    x1, y1, x2, y2 = position
    
    # Try to load a handwriting-style font, fallback to default
    try:
        # Try common handwriting fonts
        font_paths = [
            "C:/Windows/Fonts/segoepr.ttf",  # Segoe Print (handwriting-like)
            "C:/Windows/Fonts/Inkfree.ttf",  # Ink Free
            "C:/Windows/Fonts/BRUSHSCI.TTF", # Brush Script
            "arial.ttf",
        ]
        
        font = None
        for font_path in font_paths:
            try:
                font = ImageFont.truetype(font_path, font_size)
                break
            except:
                continue
        
        if font is None:
            font = ImageFont.load_default()
    except:
        font = ImageFont.load_default()
    
    # Calculate text position (left-aligned in the box)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Left-align horizontally, bottom-align vertically
    x = x1 + 15  # Padding from left edge
    y = y2 - text_height - bbox[1] - 5  # Align to bottom with small padding
    
    # Draw text in blue ink color to match typical handwritten documents
    # Using a dark blue that matches common pen ink
    draw.text((x, y), text, fill=(0, 0, 139), font=font)


def process_igazolas(from_date_str, to_date_str=None):
    """
    Process the igazolas image with the provided dates.
    
    Args:
        from_date_str: From date string in format YYYY-MM-DD or YYYY.MM.DD
        to_date_str: To date string (optional). If not provided, uses from_date_str
    """
    # If to_date not provided, use from_date for both
    if to_date_str is None:
        to_date_str = from_date_str
    
    # Load the input image
    input_file = "igazolas.jpg"
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found in current directory")
        sys.exit(1)
    
    image = Image.open(input_file)
    
    # Parse from date
    try:
        if '.' in from_date_str:
            from_date = datetime.strptime(from_date_str, "%Y.%m.%d")
        else:
            from_date = datetime.strptime(from_date_str, "%Y-%m-%d")
    except ValueError:
        print(f"Error: Invalid from date format '{from_date_str}'. Use YYYY-MM-DD or YYYY.MM.DD")
        sys.exit(1)
    
    # Parse to date
    try:
        if '.' in to_date_str:
            to_date = datetime.strptime(to_date_str, "%Y.%m.%d")
        else:
            to_date = datetime.strptime(to_date_str, "%Y-%m-%d")
    except ValueError:
        print(f"Error: Invalid to date format '{to_date_str}'. Use YYYY-MM-DD or YYYY.MM.DD")
        sys.exit(1)
    
    # Format dates with short year format (25 instead of 2025)
    from_date_formatted = from_date.strftime("%y.%m.%d")
    to_date_formatted = to_date.strftime("%y.%m.%d")
    current_date = datetime.now()
    current_date_formatted = current_date.strftime("%y.%m.%d")
    
    # Define positions for date replacements
    positions = {
        'from_date': (1347, 750, 1966, 864),
        'to_date': (2386, 759, 2934, 862),
        'current_date': (921, 1385, 1685, 1505),
    }
    
    # Draw dates
    draw = ImageDraw.Draw(image)
    
    # Add from date and to date to first two positions
    generate_handwritten_text(draw, from_date_formatted, positions['from_date'], font_size=100)
    generate_handwritten_text(draw, to_date_formatted, positions['to_date'], font_size=100)
    
    # Add current date to the third position
    generate_handwritten_text(draw, current_date_formatted, positions['current_date'], font_size=100)
    
    # Generate output filename using the to date
    output_filename = f"igazolas_{to_date.month}_{to_date.day}.jpg"
    
    # Save the image
    image.save(output_filename, "JPEG", quality=95)
    print(f"Successfully created: {output_filename}")
    print(f"From date: {from_date_formatted}")
    print(f"To date: {to_date_formatted}")
    print(f"Current date: {current_date_formatted}")


def main():
    """Main entry point."""
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python igazolo.py <from_date> [to_date]")
        print("Date format: YYYY-MM-DD or YYYY.MM.DD")
        print("Examples:")
        print("  python igazolo.py 2025-12-01              # Uses same date for both")
        print("  python igazolo.py 2025-12-01 2025-12-05  # Different from/to dates")
        sys.exit(1)
    
    from_date = sys.argv[1]
    to_date = sys.argv[2] if len(sys.argv) == 3 else None
    process_igazolas(from_date, to_date)


if __name__ == "__main__":
    main()

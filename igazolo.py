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


def clear_region(image, position):
    """
    Clear a region by sampling and filling with the surrounding background color.
    
    Args:
        image: PIL Image object
        position: Tuple of (x1, y1, x2, y2) coordinates
    """
    x1, y1, x2, y2 = position
    
    # Sample background colors from multiple points around the region perimeter
    sample_points = []
    
    # Sample from outside the box on all four sides
    offset = 10
    # Top edge samples
    for i in range(5):
        x = x1 + (x2 - x1) * i // 4
        sample_points.append((x, y1 - offset))
    # Bottom edge samples
    for i in range(5):
        x = x1 + (x2 - x1) * i // 4
        sample_points.append((x, y2 + offset))
    # Left edge samples
    for i in range(3):
        y = y1 + (y2 - y1) * i // 2
        sample_points.append((x1 - offset, y))
    # Right edge samples
    for i in range(3):
        y = y1 + (y2 - y1) * i // 2
        sample_points.append((x2 + offset, y))
    
    # Collect valid samples
    colors = []
    for x, y in sample_points:
        if 0 <= x < image.width and 0 <= y < image.height:
            try:
                colors.append(image.getpixel((x, y)))
            except:
                pass
    
    # Calculate average color or fallback to light gray
    if colors:
        avg_color = tuple(sum(c[i] for c in colors) // len(colors) for i in range(3))
    else:
        avg_color = (240, 240, 240)  # Light gray fallback
    
    draw = ImageDraw.Draw(image)
    draw.rectangle(position, fill=avg_color)


def process_igazolas(input_date_str):
    """
    Process the igazolas image with the provided dates.
    
    Args:
        input_date_str: Date string in format YYYY-MM-DD or YYYY.MM.DD
    """
    # Load the input image
    input_file = "igazolas.jpg"
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found in current directory")
        sys.exit(1)
    
    image = Image.open(input_file)
    
    # Parse input date
    try:
        if '.' in input_date_str:
            input_date = datetime.strptime(input_date_str, "%Y.%m.%d")
        else:
            input_date = datetime.strptime(input_date_str, "%Y-%m-%d")
    except ValueError:
        print(f"Error: Invalid date format '{input_date_str}'. Use YYYY-MM-DD or YYYY.MM.DD")
        sys.exit(1)
    
    # Format dates with short year format (25 instead of 2025)
    input_date_formatted = input_date.strftime("%y.%m.%d")
    current_date = datetime.now()
    current_date_formatted = current_date.strftime("%y.%m.%d")
    
    # Define positions for date replacements
    positions = {
        'input_date_1': (1347, 750, 1966, 864),
        'input_date_2': (2386, 759, 2934, 862),
        'current_date': (921, 1385, 1685, 1505),
    }
    
    # Clear regions
    for position in positions.values():
        clear_region(image, position)
    
    # Draw dates
    draw = ImageDraw.Draw(image)
    
    # Add input date to first two positions
    generate_handwritten_text(draw, input_date_formatted, positions['input_date_1'], font_size=100)
    generate_handwritten_text(draw, input_date_formatted, positions['input_date_2'], font_size=100)
    
    # Add current date to the third position
    generate_handwritten_text(draw, current_date_formatted, positions['current_date'], font_size=100)
    
    # Generate output filename
    output_filename = f"igazolas_{current_date.month}_{current_date.day}.jpg"
    
    # Save the image
    image.save(output_filename, "JPEG", quality=95)
    print(f"Successfully created: {output_filename}")
    print(f"Input date used: {input_date_formatted}")
    print(f"Current date used: {current_date_formatted}")


def main():
    """Main entry point."""
    if len(sys.argv) != 2:
        print("Usage: python igazolo.py <date>")
        print("Date format: YYYY-MM-DD or YYYY.MM.DD")
        print("Example: python igazolo.py 2025-12-01")
        sys.exit(1)
    
    input_date = sys.argv[1]
    process_igazolas(input_date)


if __name__ == "__main__":
    main()

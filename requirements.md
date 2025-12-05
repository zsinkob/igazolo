# Igazolas Date Replacement Application Requirements

## Overview
Build a Python application that replaces dates in `igazolas.jpg` with handwritten-style text.

## Input Parameters
- **From Date**: Start date (required)
- **To Date**: End date (optional - if not provided, uses the from date for both positions)
- Date format: `YYYY-MM-DD` or `YYYY.MM.DD`

## Date Placement Requirements

### Position 1: From Date
- **Location**: 1347x750 to 1966x864
- **Content**: User-provided from date
- **Format**: YY.MM.DD (e.g., 25.12.01)
- **Style**: Handwritten font

### Position 2: To Date
- **Location**: 2386x759 to 2934x862
- **Content**: User-provided to date (or from date if not specified)
- **Format**: YY.MM.DD (e.g., 25.12.05)
- **Style**: Handwritten font

### Position 3: Current Date
- **Location**: 921x1403 to 1685x1505
- **Content**: Today's date (auto-generated)
- **Format**: YY.MM.DD (e.g., 25.12.05)
- **Style**: Handwritten font

## Text Formatting
- **Year Format**: Short year only (25 instead of 2025)
- **Font**: Handwritten-style font (Segoe Print, Ink Free, or Brush Script preferred)
- **Font Size**: 100pt
- **Horizontal Alignment**: Left-aligned within bounding box (15px padding from left edge)
- **Vertical Alignment**: Bottom-aligned within bounding box (5px padding from bottom edge)
- **Ink Color**: Dark blue (RGB: 0, 0, 139) to match typical handwritten document ink

## Output File
- **Filename Format**: `igazolas_{end_month}_{end_day}.jpg`
- **Example**: `igazolas_12_5.jpg` (for end date December 5)
- **Quality**: JPEG quality 95
- **Location**: Same directory as input file

## Technical Requirements
- **Image Library**: Pillow (PIL) for image manipulation and text rendering
- **Base Image**: Pre-processed `igazolas.jpg` with blank regions for date placement
- **Python Version**: 3.7+

## Usage Examples
```bash
# Single date (used for both from and to)
python igazolo.py 2025-12-01

# Different from and to dates
python igazolo.py 2025-12-01 2025-12-05

# Alternative date format
python igazolo.py 2025.12.01 2025.12.05
```

## Dependencies
- Pillow >= 10.0.0
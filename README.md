# Igazolas Date Replacement Tool

A Python application that replaces dates in `igazolas.jpg` with handwritten-style text.

## Requirements

- Python 3.7+
- Pillow (PIL) library

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the script with a date parameter:

```bash
python igazolo.py <date>
```

### Date Format

The date should be provided in one of these formats:
- `YYYY-MM-DD` (e.g., `2025-12-05`)
- `YYYY.MM.DD` (e.g., `2025.12.05`)

### Example

```bash
python igazolo.py 2025-12-01
```

## What It Does

The application:

1. Reads `igazolas.jpg` from the current directory
2. Replaces dates in three specific regions:
   - **Position 1** (1347x750 to 1966x855): Input date
   - **Position 2** (2386x759 to 2934x847): Input date
   - **Position 3** (921x1403 to 1685x1495): Current date
3. Uses handwriting-style fonts (Segoe Print, Ink Free, or similar)
4. Saves the result as `igazolas_{month}_{day}.jpg` (e.g., `igazolas_12_5.jpg`)

## Notes

- The original `igazolas.jpg` file must be present in the same directory
- The output filename uses the current date (not the input date)
- Dates are formatted as `YY.MM.DD` in the image (e.g., `25.12.05` for December 5, 2025)
- Background color is sampled from surrounding areas for seamless blending
- Text uses dark blue ink color to match typical handwritten documents

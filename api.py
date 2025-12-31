#!/usr/bin/env python3
"""
REST API for Igazolas Image Date Replacement Tool
Exposes the image generation as a GET endpoint.
"""

from flask import Flask, request, send_file, jsonify
import os
import io

# Import the core functionality from igazolo.py
from igazolo import generate_igazolas_image

app = Flask(__name__)


@app.route('/generate', methods=['GET'])
def generate_igazolas_endpoint():
    """
    Generate igazolas image with dates from query parameters.
    
    Query Parameters:
        from_date: Required. From date in YYYY-MM-DD or YYYY.MM.DD format
        to_date: Optional. To date in YYYY-MM-DD or YYYY.MM.DD format
    
    Returns:
        JPEG image file
    
    Example:
        GET /generate?from_date=2025-12-01&to_date=2025-12-05
        GET /generate?from_date=2025-12-01
    """
    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')
    
    if not from_date:
        return jsonify({
            'error': 'Missing required parameter: from_date',
            'usage': 'GET /generate?from_date=YYYY-MM-DD&to_date=YYYY-MM-DD',
            'example': 'GET /generate?from_date=2025-12-01&to_date=2025-12-05'
        }), 400
    
    # Use the function from igazolo.py
    image, filename, _, _, error = generate_igazolas_image(from_date, to_date)
    
    if error:
        return jsonify({'error': error}), 400
    
    # Convert image to bytes
    img_io = io.BytesIO()
    image.save(img_io, "JPEG", quality=95)
    img_io.seek(0)
    
    return send_file(
        img_io,
        mimetype='image/jpeg',
        as_attachment=True,
        download_name=filename
    )


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'igazolas-api'
    })


@app.route('/', methods=['GET'])
def index():
    """API documentation."""
    return jsonify({
        'service': 'Igazolas Image Generator API',
        'endpoints': {
            '/generate': {
                'method': 'GET',
                'description': 'Generate igazolas image with dates',
                'parameters': {
                    'from_date': {
                        'required': True,
                        'format': 'YYYY-MM-DD or YYYY.MM.DD',
                        'description': 'Start date for the certificate'
                    },
                    'to_date': {
                        'required': False,
                        'format': 'YYYY-MM-DD or YYYY.MM.DD',
                        'description': 'End date for the certificate (defaults to from_date)'
                    }
                },
                'examples': [
                    '/generate?from_date=2025-12-01',
                    '/generate?from_date=2025-12-01&to_date=2025-12-05',
                    '/generate?from_date=2025.12.01&to_date=2025.12.05'
                ]
            },
            '/health': {
                'method': 'GET',
                'description': 'Health check endpoint'
            }
        }
    })


if __name__ == '__main__':
    # Check if igazolas.jpg exists
    if not os.path.exists('igazolas.jpg'):
        print("Warning: igazolas.jpg not found in current directory")
        print("The API will return errors until the template image is available")
    
    # Run the Flask app
    print("Starting Igazolas API server...")
    print("API documentation available at: http://localhost:5001/")
    print("Generate endpoint: http://localhost:5001/generate?from_date=2025-12-01&to_date=2025-12-05")
    app.run(debug=True, host='0.0.0.0', port=5001)

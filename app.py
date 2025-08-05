#!/usr/bin/env python3
"""
Flask Web Application for Box Processing
Uses only the existing functions from process_boxes.py without duplicating logic
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
import tempfile
import pandas as pd
from werkzeug.utils import secure_filename
from pathlib import Path
import base64

# Import from process_boxes.py - using existing functions only
from process_boxes import process_images, download_image_as_base64

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Create uploads directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Check if the file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_single_box_via_csv(image_url: str, height: float, weight: float, breadth: float, image_id: str = "1") -> dict:
    """
    Process a single box by creating a temporary CSV and using the existing process_images function
    This ensures we use the exact same logic as the original script
    """
    # Create a temporary CSV file with the single box data
    temp_data = {
        'image_id': [image_id],
        'image_url': [image_url], 
        'height': [height],
        'weight': [weight],
        'breadth': [breadth]
    }
    
    df = pd.DataFrame(temp_data)
    
    # Create temporary CSV file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as temp_file:
        df.to_csv(temp_file.name, index=False)
        temp_csv_path = temp_file.name
    
    try:
        # Use the existing process_images function from process_boxes.py
        result = process_images(temp_csv_path)
        
        # Extract the single result
        if result['data']:
            return result['data'][0]
        else:
            raise ValueError("No data processed")
            
    finally:
        # Clean up temporary file
        if os.path.exists(temp_csv_path):
            os.unlink(temp_csv_path)

def get_image_as_base64_from_file(file_path: str) -> str:
    """Convert uploaded file to base64 using similar logic as download_image_as_base64"""
    try:
        with open(file_path, 'rb') as f:
            image_content = f.read()
        
        # Determine content type from file extension
        ext = Path(file_path).suffix.lower()
        content_type_map = {
            '.png': 'image/png',
            '.jpg': 'image/jpeg', 
            '.jpeg': 'image/jpeg',
            '.gif': 'image/gif'
        }
        content_type = content_type_map.get(ext, 'image/jpeg')
        
        # Convert to base64
        image_base64 = base64.b64encode(image_content).decode('utf-8')
        return f"data:{content_type};base64,{image_base64}"
        
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return ""

@app.route('/')
def index():
    """Main page with the form"""
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_box():
    """Process the box data using existing process_boxes.py functions"""
    try:
        # Get form data
        height = float(request.form.get('height', 0))
        weight = float(request.form.get('weight', 0))
        breadth = float(request.form.get('breadth', 0))
        image_url = request.form.get('image_url', '').strip()
        
        # Validate dimensions
        if height <= 0 or weight <= 0 or breadth <= 0:
            flash('All dimensions must be positive numbers', 'error')
            return redirect(url_for('index'))
        
        # Handle image input - either URL or file upload
        final_image_url = ""
        
        if 'image_file' in request.files and request.files['image_file'].filename:
            # File upload case
            file = request.files['image_file']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                # For file uploads, we need to create a temporary URL
                # Since process_images expects URLs, we'll use a local file path
                final_image_url = f"file://{os.path.abspath(filepath)}"
            else:
                flash('Invalid file type. Please upload PNG, JPG, JPEG, or GIF files', 'error')
                return redirect(url_for('index'))
        elif image_url:
            # URL case
            final_image_url = image_url
        else:
            flash('Please provide either an image URL or upload an image file', 'error')
            return redirect(url_for('index'))
        
        # Process using existing function from process_boxes.py
        result = process_single_box_via_csv(final_image_url, height, weight, breadth)
        
        # If it's a file upload and image_base64 is empty, get it from the file
        if final_image_url.startswith('file://') and not result.get('image_base64'):
            file_path = final_image_url.replace('file://', '')
            result['image_base64'] = get_image_as_base64_from_file(file_path)
        
        return render_template('results.html', result=result)
        
    except ValueError as e:
        flash('Please enter valid numeric values for dimensions', 'error')
        return redirect(url_for('index'))
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/batch')
def batch_processing():
    """Batch processing page"""
    return render_template('batch.html')

@app.route('/batch/upload', methods=['POST'])
def batch_upload():
    """Handle batch CSV upload using existing process_images function"""
    try:
        if 'csv_file' not in request.files:
            flash('No CSV file uploaded', 'error')
            return redirect(url_for('batch_processing'))
        
        file = request.files['csv_file']
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(url_for('batch_processing'))
        
        if file and file.filename and file.filename.endswith('.csv'):
            # Save uploaded file
            filename = secure_filename(file.filename)
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(upload_path)
            
            # Use existing process_images function directly
            results = process_images(upload_path)
            
            return render_template('batch_results.html', 
                                 results=results['data'],
                                 processing_times=results['processing_times'])
        else:
            flash('Please upload a valid CSV file', 'error')
            return redirect(url_for('batch_processing'))
            
    except Exception as e:
        flash(f'Error processing batch file: {str(e)}', 'error')
        return redirect(url_for('batch_processing'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

#!/usr/bin/env python3
"""
Box Processing Demo Script
Processes a CSV file containing box dimensions and generates:
1. A new CSV file with calculated surface area and capacity
2. A markdown file with images, calculations, and processing statistics
"""

import pandas as pd
import time
import random
from typing import List, Dict
import requests
from pathlib import Path
import base64

from utils.math_utils import calculate_capacity, calculate_surface_area, generate_timing_statistics
from utils.report_utils import generate_csv_output, generate_markdown_output

def download_image_as_base64(url: str) -> str:
    """Download image from URL and convert to base64 for embedding in markdown"""
    try:
        # Handle local file URLs
        if url.startswith('file://'):
            file_path = url.replace('file://', '')
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
        
        # Handle HTTP/HTTPS URLs
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Get the image content type
        content_type = response.headers.get('content-type', 'image/jpeg')
        
        # Convert to base64
        image_base64 = base64.b64encode(response.content).decode('utf-8')
        
        return f"data:{content_type};base64,{image_base64}"
    except Exception as e:
        print(f"Error downloading image from {url}: {e}")
        return ""


def process_images(input_csv: str) -> Dict:
    """Process the CSV file and return processed data with timing information"""
    
    # Read the CSV file
    df = pd.read_csv(input_csv)
    
    # Initialize lists to store results
    processed_data = []
    processing_times = []
    
    print(f"Processing {len(df)} images...")
    
    for index, row in df.iterrows():
        start_time = time.time()
        
        # Extract data
        image_id = row['image_id']
        image_url = row['image_url']
        height = row['height']
        weight = row['weight']
        breadth = row['breadth']
        
        # Calculate surface area and capacity
        surface_area = calculate_surface_area(height, weight, breadth)
        capacity = calculate_capacity(height, weight, breadth)
        
        # Add random processing delay (max 2 seconds)
        processing_delay = random.uniform(0.1, 2.0)
        time.sleep(processing_delay)
        
        # Download image as base64 for markdown
        image_base64 = download_image_as_base64(image_url)
        
        end_time = time.time()
        processing_time = end_time - start_time
        processing_times.append(processing_time)
        
        # Store processed data
        processed_data.append({
            'image_id': image_id,
            'image_url': image_url,
            'height': height,
            'weight': weight,
            'breadth': breadth,
            'surface_area': surface_area,
            'capacity': capacity,
            'processing_time': processing_time,
            'image_base64': image_base64
        })
        
        print(f"Processed image {image_id} in {processing_time:.2f} seconds")
    
    return {
        'data': processed_data,
        'processing_times': processing_times
    }



def main():
    """Main function to orchestrate the processing"""
    
    # Input and output file paths
    input_csv = "input/testbed.csv"
    output_csv = "output/processed_boxes.csv"
    output_markdown = "output/box_processing_report.md"
    
    # Check if input file exists
    if not Path(input_csv).exists():
        print(f"Error: Input file '{input_csv}' not found!")
        return
    
    print("=" * 50)
    print("Box Processing Demo Script")
    print("=" * 50)
    
    # Process the images
    start_total = time.time()
    results = process_images(input_csv)
    end_total = time.time()
    
    # Calculate timing statistics
    timing_stats = generate_timing_statistics(results['processing_times'])
    
    print(f"\nTotal processing time: {end_total - start_total:.2f} seconds")
    
    # Generate output files
    generate_csv_output(results['data'], output_csv)
    generate_markdown_output(results['data'], timing_stats, output_markdown)
    
    print("\n" + "=" * 50)
    print("Processing completed successfully!")
    print(f"Generated files:")
    print(f"  - {output_csv}")
    print(f"  - {output_markdown}")
    print("=" * 50)


if __name__ == "__main__":
    main()

from typing import List, Dict
import pandas as pd

def generate_csv_output(processed_data: List[Dict], output_file: str):
    """Generate CSV output file with calculated values"""
    
    # Prepare data for CSV (exclude base64 image data)
    csv_data = []
    for item in processed_data:
        csv_data.append({
            'image_id': item['image_id'],
            'image_url': item['image_url'],
            'height': item['height'],
            'weight': item['weight'],
            'breadth': item['breadth'],
            'surface_area': round(item['surface_area'], 2),
            'capacity': round(item['capacity'], 2),
            'processing_time': round(item['processing_time'], 3)
        })
    
    # Create DataFrame and save to CSV
    df = pd.DataFrame(csv_data)
    df.to_csv(output_file, index=False)
    print(f"CSV output saved to: {output_file}")


def generate_markdown_output(processed_data: List[Dict], timing_stats: Dict, output_file: str):
    """Generate markdown output file with images, data, and timing statistics"""
    
    markdown_content = []
    
    # Header
    markdown_content.append("# Box Processing Results")
    markdown_content.append("")
    markdown_content.append("This report contains the processing results for box dimensions, including surface area and capacity calculations.")
    markdown_content.append("")
    
    # Main data table
    markdown_content.append("## Box Data and Images")
    markdown_content.append("")
    markdown_content.append("| Image ID | Image | Surface Area (sq units) | Capacity (cubic units) | Processing Time (s) |")
    markdown_content.append("|----------|-------|--------------------------|-------------------------|---------------------|")
    
    for item in processed_data:
        image_display = ""
        if item['image_base64']:
            image_display = f'<img src="{item["image_base64"]}" alt="Box {item["image_id"]}" width="150" height="auto">'
        else:
            image_display = f"[Image]({item['image_url']})"
        
        markdown_content.append(
            f"| {item['image_id']} | {image_display} | {item['surface_area']:.2f} | "
            f"{item['capacity']:.2f} | {item['processing_time']:.3f} |"
        )
    
    markdown_content.append("")
    
    # Timing statistics
    markdown_content.append("## Processing Time Statistics")
    markdown_content.append("")
    
    if timing_stats:
        markdown_content.append("| Metric | Value (seconds) |")
        markdown_content.append("|--------|-----------------|")
        markdown_content.append(f"| Count | {timing_stats['count']} |")
        markdown_content.append(f"| Average | {timing_stats['average']:.3f} |")
        markdown_content.append(f"| Median | {timing_stats['median']:.3f} |")
        markdown_content.append(f"| Minimum | {timing_stats['min']:.3f} |")
        markdown_content.append(f"| Maximum | {timing_stats['max']:.3f} |")
        markdown_content.append(f"| Standard Deviation | {timing_stats['std_dev']:.3f} |")
        markdown_content.append(f"| 90th Percentile (P90) | {timing_stats['p90']:.3f} |")
        markdown_content.append(f"| 99th Percentile (P99) | {timing_stats['p99']:.3f} |")
    
    markdown_content.append("")
    
    # Box details section
    markdown_content.append("## Detailed Box Information")
    markdown_content.append("")
    
    for item in processed_data:
        markdown_content.append(f"### Box {item['image_id']}")
        markdown_content.append("")
        markdown_content.append(f"- **Image URL**: {item['image_url']}")
        markdown_content.append(f"- **Dimensions**: {item['height']} × {item['weight']} × {item['breadth']}")
        markdown_content.append(f"- **Surface Area**: {item['surface_area']:.2f} square units")
        markdown_content.append(f"- **Capacity**: {item['capacity']:.2f} cubic units")
        markdown_content.append(f"- **Processing Time**: {item['processing_time']:.3f} seconds")
        markdown_content.append("")
    
    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(markdown_content))
    
    print(f"Markdown output saved to: {output_file}")

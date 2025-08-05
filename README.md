# Box Processing Tool

A Python application for processing box dimensions and calculating surface area and capacity. The tool supports both command-line interface (CLI) and web-based user interface (UI) modes.

## Features

- **Surface Area Calculation**: Calculates total surface area using the formula `2(lw + lh + wh)`
- **Capacity Calculation**: Calculates volume using the formula `l × w × h`
- **Image Processing**: Downloads and processes box images for visualization
- **Batch Processing**: Process multiple boxes from CSV files
- **Report Generation**: Creates CSV and Markdown reports with processing statistics
- **Web Interface**: User-friendly web UI for single box and batch processing
- **Processing Statistics**: Detailed timing and performance metrics

## Project Structure

```
├── process_boxes.py          # Main CLI script
├── app.py                   # Flask web application
├── requirements.txt         # Python dependencies
├── input/
│   ├── testbed.csv         # Sample input data
│   └── images/             # Sample images
├── output/                 # Generated reports (created automatically)
├── uploads/               # Uploaded files (created automatically)
├── utils/
│   ├── math_utils.py      # Mathematical calculations
│   └── report_utils.py    # Report generation utilities
└── templates/             # HTML templates for web UI
    ├── base.html
    ├── index.html
    ├── results.html
    ├── batch.html
    └── batch_results.html
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd copilot-use-case-101-enhanced
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation**:
   ```bash
   python3 --version
   pip list | grep -E "(pandas|numpy|requests|flask)"
   ```

## Usage

### Command Line Interface (CLI)

#### Running the Original Script

Process the sample data using the CLI:

```bash
# Run with default input (input/testbed.csv)
python3 process_boxes.py
```

The script will:
- Read data from `input/testbed.csv`
- Process each box (calculate surface area and capacity)
- Download images and convert to base64
- Generate reports in `output/` directory:
  - `processed_boxes.csv`: Tabular results
  - `box_processing_report.md`: Detailed report with images

#### Sample Output
```
==================================================
Box Processing Demo Script
==================================================
Processing 3 images...
Processed image 1 in 1.23 seconds
Processed image 2 in 0.87 seconds
Processed image 3 in 1.45 seconds

Total processing time: 3.55 seconds
CSV output saved to: output/processed_boxes.csv
Markdown output saved to: output/box_processing_report.md

==================================================
Processing completed successfully!
Generated files:
  - output/processed_boxes.csv
  - output/box_processing_report.md
==================================================
```

### Web User Interface (UI)

#### Starting the Web Application

1. **Start the Flask server**:
   ```bash
   python3 app.py
   ```

2. **Access the web interface**:
   - Open your browser and go to: `http://localhost:5000`
   - Or use the network URL shown in the terminal (e.g., `http://192.168.1.x:5000`)

#### Web UI Features

**Single Box Processing**:
- Navigate to the home page (`http://localhost:5000`)
- Enter box dimensions (height, length/weight, width/breadth)
- Provide image URL or upload an image file
- Click "Process Box" to get results
- View calculated surface area, capacity, and processing time
- Download results as JSON or text

**Batch Processing**:
- Click "Batch Processing" in the navigation
- Upload a CSV file with the same format as `input/testbed.csv`
- View comprehensive results for all boxes
- Download batch summary

**Example Data**:
- Use the "Try with Example Data" buttons to quickly test with sample data
- Examples use the same data as in `input/testbed.csv`

## Input Data Format

### CSV Structure

Your CSV file should have the following columns:

| Column Name | Description | Example |
|-------------|-------------|---------|
| `image_id` | Unique identifier | 1, 2, 3... |
| `image_url` | Image URL | https://example.com/box1.jpg |
| `height` | Box height | 600 |
| `weight` | Box length | 400 |
| `breadth` | Box width | 300 |

### Sample CSV Content

```csv
image_id,image_url,height,weight,breadth
1,https://raw.githubusercontent.com/shresthjain-bs/public/main/copilot_demo/box1.jpeg,600,400,300
2,https://raw.githubusercontent.com/shresthjain-bs/public/main/copilot_demo/box2.png,800,600,400
3,https://raw.githubusercontent.com/shresthjain-bs/public/main/copilot_demo/box3.jpeg,1024,768,512
```

## Output

### CLI Output Files

1. **processed_boxes.csv**: Tabular data with calculated values
   ```csv
   image_id,image_url,height,weight,breadth,surface_area,capacity,processing_time
   1,https://...,600,400,300,660000.00,72000000.00,1.234
   ```

2. **box_processing_report.md**: Comprehensive markdown report with:
   - Images embedded as base64
   - Calculation results
   - Processing statistics
   - Detailed box information

### Web UI Output

- **Interactive Results**: View results directly in the browser
- **Download Options**: Export as JSON or text format
- **Batch Summaries**: Comprehensive statistics for multiple boxes

## Formulas Used

- **Surface Area**: `2 × (length×width + length×height + width×height)`
- **Capacity (Volume)**: `length × width × height`

## Technical Details

### Architecture

The web application maintains complete consistency with the CLI script by:
- Using the same `process_images()` function from `process_boxes.py`
- Creating temporary CSV files for single box processing
- Calling identical utility functions for calculations
- Ensuring any changes to the CLI script automatically apply to the web UI

### Dependencies

- **pandas**: Data manipulation and CSV processing
- **numpy**: Statistical calculations
- **requests**: HTTP requests for image downloads
- **flask**: Web framework
- **werkzeug**: File upload handling

### Processing Features

- Random processing delays (0.1-2.0 seconds per box) to simulate real-world processing
- Image download and base64 conversion for embedding
- Comprehensive timing statistics (average, median, percentiles)
- Error handling for network issues and invalid data

## Development

### Running in Development Mode

```bash
# CLI development
python3 process_boxes.py

# Web UI development (with auto-reload)
export FLASK_ENV=development
python3 app.py
```

### Adding New Features

The modular architecture allows easy extension:
- **Math functions**: Add to `utils/math_utils.py`
- **Report formats**: Extend `utils/report_utils.py`
- **Web routes**: Add to `app.py`
- **Templates**: Create new HTML files in `templates/`

## Troubleshooting

### Common Issues

1. **Module not found**: Ensure all dependencies are installed
   ```bash
   pip install -r requirements.txt
   ```

2. **File not found**: Check that `input/testbed.csv` exists
3. **Permission errors**: Ensure write permissions for `output/` directory
4. **Network issues**: Check internet connection for image downloads
5. **Port conflicts**: Change port in `app.py` if 5000 is in use

### Debug Mode

Enable debug output:
```bash
# For CLI
python3 -v process_boxes.py

# For web UI (Flask debug mode is enabled by default)
python3 app.py
```

## License

This project is part of the Copilot use cases demonstration repository.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test both CLI and web interfaces
5. Submit a pull request

---

**Note**: This tool demonstrates how to create consistent functionality across CLI and web interfaces by reusing the same core processing logic.

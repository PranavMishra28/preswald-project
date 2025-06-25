# 🎓 University Rankings Analytics Dashboard

## Overview

The University Rankings Analytics Dashboard is a comprehensive data analysis tool built with Preswald that enables users to explore, filter, visualize, and gain insights from global university rankings data. This interactive dashboard provides an exceptional user interface for analyzing higher education performance metrics across different regions, countries, and institution types.

![University Rankings Dashboard](images/logo.png)

## Features

### 📊 Core Analytics Features

- **Interactive Data Filters**: Filter universities by region, country, size, institution type, and performance metrics
- **Advanced Search**: Find universities by name, location, or any relevant keyword
- **Dynamic Visualizations**: Multiple chart types including scatter plots, bar charts, box plots, and histograms
- **Performance Thresholds**: Adjust minimum score requirements to explore different performance tiers
- **Custom Dataset Export**: Download filtered results in various formats (CSV, JSON, Excel)

### 🔍 Advanced Analysis Capabilities

- **Regional Performance Comparison**: Compare university performance across different global regions
- **Research Excellence Analysis**: Explore the relationship between research performance and other metrics
- **Elite Performers Spotlight**: Highlight top-performing institutions based on customized criteria
- **Score Distribution Analysis**: Understand statistical distribution patterns across regions and institution types

### 🎯 Professional User Experience

- **Intuitive Interface**: Clearly organized sections with professional styling and visual hierarchy
- **Responsive Design**: Optimized layout with proper spacing and visual breathing room
- **Data-Driven Insights**: Automatic calculation of key metrics and performance indicators
- **Expert Tips**: Built-in guidance to help users maximize their analysis experience

## Setup Instructions

### Prerequisites

- Python 3.7+
- Preswald framework installed
- Required Python packages: pandas, plotly

### Installation

1. Clone or download this repository to your local machine:

```bash
git clone https://github.com/yourusername/university-rankings-dashboard.git
cd university-rankings-dashboard
```

2. Install the required dependencies:

```bash
pip install preswald pandas plotly
```

3. Ensure your data file is properly placed in the `data/` directory:

```
data/sample.csv
```

4. Configure your Preswald environment:

- Verify `preswald.toml` contains the correct data source configurations
- Ensure your `secrets.toml` has any required API keys or credentials (if applicable)

## Usage Guide

### Running the Dashboard

1. Navigate to the project directory:

```bash
cd path/to/university-rankings-dashboard
```

2. Launch the application:

```bash
preswald run hello.py
```

3. Access the dashboard through your web browser at the URL provided by Preswald (typically http://localhost:8501)

### Dashboard Sections

1. **Dashboard Overview**: Key metrics about the dataset
2. **Advanced Search & Filter Controls**: Tools to refine your university selection
3. **Elite Universities Showcase**: Top-tier institutions with exceptional scores
4. **Dynamic Performance Analysis**: Adjustable threshold exploration
5. **Customized Results Dashboard**: Your filtered university selection with detailed statistics
6. **Interactive Data Visualization Suite**: Multiple chart options for exploring patterns
7. **Data Export & Action Center**: Tools for downloading and working with your data

### Using Filters

1. **Geographic Selection**:
   - Choose specific regions or countries from dropdown menus
2. **Institution Characteristics**:
   - Filter by university size (XS to XL)
   - Include or exclude private/public institutions
3. **Advanced Analytics Options**:
   - Set minimum academic reputation scores
   - Filter by institutional focus areas
4. **Search Function**:
   - Enter keywords to find specific universities or characteristics

### Visualizing Data

1. Select your preferred visualization type from the dropdown menu:

   - Scatter Plot: Explore relationships between different performance metrics
   - Regional Bar Chart: Compare average scores across regions
   - Distribution Box Plot: Analyze score distributions and statistical patterns
   - Score Histogram: View frequency distribution of scores

2. Interact with the generated charts:
   - Hover over data points for detailed information
   - Zoom in/out for closer examination
   - Download chart images for reports or presentations

## Exporting Data

### Export Options

1. **Format Selection**:

   - CSV (Excel Compatible): For spreadsheet analysis
   - JSON (Data Format): For programmatic use
   - Excel (Advanced Workbook): For comprehensive data analysis

2. **Export Process**:
   - Apply your desired filters
   - Select your preferred export format
   - Click "Download Filtered Dataset"
   - Save the file to your preferred location

### HTML Export

To create a static HTML version of the complete dashboard:

```bash
preswald export --format html
```

This will generate a standalone HTML file in the `preswald_export/` directory that can be shared and viewed without requiring the Preswald framework.

## Project Structure

```
university-rankings-dashboard/
│
├── hello.py                # Main application file
├── preswald.toml           # Preswald configuration
├── secrets.toml            # API keys and credentials (gitignored)
├── README.md               # This documentation file
│
├── data/                   # Data directory
│   └── sample.csv          # University rankings dataset
│
├── images/                 # Image assets
│   ├── favicon.ico         # Browser favicon
│   └── logo.png            # Dashboard logo
│
└── preswald_export/        # Generated exports directory
    └── dashboard.html      # Exported HTML dashboard
```

## Customization

### Adding New Data Sources

1. Update your `preswald.toml` file to include additional data sources
2. Modify the data loading section in `hello.py` to incorporate the new data

### Extending Visualization Options

1. Add new chart types to the visualization selection dropdown
2. Implement the corresponding visualization code in the chart rendering section

### Styling Customization

1. Modify text elements and styling in the dashboard header, metrics cards, and footer
2. Update chart visual properties like colors, fonts, and layouts in the plot settings

## Troubleshooting

### Common Issues

1. **Data Loading Errors**:

   - Ensure your data file is properly formatted and located in the `data/` directory
   - Check that the column names in your data match those referenced in the code

2. **Visualization Errors**:

   - Verify that numeric fields are properly converted from strings to numbers
   - Handle potential null values in your dataset with appropriate error handling

3. **Export Problems**:
   - Check write permissions in your target export directory
   - Ensure the Preswald export functionality is properly configured

## Additional Resources

- [Preswald Documentation](https://preswald.readthedocs.io/)
- [Plotly Python Documentation](https://plotly.com/python/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- University rankings data provided by [Kaggle]
- Built with the Preswald Analytics Framework
- Visualization powered by Plotly
- Data processing with Pandas

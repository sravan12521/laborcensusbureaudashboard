# README: U.S. Bureau of Labor Statistics Dashboard

## Overview

This project is a **U.S. Bureau of Labor Statistics Dashboard** that integrates data from the Bureau of Labor Statistics (BLS) API, processes it, and provides a visual and interactive representation of key labor market indicators. The dashboard is built with **Streamlit** and incorporates interactive charts and data tables for ease of exploration.

## Features

1. **Data Pull and Processing:**
   - Fetches historical and incremental data from the BLS API.
   - Handles datasets like Civilian Labor Force, Non-Farm Employment, Productivity, and Hourly Earnings.
   - Ensures data consistency by merging new data with historical data while removing duplicates.

2. **Interactive Dashboard:**
   - **Date Filtering:** Users can filter charts and tables based on a date range.
   - **Visualizations:** Includes bar charts, pie charts, and data tables.
   - Displays labor statistics in a user-friendly layout, providing insights into the U.S. labor market.

3. **API Integration:**
   - Uses BLS API for automated data retrieval.
   - Supports real-time updates through incremental data loading.

## Prerequisites

To run this project locally, ensure the following are installed:

- Python 3.8+
- Required libraries: `streamlit`, `pandas`, `numpy`, `requests`, `json`, `datetime`, `plotly`, `dateutil`

## Project Structure

- **`load_latest_data.py`**: Handles the incremental loading of the latest data from the BLS API.
- **`dashboard_app.py`**: The core dashboard application, combining data processing and visualization.

## Setup Instructions

1. Clone this repository:
   ```bash
   git clone <repository_url>
   cd <repository_folder>
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the dashboard:
   ```bash
   streamlit run dashboard_app.py
   ```

4. Access the dashboard on your browser at:
   ```
   http://localhost:8501
   ```

## Functional Components

### Data Pulling
- **Historical Data**: Fetches data for the last year from the BLS API.
- **Incremental Data**: Updates the datasets with the latest available information.

### Dashboard Visualizations
- **Bar Charts**: 
  - Civilian Labor Force trends.
  - Non-Farm Employment statistics.
- **Pie Charts**:
  - Quarterly productivity and earnings breakdown.
- **Data Tables**:
  - Displays raw data for further inspection.

### Filters
- **Date Range**: Customize the time period to analyze.
- **Reload Data**: Trigger incremental updates for real-time insights.

## Folder Structure

```plaintext
labor_census_bureau/         # Directory to store downloaded CSV files
load_latest_data.py          # Script for incremental data fetching
dashboard_app.py             # Streamlit-based dashboard
requirements.txt             # List of dependencies
```

## How It Works

1. On the first run, the application:
   - Creates the `labor_census_bureau/` folder if it doesn't exist.
   - Fetches historical data from the BLS API and saves it as CSV files.
   
2. Subsequent runs:
   - Fetch incremental data to update the stored CSV files.

3. The dashboard reads the processed data, applies user-defined filters, and renders visualizations and tables.

## API Keys

This project uses a sample registration key (`34cf2452001040f3ba96a89e33a46db8`) for the BLS API. Replace it with your own API key if necessary.

## Future Improvements

- Add more visualizations and advanced analytics.
- Integrate additional APIs for broader insights.
- Enable user-uploaded data for custom comparisons.


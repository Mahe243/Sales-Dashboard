# 📊 Sales Dashboard (Streamlit + Plotly)

An interactive sales analytics dashboard built with **Streamlit** and **Plotly**.

## Features
- Revenue & Profit KPIs (plus Orders, Avg Order Value, Profit Margin)
- Sales by Region (bar chart)
- Sales by Category (donut chart)
- Monthly Revenue & Profit trend (line chart)
- Top 10 Products by Revenue (horizontal bar chart)
- Region vs Category heatmap
- Sidebar filters: date range, region, category, product
- Downloadable filtered data as CSV

## Project Structure
```
sales_dashboard/
├── app.py               # Main Streamlit application
├── generate_data.py     # Script to generate sample sales_data.csv
├── requirements.txt     # Python dependencies
├── data/
│   └── sales_data.csv   # Sample dataset (auto-generated)
└── README.md
```

## Setup & Run in VS Code

> **Note on Python version:** This has been verified for Python 3.13. The
> `requirements.txt` versions are pinned to minimums that have prebuilt
> wheels for 3.13 (older `numpy`/`pandas` releases don't). If you use an
> older Python (3.9–3.12) the same `requirements.txt` still works fine.

### 1. Open the project
Open the `sales_dashboard` folder in VS Code (`File > Open Folder`).

### 2. Create a virtual environment (recommended)
Open the VS Code integrated terminal (`` Ctrl+` ``) and run:

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Generate sample data
The repo already ships with `data/sales_data.csv`, but you can regenerate a
fresh random dataset anytime:
```bash
python generate_data.py
```

To use your **own data**, replace `data/sales_data.csv` with a CSV that has
these columns: `Date, Region, Category, Product, Quantity, Sales, Profit`.

### 5. Run the dashboard
```bash
streamlit run app.py
```

### 6. View in browser
Streamlit will automatically open your default browser. If not, go to:
```
http://localhost:8501
```

## Customizing
- **Colors/theme**: edit the `<style>` block at the top of `app.py`, or add a
  `.streamlit/config.toml` file for a full Streamlit theme.
- **Data source**: swap `load_data()` in `app.py` to read from a database or
  API instead of CSV.
- **Charts**: all charts use Plotly Express / Graph Objects — add new ones
  following the same pattern (`px.bar`, `px.pie`, `px.line`, `px.imshow`, etc.).

## Troubleshooting
- **Port already in use**: run `streamlit run app.py --server.port 8502`
- **Module not found**: make sure your virtual environment is activated
  before installing/running.
- **CSV not found error**: run `python generate_data.py` first, or check that
  `data/sales_data.csv` exists.

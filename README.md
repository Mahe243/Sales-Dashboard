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

## Proof of Execution
<img width="1413" height="696" alt="Screenshot 2026-07-03 184239" src="https://github.com/user-attachments/assets/7f175513-0953-46ef-8a17-58366bc54332" />
<img width="1920" height="944" alt="Screenshot 2026-07-03 184226" src="https://github.com/user-attachments/assets/f6b68572-2ed9-4353-93e7-44bc4d1142e4" />
<img width="1469" height="634" alt="Screenshot 2026-07-03 184301" src="https://github.com/user-attachments/assets/8d74e4ae-ec8e-490a-b685-99f58e04f4fc" />
<img width="1369" height="665" alt="Screenshot 2026-07-03 184251" src="https://github.com/user-attachments/assets/cc43c1fd-8209-4d0c-bf8b-77b2611d0fbb" />

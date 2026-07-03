"""
Generates synthetic sales data for the dashboard.
Run once: python generate_data.py
Creates data/sales_data.csv
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

regions = ["North", "South", "East", "West", "Central"]
categories = {
    "Electronics": ["Laptop", "Smartphone", "Headphones", "Tablet", "Smartwatch"],
    "Furniture": ["Office Chair", "Desk", "Bookshelf", "Sofa", "Dining Table"],
    "Clothing": ["T-Shirt", "Jeans", "Jacket", "Sneakers", "Cap"],
    "Groceries": ["Coffee", "Snack Pack", "Organic Juice", "Cereal", "Olive Oil"],
    "Stationery": ["Notebook", "Pen Set", "Backpack", "Desk Lamp", "Sticky Notes"],
}

start_date = datetime(2024, 1, 1)
end_date = datetime(2025, 12, 31)
date_range = (end_date - start_date).days

rows = []
for _ in range(6000):
    date = start_date + timedelta(days=np.random.randint(0, date_range))
    region = np.random.choice(regions)
    category = np.random.choice(list(categories.keys()))
    product = np.random.choice(categories[category])

    base_price = {
        "Electronics": np.random.uniform(80, 1200),
        "Furniture": np.random.uniform(60, 900),
        "Clothing": np.random.uniform(15, 150),
        "Groceries": np.random.uniform(3, 40),
        "Stationery": np.random.uniform(5, 80),
    }[category]

    quantity = np.random.randint(1, 12)
    sales = round(base_price * quantity, 2)
    margin = np.random.uniform(0.05, 0.35)
    profit = round(sales * margin, 2)

    rows.append([date.strftime("%Y-%m-%d"), region, category, product, quantity, sales, profit])

df = pd.DataFrame(rows, columns=["Date", "Region", "Category", "Product", "Quantity", "Sales", "Profit"])
df = df.sort_values("Date").reset_index(drop=True)

df.to_csv("data/sales_data.csv", index=False)
print(f"Generated {len(df)} rows -> data/sales_data.csv")

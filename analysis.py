# =====================================
# Hospital Supply Chain Cost Analysis
# =====================================

import pandas as pd
import numpy as np
# File path
file_path = "data/Supply Chain Variable Cost Reduction.xls"

df = pd.read_excel(file_path)
print("Preview of dataset:")
print(df.head())

# -----------------------------
# Inspect dataset structure
# -----------------------------

# Display coloumn names
print("\nDataset information:")
print(df.columns)

# Display dataset information
print("\nDataset information:")
print(df.info())

# Check number of rows and columns
print("\nDataset shape:")
print(df.shape)

# -----------------------------
# Clean column names
# -----------------------------

df_clean = df.copy()

# Standardize column names:
# - remove leading/trailing spaces
# - make everything lowercase
# - replace spaces with underscores
df_clean.columns = (
    df_clean.columns
    .str.strip()
    .str.lower()
    .str.replace(" ","_")
)
print("\nCleaned column  names:")
print(df_clean.columns)

# -----------------------------
# Final column formatting
# -----------------------------

# Replace hyphens with underscores in column names
df_clean.columns = df_clean.columns.str.replace("-", "_")

print("\nFinal cleaned column names:")
print(df_clean.columns)

# -----------------------------
# Remove the empty columns
# -----------------------------

# Dropping columns that contain only missing values
df_clean = df_clean.dropna(axis=1, how="all")

print("\nDataset after removing empty columns:")
print(df_clean.info())

# -----------------------------
# Calculate inventory value
# -----------------------------

# Create a new column for total inventory value
df_clean["inventory_value"] = df_clean["on_hand_quantity"] * df_clean["cost_at_lowest_uom"]

print("\nPreview with inventory value column:")
print(df_clean[["description", "on_hand_quantity", "cost_at_lowest_uom", "inventory_value"]].head())

# -----------------------------
# Identify top inventory value items
# -----------------------------

# Sort items by inventory value (largest first)
top_inventory_items = df_clean.sort_values(by="inventory_value", ascending=False)

# Display the top 10 items with the highest inventory value
print("\nTop 10 items by inventory value:")
print(
    top_inventory_items[
        ["description", "on_hand_quantity", "cost_at_lowest_uom", "inventory_value"]
    ].head(10)
)
# -----------------------------
# Calculate total inventory value
# -----------------------------

# Calculate total inventory value across all items
total_inventory_value = df_clean["inventory_value"].sum()

print("\nTotal inventory value:")
print(total_inventory_value)

# -----------------------------
# Calculate value of top 10 items
# -----------------------------

# Calculate total value of the top 10 inventory items
top_10_value = top_inventory_items["inventory_value"].head(10).sum()

print("\nTotal value of top 10 inventory items:")
print(top_10_value)


# Calculate percentage of total inventory value
top_10_percentage = (top_10_value / total_inventory_value) * 100

print("\nPercentage of total inventory value represented by top 10 items:")
print(top_10_percentage)

# -----------------------------
# Sort items by inventory value
# -----------------------------

# Sort dataset from highest value to lowest value
df_clean = df_clean.sort_values(by="inventory_value", ascending=False)

# Preview top rows after sorting
print("\nTop rows after sorting by inventory value:")
print(df_clean[["description", "inventory_value"]].head())

# -----------------------------
# Calculate cumulative inventory value
# -----------------------------

# Calculate cumulative inventory value as we move down the ranked list
df_clean["cumulative_value"] = df_clean["inventory_value"].cumsum()

# Calculate cumulative percentage of total inventory value
df_clean["cumulative_percentage"] = (
    df_clean["cumulative_value"] / total_inventory_value
) * 100

# Results
print("\nPreview cumulative value calculations:")
print(
    df_clean[
        ["description", "inventory_value", "cumulative_value", "cumulative_percentage"]
    ].head(10)
)

# -----------------------------
# Create ABC inventory classification
# -----------------------------

# Use NumPy to classify items based on cumulative percentage
df_clean["abc_category"] = np.where(
    df_clean["cumulative_percentage"] <= 80, "A",
    np.where(df_clean["cumulative_percentage"] <= 95, "B", "C")
)

# Preview results
print("\nPreview ABC classification:")
print(
    df_clean[
        ["description", "inventory_value", "cumulative_percentage", "abc_category"]
    ].head(15)
)

# -----------------------------
# Summarize ABC categories
# -----------------------------

# Count number of items in each category
category_counts = df_clean["abc_category"].value_counts()

print("\nNumber of items in each ABC category:")
print(category_counts)

# Calculate total value for each category
category_value = df_clean.groupby("abc_category")["inventory_value"].sum()

print("\nTotal inventory value by ABC category:")
print(category_value)

# Calculate percentage of total value for each category
category_percentage = (category_value / total_inventory_value) * 100

print("\nPercentage of total inventory value by ABC category:")
print(category_percentage)

# -----------------------------
# Visualize ABC category value
# -----------------------------

# Import matplotlib for visualization
import matplotlib.pyplot as plt

# Create bar chart
category_value.plot(kind="bar")

# Add labels and title
plt.title("Inventory Value by ABC Category")
plt.xlabel("ABC Category")
plt.ylabel("Total Inventory Value ($)")

# Improve layout
plt.tight_layout()

# Show the chart
plt.show()

# -----------------------------
# Identify high-value items with low stock
# -----------------------------

# Define thresholds
low_stock_threshold = 20
high_value_threshold = df_clean["inventory_value"].quantile(0.90)

# Identify items meeting both conditions
high_value_low_stock = df_clean[
    (df_clean["on_hand_quantity"] < low_stock_threshold) &
    (df_clean["inventory_value"] > high_value_threshold)
]

# Display results
print("\nHigh-value items with low inventory levels:")
print(
    high_value_low_stock[
        ["description", "on_hand_quantity", "inventory_value"]
    ].head(10)
)
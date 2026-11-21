"""Pandas and NumPy analysis for the sales dataset."""

import numpy as np
import pandas as pd

from data_manager import DATA_FILE, ensure_dataset, load_records
from formatter import print_table


def create_dataframe():
    """Construct a DataFrame from the CSV-backed project records."""
    return pd.DataFrame(load_records(), columns=[
        "transaction_id",
        "date",
        "product",
        "category",
        "region",
        "quantity",
        "unit_price",
        "revenue",
        "customer_type",
    ])


def read_dataset():
    """Read the CSV with Pandas and normalize numeric columns and missing regions."""
    ensure_dataset()
    frame = pd.read_csv(DATA_FILE)
    frame["quantity"] = pd.to_numeric(frame["quantity"], errors="raise")
    frame["unit_price"] = pd.to_numeric(frame["unit_price"], errors="raise")
    frame["revenue"] = pd.to_numeric(frame["revenue"], errors="raise")
    missing_regions = int(frame["region"].isna().sum())
    frame["region"] = frame["region"].fillna("Unknown")
    return frame, missing_regions


def generate_summary():
    """Print the requested Pandas and NumPy views, statistics, and insights."""
    frame, missing_regions = read_dataset()
    revenue = frame["revenue"].to_numpy(dtype=float)
    numeric_matrix = frame[["quantity", "revenue"]].to_numpy(dtype=float)
    categories = set(frame["category"].tolist())

    print("\n=== Sales Summary Report ===")
    print(f"Transactions: {len(frame)}")
    print(f"Categories: {', '.join(sorted(categories))}")
    print(f"Missing region values filled as 'Unknown': {missing_regions}")

    print("\nSelected rows (first 5):")
    print_table(frame[["transaction_id", "product", "region", "revenue"]].head())
    print("\nHigh-value transactions (revenue >= overall mean), sorted by revenue:")
    high_value = frame.loc[frame["revenue"] >= frame["revenue"].mean()]
    print_table(
        high_value[["transaction_id", "product", "category", "revenue"]]
        .sort_values("revenue", ascending=False)
        .head(10)
    )

    print("\nRevenue by category (GroupBy):")
    grouped = (
        frame.groupby("category", as_index=False)
        .agg(
            transactions=("transaction_id", "count"),
            units_sold=("quantity", "sum"),
            total_revenue=("revenue", "sum"),
            average_revenue=("revenue", "mean"),
        )
        .sort_values("total_revenue", ascending=False)
    )
    print_table(grouped)

    print("\nPandas statistical analysis:")
    print_table(
        frame[["quantity", "unit_price", "revenue"]].describe().round(2),
        include_index=True,
    )

    print("\nNumPy arrays and calculations:")
    print(f"1D revenue array, first 5 values: {revenue[:5]}")
    print(f"1D array index [0]: {revenue[0]:.2f}")
    print(f"1D array slice [0:5]: {revenue[0:5]}")
    print("2D array [quantity, revenue], first 3 rows:")
    print(numeric_matrix[:3])
    print(f"2D array element [0, 1] (first transaction revenue): {numeric_matrix[0, 1]:.2f}")
    print(
        "Revenue statistics: "
        f"sum={np.sum(revenue):.2f}, mean={np.mean(revenue):.2f}, "
        f"max={np.max(revenue):.2f}, min={np.min(revenue):.2f}, "
        f"std_dev={np.std(revenue):.2f}"
    )

    best_category = grouped.iloc[0]
    best_product = frame.groupby("product")["revenue"].sum().idxmax()
    print("\nKey insights:")
    print(
        f"- {best_category['category']} generated the most revenue "
        f"(${best_category['total_revenue']:.2f})."
    )
    print(f"- {best_product} was the top product by total revenue.")
    print(f"- Average transaction revenue was ${frame['revenue'].mean():.2f}.")
    return frame

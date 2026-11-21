"""CSV-backed sales record creation and CRUD operations."""

import csv
from datetime import date, timedelta
from pathlib import Path


DATA_DIR = Path(__file__).parent / "data"
DATA_FILE = DATA_DIR / "sales_data.csv"
FIELDS = (
    "transaction_id",
    "date",
    "product",
    "category",
    "region",
    "quantity",
    "unit_price",
    "revenue",
    "customer_type",
)

PRODUCTS = {
    "Laptop": ("Electronics", 899.99),
    "Headphones": ("Electronics", 79.50),
    "Keyboard": ("Accessories", 45.00),
    "Mouse": ("Accessories", 24.99),
    "Desk": ("Furniture", 249.00),
    "Chair": ("Furniture", 179.50),
    "Notebook": ("Stationery", 5.25),
    "Pen Set": ("Stationery", 12.00),
}
REGIONS = ("North", "South", "East", "West", "Central")
CUSTOMER_TYPES = ("New", "Returning", "VIP")


def create_sample_dataset(path=DATA_FILE, record_count=100):
    """Create a deterministic sample CSV with at least 50 records."""
    if record_count < 50:
        raise ValueError("The sample dataset must contain at least 50 records.")

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    products = tuple(PRODUCTS.items())
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        for index in range(record_count):
            product, (category, unit_price) = products[index % len(products)]
            quantity = index % 12 + 1
            writer.writerow(
                {
                    "transaction_id": 1001 + index,
                    "date": (date(2025, 1, 1) + timedelta(days=index)).isoformat(),
                    "product": product,
                    "category": category,
                    "region": "" if index % 19 == 0 else REGIONS[index % len(REGIONS)],
                    "quantity": quantity,
                    "unit_price": f"{unit_price:.2f}",
                    "revenue": f"{quantity * unit_price:.2f}",
                    "customer_type": CUSTOMER_TYPES[index % len(CUSTOMER_TYPES)],
                }
            )
    return path


def ensure_dataset():
    """Create the sample CSV when it is not present."""
    if not DATA_FILE.exists():
        create_sample_dataset()
    return DATA_FILE


def load_records():
    """Read the project dataset into a list of dictionaries."""
    ensure_dataset()
    with DATA_FILE.open("r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def save_records(records):
    """Write all records to the project CSV."""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with DATA_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(records)


def add_record(product, region, quantity, customer_type):
    """Validate and append a sales transaction; return the new record."""
    if product not in PRODUCTS:
        raise ValueError(f"Unknown product. Choose one of: {', '.join(PRODUCTS)}")
    if region not in REGIONS:
        raise ValueError(f"Unknown region. Choose one of: {', '.join(REGIONS)}")
    if customer_type not in CUSTOMER_TYPES:
        raise ValueError(
            f"Unknown customer type. Choose one of: {', '.join(CUSTOMER_TYPES)}"
        )
    quantity = int(quantity)
    if quantity <= 0:
        raise ValueError("Quantity must be a positive whole number.")

    records = load_records()
    category, unit_price = PRODUCTS[product]
    record = {
        "transaction_id": max((int(row["transaction_id"]) for row in records), default=1000)
        + 1,
        "date": date.today().isoformat(),
        "product": product,
        "category": category,
        "region": region,
        "quantity": quantity,
        "unit_price": f"{unit_price:.2f}",
        "revenue": f"{quantity * unit_price:.2f}",
        "customer_type": customer_type,
    }
    records.append(record)
    save_records(records)
    return record


def search_records(query):
    """Find records whose ID, product, category, region, or customer type matches."""
    query = str(query).strip().lower()
    return [
        row
        for row in load_records()
        if any(
            query in row[field].lower()
            for field in ("transaction_id", "product", "category", "region", "customer_type")
        )
    ]


def update_record(transaction_id, field, value):
    """Update an allowed field of a record and return whether it was found."""
    editable_fields = {"region", "quantity", "customer_type"}
    if field not in editable_fields:
        raise ValueError(f"Field must be one of: {', '.join(sorted(editable_fields))}")
    records = load_records()
    for row in records:
        if row["transaction_id"] == str(transaction_id):
            if field == "region" and value not in REGIONS:
                raise ValueError(f"Region must be one of: {', '.join(REGIONS)}")
            if field == "customer_type" and value not in CUSTOMER_TYPES:
                raise ValueError(
                    f"Customer type must be one of: {', '.join(CUSTOMER_TYPES)}"
                )
            if field == "quantity":
                quantity = int(value)
                if quantity <= 0:
                    raise ValueError("Quantity must be a positive whole number.")
                row[field] = quantity
                row["revenue"] = f"{quantity * float(row['unit_price']):.2f}"
            else:
                row[field] = value
            save_records(records)
            return True
    return False


def delete_record(transaction_id):
    """Delete a transaction by ID and return whether it was found."""
    records = load_records()
    remaining = [row for row in records if row["transaction_id"] != str(transaction_id)]
    if len(remaining) == len(records):
        return False
    save_records(remaining)
    return True

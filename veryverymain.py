"""Interactive sales record manager and analysis CLI."""

import argparse

from analysis import generate_summary
from data_manager import (
    CUSTOMER_TYPES,
    PRODUCTS,
    REGIONS,
    add_record,
    delete_record,
    ensure_dataset,
    load_records,
    search_records,
    update_record,
)
from formatter import print_table


def prompt_choice(label, options):
    """Prompt until the user enters one of the supported options."""
    print(f"{label}: {', '.join(options)}")
    while True:
        value = input("> ").strip()
        if value in options:
            return value
        print("Please choose one of the listed options.")


def run_menu():
    """Run the interactive record-management menu."""
    ensure_dataset()
    print("Sales Record Manager")
    while True:
        print(
            "\n1. Add record\n2. Display all records\n3. Search records\n"
            "4. Update record\n5. Delete record\n6. Summary report\n7. Exit"
        )
        choice = input("Select an option: ").strip()
        try:
            if choice == "1":
                product = prompt_choice("Products", list(PRODUCTS))
                region = prompt_choice("Regions", list(REGIONS))
                quantity = input("Quantity: ").strip()
                customer_type = prompt_choice("Customer types", list(CUSTOMER_TYPES))
                record = add_record(product, region, quantity, customer_type)
                print(f"Added transaction {record['transaction_id']}.")
            elif choice == "2":
                records = load_records()
                print(f"\nAll records ({len(records)}):")
                print_table(records)
            elif choice == "3":
                query = input("Search by ID, product, category, region, or customer type: ")
                results = search_records(query)
                print(f"\nMatching records ({len(results)}):")
                print_table(results)
            elif choice == "4":
                transaction_id = input("Transaction ID to update: ").strip()
                field = prompt_choice("Editable fields", ["region", "quantity", "customer_type"])
                value = input(f"New {field}: ").strip()
                if update_record(transaction_id, field, value):
                    print("Record updated.")
                else:
                    print("No record found with that ID.")
            elif choice == "5":
                transaction_id = input("Transaction ID to delete: ").strip()
                if delete_record(transaction_id):
                    print("Record deleted.")
                else:
                    print("No record found with that ID.")
            elif choice == "6":
                generate_summary()
            elif choice == "7":
                print("Goodbye.")
                return
            else:
                print("Enter a number from 1 to 7.")
        except (ValueError, OSError) as error:
            print(f"Operation failed: {error}")


def main():
    parser = argparse.ArgumentParser(description="Manage and analyze a sales CSV dataset.")
    parser.add_argument(
        "--report",
        action="store_true",
        help="print the analysis report and exit",
    )
    args = parser.parse_args()
    ensure_dataset()
    if args.report:
        generate_summary()
    else:
        run_menu()


if __name__ == "__main__":
    main()

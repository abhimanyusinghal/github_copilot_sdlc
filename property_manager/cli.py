#!/usr/bin/env python3
"""
Command-line interface for the Property Manager application.
Provides a simple interactive menu to manage property records.
"""

import sys
from .db import PropertyDatabase


def main():
    """Run the interactive CLI for property management."""
    database = PropertyDatabase()

    # Default data file is 'properties.json' in the current working directory
    # Users can override by setting the DB_FILE environment variable if desired
    while True:
        print("\n=== Property Manager ===")
        print("1. Add Property")
        print("2. List Properties")
        print("3. Delete Property")
        print("4. Exit")
        print("========================")

        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            property_id = input("Property ID: ").strip()
            address = input("Address: ").strip()
            owner = input("Owner: ").strip()
            price_input = input("Price: ").strip()
            try:
                price = float(price_input)
            except ValueError:
                print("Invalid price. Please enter a numeric value.")
                continue

            database.add_property(property_id, address, owner, price)

        elif choice == "2":
            database.list_properties()

        elif choice == "3":
            property_id = input("Enter Property ID to delete: ").strip()
            database.delete_property(property_id)

        elif choice == "4":
            print("Goodbye!")
            sys.exit(0)

        else:
            print("Invalid option. Please choose a number between 1 and 4.")


if __name__ == "__main__":
    main()
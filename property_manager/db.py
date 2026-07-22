import json
from pathlib import Path


class PropertyDatabase:
    def __init__(self, file_name="properties.json"):
        self.file_path = Path(file_name)
        self.properties = []
        self.load_data()

    def load_data(self):
        if self.file_path.exists():
            with open(self.file_path, "r", encoding="utf-8") as file:
                self.properties = json.load(file)
        else:
            self.properties = []

    def save_data(self):
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(self.properties, file, indent=4)

    def add_property(self, property_id, address, owner, price):
        property_record = {
            "property_id": property_id,
            "address": address,
            "owner": owner,
            "price": price,
        }
        self.properties.append(property_record)
        self.save_data()
        print("Property added successfully.")

    def list_properties(self):
        if not self.properties:
            print("No properties found.")
            return

        for property_record in self.properties:
            print("-" * 40)
            print(f"ID: {property_record['property_id']}")
            print(f"Address: {property_record['address']}")
            print(f"Owner: {property_record['owner']}")
            print(f"Price: ${property_record['price']}")

    def delete_property(self, property_id):
        original_count = len(self.properties)
        self.properties = [
            property_record
            for property_record in self.properties
            if property_record["property_id"] != property_id
        ]

        if len(self.properties) < original_count:
            self.save_data()
            print("Property deleted successfully.")
        else:
            print("Property not found.")
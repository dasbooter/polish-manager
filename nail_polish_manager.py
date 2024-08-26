import json
import os
from tkinter import messagebox
from polish_database import Polish, PolishDatabase

class Inventory:
    def __init__(self, filename="inventory.json"):
        database_folder = os.path.join(os.path.dirname(__file__), "database")
        os.makedirs(database_folder, exist_ok=True)
        self.filename = os.path.join(database_folder, filename)
        self.polishes = self.load_inventory()

    def load_inventory(self):
        try:
            with open(self.filename, "r") as file:
                polishes_data = json.load(file)
                return [Polish.from_dict(data) for data in polishes_data]
        except FileNotFoundError:
            return []

    def save_inventory(self):
        with open(self.filename, "w") as file:
            json.dump([polish.to_dict() for polish in self.polishes], file)

    def add_to_inventory(self, polish):
        self.polishes.append(polish)
        self.save_inventory()

    def remove_from_inventory(self, index):
        try:
            del self.polishes[index]
            self.save_inventory()
        except IndexError:
            print("Index out of range.")

    def view_inventory(self):
        return self.polishes
    
class Wishlist:
    def __init__(self, filename="wishlist.json"):
        database_folder = os.path.join(os.path.dirname(__file__), "database")
        os.makedirs(database_folder, exist_ok=True)
        self.filename = os.path.join(database_folder, filename)
        self.polishes = self.load_wishlist()

    def load_wishlist(self):
        try:
            with open(self.filename, "r") as file:
                polishes_data = json.load(file)
                return [Polish.from_dict(data) for data in polishes_data]
        except FileNotFoundError:
            return []

    def save_wishlist(self):
        with open(self.filename, "w") as file:
            json.dump([polish.to_dict() for polish in self.polishes], file)

    def add_to_wishlist(self, polish):
        self.polishes.append(polish)
        self.save_wishlist()

    def remove_from_wishlist(self, index):
        try:
            del self.polishes[index]
            self.save_wishlist()
        except IndexError:
            print("Index out of range.")

    def view_wishlist(self):
        return self.polishes

def main():
    db = PolishDatabase()
    inventory = Inventory()

    while True:
        print("\n1. Review Inventory")
        print("2. Search Known Polishes")
        print("3. Add New Polish to Database")
        print("4. Remove Polish from Database")
        print("5. Remove Polish from Inventory")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            inv = inventory.view_inventory()
            if inv:
                print("\nYour Inventory:")
                for idx, polish in enumerate(inv, 1):
                    print(f"{idx}. {polish}")
            else:
                print("\nYour inventory is empty.")

        elif choice == '2':
            name = input("Enter polish name (or press Enter to skip): ")
            collection = input("Enter collection (or press Enter to skip): ")
            brand = input("Enter brand (or press Enter to skip): ")
            color = input("Enter color (or press Enter to skip): ")
            finish = input("Enter finish (or press Enter to skip): ")
            
            results = db.search_polish(name, collection, brand, color, finish)
            if results:
                print("\nSearch Results:")
                for idx, polish in enumerate(results, 1):
                    print(f"{idx}. {polish}")
                add_choice = input("Enter the number of the polish to add to your inventory (or press Enter to skip): ")
                if add_choice:
                    inventory.add_to_inventory(results[int(add_choice)-1])
                    print("Polish added to your inventory.")
            else:
                print("No polishes found matching the criteria.")

        elif choice == '3':
            name = input("Enter polish name: ")
            collection = input("Enter collection: ")
            brand = input("Enter brand: ")
            color = input("Enter color: ")
            finish = input("Enter finish: ")
            
            new_polish = Polish(name, collection, brand, color, finish)
            db.add_polish(new_polish)
            print("New polish added to the database.")

        elif choice == '4':
            print("\nPolishes in Database:")
            all_polishes = db.display_all()
            for idx, polish in enumerate(all_polishes, 1):
                print(f"{idx}. {polish}")
            index = input("Enter the number of the polish to remove (or press Enter to skip): ")
            if index:
                db.remove_polish(index=int(index)-1)
                print("Polish removed from the database.")

        elif choice == '5':
            inv = inventory.view_inventory()
            if inv:
                print("\nYour Inventory:")
                for idx, polish in enumerate(inv, 1):
                    print(f"{idx}. {polish}")
                index = input("Enter the number of the polish to remove from your inventory: ")
                if index:
                    inventory.remove_from_inventory(int(index)-1)
                    print("Polish removed from your inventory.")
            else:
                print("\nYour inventory is empty.")

        elif choice == '6':
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

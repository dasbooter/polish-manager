import os
import tkinter as tk
from datetime import datetime
from polish_database import Inventory, PolishDatabase, Polish, Wishlist
from polish_form import PolishForm

class NailPolishApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Nail Polish Manager")
        self.current_info_window = None

        self.db = PolishDatabase()
        self.inventory = Inventory()
        self.wishlist = Wishlist()

        assets_path = os.path.join(os.path.dirname(__file__), "assets")
        self.heart_icon = tk.PhotoImage(file=os.path.join(assets_path, "heart_icon.png")).subsample(12, 12)
        self.plus_icon = tk.PhotoImage(file=os.path.join(assets_path, "plus_icon.png")).subsample(15, 15)
        self.minus_icon = tk.PhotoImage(file=os.path.join(assets_path, "minus_icon.png")).subsample(15, 15)

        self.create_buttons()

    def create_buttons(self):
        tk.Button(self.root, text="Review Inventory", command=lambda: self.view_items("inventory")).pack(pady=10)
        tk.Button(self.root, text="Wishlist", command=lambda: self.view_items("wishlist")).pack(pady=10)
        tk.Button(self.root, text="Search Polish Database", command=self.search_polishes).pack(pady=10)
        tk.Button(self.root, text="Add New Polish to Database", command=self.add_polish_to_database).pack(pady=10)
        tk.Button(self.root, text="Edit Database", command=self.edit_polish_in_database).pack(pady=10)
        tk.Button(self.root, text="Remove Polish from Database", command=self.remove_polish_from_database).pack(pady=10)
        tk.Button(self.root, text="Exit", command=self.root.quit).pack(pady=10)

    def show_message(self, title, message):
        if self.current_info_window:
            self.current_info_window.destroy()

        self.current_info_window = tk.Toplevel(self.root)
        self.current_info_window.title(title)
        tk.Label(self.current_info_window, text=message).pack(padx=20, pady=20)
        tk.Button(self.current_info_window, text="OK", command=self.current_info_window.destroy).pack(pady=10)

    def view_items(self, item_type):
        items = getattr(self, item_type).display_all()

        if items:
            if hasattr(self, 'items_window') and self.items_window.winfo_exists():
                for widget in self.items_window.winfo_children():
                    widget.destroy()
            else:
                self.items_window = tk.Toplevel(self.root)
                self.items_window.title(f"Your {item_type.capitalize()}")

            for item in items:
                frame = tk.Frame(self.items_window)
                frame.pack(fill='x', pady=5)

                tk.Label(frame, text=str(item)).pack(side="left", padx=10)

                if item_type == "wishlist":
                    tk.Button(frame, image=self.plus_icon, command=lambda p=item: self.add_to_inventory(p)).pack(side="right")
                    tk.Button(frame, image=self.minus_icon, command=lambda p=item: self.remove_from_wishlist(p)).pack(side="right")

        else:
            self.show_message(f"Your {item_type.capitalize()}", f"Your {item_type} is empty.")

    def search_polishes(self):
        search_window = tk.Toplevel(self.root)
        search_window.title("Search Known Polishes")

        polish_form = PolishForm(search_window, self.db)

        def search_results():
            data = polish_form.get_form_data()

            results = self.db.search_polish(**data)

            if results:
                result_window = tk.Toplevel(search_window)
                result_window.title("Search Results")

                for idx, polish in enumerate(results):
                    frame = tk.Frame(result_window)
                    frame.pack(fill='x', pady=5)

                    tk.Button(frame, text=str(polish), command=lambda p=polish: self.add_to_inventory_and_close(p, result_window)).pack(side="left")
                    tk.Button(frame, image=self.heart_icon, command=lambda p=polish: self.add_to_wishlist(p)).pack(side="right")
            else:
                self.show_message("Search Results", "No polishes found matching the criteria.")

        tk.Button(search_window, text="Search", command=search_results).grid(row=12, column=0, columnspan=2, pady=10)

    def add_polish_to_database(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add New Polish to Database")

        polish_form = PolishForm(add_window, self.db)

        def save_polish():
            data = polish_form.get_form_data()

            if not data["name"]:
                self.show_message("Error", "Polish name is required.")
                return

            new_polish = Polish(**data)
            self.db.manage_polish(new_polish, "add")
            self.show_message("Success", "New polish added to the database.")
            add_window.destroy()

        tk.Button(add_window, text="Add Polish", command=save_polish).grid(row=12, column=0, columnspan=2, pady=10)

    def edit_polish_in_database(self):
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Polish in Database")

        polish_form = PolishForm(edit_window, self.db)

        def search_and_edit():
            data = polish_form.get_form_data()

            results = self.db.search_polish(**data)

            if results:
                polish = results[0] 
                polish_form.populate_form(polish)
                self.edit_polish_form(polish, edit_window)
            else:
                self.show_message("Search Results", "No polishes found matching the criteria.")

        tk.Button(edit_window, text="Search", command=search_and_edit).grid(row=12, column=0, columnspan=2, pady=10)

    def remove_polish_from_database(self):
        remove_window = tk.Toplevel(self.root)
        remove_window.title("Remove Polish from Database")

        polish_form = PolishForm(remove_window, self.db)

        def search_and_remove():
            data = polish_form.get_form_data()

            results = self.db.search_polish(**data)

            if results:
                result_window = tk.Toplevel(remove_window)
                result_window.title("Select Polish to Remove")

                for idx, polish in enumerate(results):
                    tk.Button(result_window, text=str(polish), command=lambda p=polish: self.remove_selected_polish(p, result_window)).pack(pady=5)
            else:
                self.show_message("Search Results", "No polishes found matching the criteria.")

        tk.Button(remove_window, text="Search", command=search_and_remove).grid(row=12, column=0, columnspan=2, pady=10)

    def remove_selected_polish(self, polish, result_window):
        self.db.manage_polish(polish, "remove")
        self.show_message("Success", "Polish removed from the database.")
        result_window.destroy()

    def edit_polish_form(self, polish, parent_window):
        polish_form = PolishForm(parent_window, self.db)
        polish_form.populate_form(polish)

        def save_changes():
            data = polish_form.get_form_data()
            polish.name = data["name"]
            polish.collection = data["collection"]
            polish.year = data["year"]
            polish.brand = data["brand"]
            polish.color = data["color"]
            polish.finish = data["finish"]
            polish.alternate_finish = data["alternate_finish"]

            self.db.manage_polish(polish, "update")
            self.show_message("Success", "Polish details updated successfully.")
            parent_window.destroy()

        tk.Button(parent_window, text="Save Changes", command=save_changes).grid(row=12, column=0, columnspan=2, pady=10)

    def add_to_inventory_and_close(self, polish, window):
        self.inventory.manage_polish(polish, "add")
        self.show_message("Success", f"{polish.name} added to your inventory.")
        window.destroy()

    def add_to_wishlist(self, polish):
        self.wishlist.manage_polish(polish, "add")
        self.show_message("Success", f"{polish.name} added to your wishlist.")

    def remove_from_wishlist(self, polish):
        self.wishlist.manage_polish(polish, "remove")
        self.show_message("Success", f"{polish.name} removed from your wishlist.")
        self.view_items("wishlist")

    def add_to_inventory(self, polish):
        self.inventory.manage_polish(polish, "add")
        self.show_message("Success", f"{polish.name} added to your inventory.")
        self.wishlist.manage_polish(polish, "remove")
        self.view_items("wishlist")

if __name__ == "__main__":
    root = tk.Tk()
    app = NailPolishApp(root)
    root.mainloop()
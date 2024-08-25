import tkinter as tk
from tkinter import messagebox, simpledialog
from nail_polish_manager import Inventory, PolishDatabase, Polish

class NailPolishApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Nail Polish Manager")

        # Set up the database and inventory
        self.db = PolishDatabase()
        self.inventory = Inventory()

        # Create buttons for each action
        self.create_buttons()

    def create_buttons(self):
        tk.Button(self.root, text="Review Inventory", command=self.review_inventory).pack(pady=10)
        tk.Button(self.root, text="Search Known Polishes", command=self.search_polishes).pack(pady=10)
        tk.Button(self.root, text="Add New Polish to Database", command=self.add_polish_to_database).pack(pady=10)
        tk.Button(self.root, text="Remove Polish from Database", command=self.remove_polish_from_database).pack(pady=10)
        tk.Button(self.root, text="Remove Polish from Inventory", command=self.remove_polish_from_inventory).pack(pady=10)
        tk.Button(self.root, text="Exit", command=self.root.quit).pack(pady=10)

    def review_inventory(self):
        inventory = self.inventory.view_inventory()
        
        if inventory:
            inventory_window = tk.Toplevel(self.root)
            inventory_window.title("Your Inventory")

            for polish in inventory:
                tk.Label(inventory_window, text=str(polish)).pack(anchor='w', padx=10, pady=2)
        else:
            messagebox.showinfo("Your Inventory", "Your inventory is empty.")

    def search_polishes(self):
        search_window = tk.Toplevel(self.root)
        search_window.title("Search Known Polishes")

        tk.Label(search_window, text="Polish Name:").grid(row=0, column=0, padx=10, pady=5)
        name_entry = tk.Entry(search_window)
        name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(search_window, text="Collection:").grid(row=1, column=0, padx=10, pady=5)
        collection_entry = tk.Entry(search_window)
        collection_entry.grid(row=1, column=1, padx=10, pady=5)
        self.create_listbox_for_entry(search_window, collection_entry, self.get_unique_values("collection"), row=2)

        tk.Label(search_window, text="Brand:").grid(row=3, column=0, padx=10, pady=5)
        brand_entry = tk.Entry(search_window)
        brand_entry.grid(row=3, column=1, padx=10, pady=5)
        self.create_listbox_for_entry(search_window, brand_entry, self.get_unique_values("brand"), row=4)

        tk.Label(search_window, text="Color:").grid(row=5, column=0, padx=10, pady=5)
        color_entry = tk.Entry(search_window)
        color_entry.grid(row=5, column=1, padx=10, pady=5)
        self.create_listbox_for_entry(search_window, color_entry, self.get_unique_values("color"), row=6)

        tk.Label(search_window, text="Finish:").grid(row=7, column=0, padx=10, pady=5)
        finish_entry = tk.Entry(search_window)
        finish_entry.grid(row=7, column=1, padx=10, pady=5)
        self.create_listbox_for_entry(search_window, finish_entry, self.get_unique_values("finish"), row=8)

        def search_results():
            name = name_entry.get()
            collection = collection_entry.get()
            brand = brand_entry.get()
            color = color_entry.get()
            finish = finish_entry.get()

            results = self.db.search_polish(name, collection, brand, color, finish)
            
            if results:
                result_window = tk.Toplevel(search_window)
                result_window.title("Search Results")

                for idx, polish in enumerate(results):
                    tk.Button(result_window, text=str(polish), command=lambda p=polish: self.add_to_inventory_and_close(p, result_window)).pack(pady=5)
            else:
                messagebox.showinfo("Search Results", "No polishes found matching the criteria.")

        tk.Button(search_window, text="Search", command=search_results).grid(row=9, column=0, columnspan=2, pady=10)



    def add_to_inventory_and_close(self, polish, window):
        self.inventory.add_to_inventory(polish)
        messagebox.showinfo("Success", f"{polish.name} added to your inventory.")
        window.destroy()

    def add_polish_to_database(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add New Polish to Database")

        tk.Label(add_window, text="Polish Name:").grid(row=0, column=0, padx=10, pady=5)
        name_entry = tk.Entry(add_window)
        name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(add_window, text="Collection:").grid(row=1, column=0, padx=10, pady=5)
        collection_entry = tk.Entry(add_window)
        collection_entry.grid(row=1, column=1, padx=10, pady=5)
        self.create_listbox_for_entry(add_window, collection_entry, self.get_unique_values("collection"), row=2)

        tk.Label(add_window, text="Brand:").grid(row=3, column=0, padx=10, pady=5)
        brand_entry = tk.Entry(add_window)
        brand_entry.grid(row=3, column=1, padx=10, pady=5)
        self.create_listbox_for_entry(add_window, brand_entry, self.get_unique_values("brand"), row=4)

        tk.Label(add_window, text="Color:").grid(row=5, column=0, padx=10, pady=5)
        color_entry = tk.Entry(add_window)
        color_entry.grid(row=5, column=1, padx=10, pady=5)
        self.create_listbox_for_entry(add_window, color_entry, self.get_unique_values("color"), row=6)

        tk.Label(add_window, text="Finish:").grid(row=7, column=0, padx=10, pady=5)
        finish_entry = tk.Entry(add_window)
        finish_entry.grid(row=7, column=1, padx=10, pady=5)
        self.create_listbox_for_entry(add_window, finish_entry, self.get_unique_values("finish"), row=8)

        def save_polish():
            name = name_entry.get()
            collection = collection_entry.get()
            brand = brand_entry.get()
            color = color_entry.get()
            finish = finish_entry.get()

            if not name:
                messagebox.showerror("Error", "Polish name is required.")
                return

            new_polish = Polish(name, collection, brand, color, finish)
            self.db.add_polish(new_polish)
            messagebox.showinfo("Success", "New polish added to the database.")
            add_window.destroy()

        tk.Button(add_window, text="Add Polish", command=save_polish).grid(row=9, column=0, columnspan=2, pady=10)

    def create_listbox_for_entry(self, window, entry, values, row):
        listbox = tk.Listbox(window, height=5)
        listbox.grid(row=row, column=1, padx=10, pady=5)
        listbox.bind("<<ListboxSelect>>", lambda event: self.select_from_listbox(event, entry))
        
        for value in values:
            listbox.insert(tk.END, value)

    def select_from_listbox(self, event, entry):
        widget = event.widget
        selection = widget.curselection()
        if selection:
            selected_value = widget.get(selection[0])
            entry.delete(0, tk.END)
            entry.insert(0, selected_value)

    def get_unique_values(self, attribute):
        polishes = self.db.display_all()
        return sorted(set(getattr(polish, attribute) for polish in polishes if getattr(polish, attribute)))

    def remove_polish_from_database(self):
        polishes = self.db.display_all()
        
        if polishes:
            remove_window = tk.Toplevel(self.root)
            remove_window.title("Remove Polish from Database")

            for idx, polish in enumerate(polishes):
                tk.Button(remove_window, text=str(polish), command=lambda i=idx: self.remove_from_db_and_close(i, remove_window)).pack(pady=5)
        else:
            messagebox.showinfo("Remove Polish", "No polishes in the database.")

    def remove_from_db_and_close(self, index, window):
        self.db.remove_polish(index=index)
        messagebox.showinfo("Success", "Polish removed from the database.")
        window.destroy()

    def remove_polish_from_inventory(self):
        inventory = self.inventory.view_inventory()
        
        if inventory:
            remove_window = tk.Toplevel(self.root)
            remove_window.title("Remove Polish from Inventory")

            for idx, polish in enumerate(inventory):
                tk.Button(remove_window, text=str(polish), command=lambda i=idx: self.remove_from_inventory_and_close(i, remove_window)).pack(pady=5)
        else:
            messagebox.showinfo("Remove Polish", "Your inventory is empty.")

    def remove_from_inventory_and_close(self, index, window):
        self.inventory.remove_from_inventory(index=index)
        messagebox.showinfo("Success", "Polish removed from your inventory.")
        window.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = NailPolishApp(root)
    root.mainloop()

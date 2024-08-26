import tkinter as tk
from datetime import datetime

class PolishForm:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.entries = {}
        self.listboxes = {}
        self.create_form_fields()

    def create_form_fields(self):
        # Polish Name
        tk.Label(self.parent, text="Polish Name:").grid(row=0, column=0, padx=10, pady=5)
        name_entry = tk.Entry(self.parent)
        name_entry.grid(row=0, column=1, padx=10, pady=5)
        self.entries["name"] = name_entry

        # Collection
        tk.Label(self.parent, text="Collection:").grid(row=1, column=0, padx=10, pady=5)
        collection_entry = tk.Entry(self.parent)
        collection_entry.grid(row=1, column=1, padx=10, pady=5)
        self.entries["collection"] = collection_entry
        self.create_listbox_for_entry(collection_entry, self.get_unique_values("collection"), row=2)

        # Year
        tk.Label(self.parent, text="Year:").grid(row=3, column=0, padx=10, pady=5)
        year_listbox = tk.Listbox(self.parent, height=4)
        year_listbox.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
        scrollbar = tk.Scrollbar(self.parent, orient="vertical", command=year_listbox.yview)
        scrollbar.grid(row=3, column=2, sticky='ns')
        year_listbox.config(yscrollcommand=scrollbar.set)
        current_year = datetime.now().year
        for year in range(current_year, 1900, -1):
            year_listbox.insert(tk.END, str(year))
        self.listboxes["year"] = year_listbox

        # Brand
        tk.Label(self.parent, text="Brand:").grid(row=4, column=0, padx=10, pady=5)
        brand_entry = tk.Entry(self.parent)
        brand_entry.grid(row=4, column=1, padx=10, pady=5)
        self.entries["brand"] = brand_entry
        self.create_listbox_for_entry(brand_entry, self.get_unique_values("brand"), row=5)

        # Color
        tk.Label(self.parent, text="Color:").grid(row=6, column=0, padx=10, pady=5)
        color_entry = tk.Entry(self.parent)
        color_entry.grid(row=6, column=1, padx=10, pady=5)
        self.entries["color"] = color_entry
        self.create_listbox_for_entry(color_entry, self.get_unique_values("color"), row=7)

        # Finish
        tk.Label(self.parent, text="Finish:").grid(row=8, column=0, padx=10, pady=5)
        finish_entry = tk.Entry(self.parent)
        finish_entry.grid(row=8, column=1, padx=10, pady=5)
        self.entries["finish"] = finish_entry
        self.create_listbox_for_entry(finish_entry, self.get_unique_values("finish"), row=9)

        # Alternate Finish
        tk.Label(self.parent, text="Alternate Finish:").grid(row=10, column=0, padx=10, pady=5)
        alt_finish_entry = tk.Entry(self.parent)
        alt_finish_entry.grid(row=10, column=1, padx=10, pady=5)
        self.entries["alternate_finish"] = alt_finish_entry
        self.create_listbox_for_entry(alt_finish_entry, self.get_unique_values("alternate_finish"), row=11)

    def create_listbox_for_entry(self, entry, values, row):
        listbox = tk.Listbox(self.parent, height=5)
        listbox.grid(row=row, column=1, padx=10, pady=5)
        listbox.bind("<<ListboxSelect>>", lambda event: self.select_from_listbox(event, entry))
        
        for value in values:
            listbox.insert(tk.END, value)
        
        self.listboxes[entry] = listbox

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

    def populate_form(self, polish):
        self.entries["name"].insert(0, polish.name)
        self.entries["collection"].insert(0, polish.collection)
        for i in range(self.listboxes["year"].size()):
            if self.listboxes["year"].get(i) == polish.year:
                self.listboxes["year"].selection_set(i)
                break
        self.entries["brand"].insert(0, polish.brand)
        self.entries["color"].insert(0, polish.color)
        self.entries["finish"].insert(0, polish.finish)
        self.entries["alternate_finish"].insert(0, polish.alternate_finish)

    def get_form_data(self):
        data = {}
        for key, widget in self.entries.items():
            data[key] = widget.get()
        if "year" in self.listboxes:
            selection = self.listboxes["year"].curselection()
            data["year"] = self.listboxes["year"].get(selection) if selection else ""
        return data

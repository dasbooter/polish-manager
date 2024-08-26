import json
import os

class Polish:
    def __init__(self, name, collection, year, brand, color, finish, alternate_finish):
        self.name = name
        self.collection = collection
        self.year = year
        self.brand = brand
        self.color = color
        self.finish = finish
        self.alternate_finish = alternate_finish

    def __str__(self):
        return f"{self.name} ({self.collection}) by {self.brand} ({self.year}) - Color: {self.color} - Finish: {self.finish} ALT: {self.alternate_finish}"

    def to_dict(self):
        return {
            "name": self.name,
            "collection": self.collection,
            "year": self.year,
            "brand": self.brand,
            "color": self.color,
            "finish": self.finish,
            "alternate finish": self.alternate_finish
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data.get("name", ""),
            data.get("collection", ""),
            data.get("year", ""),  
            data.get("brand", ""),
            data.get("color", ""),
            data.get("finish", ""),
            data.get("alternate finish", "")
        )

class PolishDatabase:
    def __init__(self, filename="polish_database.json"):
        database_folder = os.path.join(os.path.dirname(__file__), "database")
        os.makedirs(database_folder, exist_ok=True)
        self.filename = os.path.join(database_folder, filename)
        self.polishes = self.load_polishes()

    def load_polishes(self):
        try:
            with open(self.filename, "r") as file:
                polishes_data = json.load(file)
                return [Polish.from_dict(data) for data in polishes_data]
        except FileNotFoundError:
            return []
    
    def save_polishes(self):
        with open(self.filename, "w") as file:
            json.dump([polish.to_dict() for polish in self.polishes], file)

    def manage_polish(self, polish, operation="add"):
        if operation == "add":
            self.polishes.append(polish)
        elif operation == "update":
            for i, p in enumerate(self.polishes):
                if p.name == polish.name:
                    self.polishes[i] = polish
                    break
        elif operation == "remove":
            self.polishes = [p for p in self.polishes if p != polish]
        self.save_polishes()

    def search_polish(self, **kwargs):
        results = []
        for polish in self.polishes:
            if all(getattr(polish, key, "").lower() == val.lower() for key, val in kwargs.items() if val):
                results.append(polish)
        return results

    def display_all(self):
        return self.polishes

class Inventory(PolishDatabase):
    def __init__(self, filename="inventory.json"):
        super().__init__(filename)

class Wishlist(PolishDatabase):
    def __init__(self, filename="wishlist.json"):
        super().__init__(filename)


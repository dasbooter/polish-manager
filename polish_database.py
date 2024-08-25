import json

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
        self.filename = filename
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

    def add_polish(self, polish):
        self.polishes.append(polish)
        self.save_polishes()

    def remove_polish(self, index=None, name=None, collection=None, year=None, brand=None, color=None, finish=None, alternate_finish=None):
        if index is not None:
            try:
                del self.polishes[index]
            except IndexError:
                print("Index out of range.")
        else:
            self.polishes = [polish for polish in self.polishes if not (
                (name and name.lower() == polish.name.lower()) and
                (collection and collection.lower() == polish.collection.lower()) and
                (year and year.lower() == polish.year.lower()) and
                (brand and brand.lower() == polish.brand.lower()) and
                (color and color.lower() == polish.color.lower()) and
                (finish and finish.lower() == polish.finish.lower()) and
                (alternate_finish and alternate_finish.lower() == polish.alternate_finish.lower())
            )]
        self.save_polishes()

    def search_polish(self, name=None, collection=None, year=None, brand=None, color=None, finish=None, alternate_finish=None):
        results = []
        for polish in self.polishes:
            if ((name and name.lower() in polish.name.lower()) or
                (collection and collection.lower() in polish.collection.lower()) or
                (year and year.lower() == polish.year.lower()) or
                (brand and brand.lower() in polish.brand.lower()) or
                (color and color.lower() in polish.color.lower()) or
                (finish and finish.lower() in polish.finish.lower()) or
                (alternate_finish and alternate_finish.lower() == polish.alternate_finish.lower())):
                results.append(polish)
        return results

    def display_all(self):
        return self.polishes

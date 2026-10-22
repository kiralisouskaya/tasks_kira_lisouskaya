import json
from abc import ABC, abstractmethod


class BaseParser(ABC):
    """Abstract base class defining the standard interface for input file parsers."""
    @abstractmethod
    def parse(self, file_path: str) -> list[tuple]:
        """Define the parse method signature accepting self and a file path returning a list of tuples"""
        pass


class RoomsJSONParser(BaseParser):
    """Parses JSON files containing room records into database tuples."""
    def parse(self, file_path: str) -> list[tuple]:
        """Implement the parse method to convert room JSON data into database tuples"""
        with open(file_path, "r", encoding="utf-8") as file:
            # Parse raw JSON text into Python dictionaries
            data = json.load(file)
            # Extract id and name into a tuple for each room record
            return [(item["id"], item["name"]) for item in data]


class StudentsJSONParser(BaseParser):
    """Parses JSON files containing student records into database tuples."""
    def parse(self, file_path: str) -> list[tuple]:
        """Implement the parse method to convert student JSON data into database tuples"""
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            # Map each student dictionary entry to a tuple matching database table column order
            return [
                (
                    item["id"],
                    item["name"],
                    item["birthday"],
                    item["sex"],
                    item["room"],
                )
                # Iterate through every student dictionary in the loaded JSON list
                for item in data
            ]

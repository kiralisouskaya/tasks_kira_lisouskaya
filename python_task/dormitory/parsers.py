import json


class JSONFileParser:
    """
    A general-purpose parser for reading JSON files.
    Extracts raw data without binding it to a specific database schema.
    """

    @staticmethod
    def parse(filepath: str) -> list[dict]:
        """
        Reads a JSON file and returns its content as a list of dictionaries.
        """
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
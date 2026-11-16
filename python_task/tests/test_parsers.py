import json
import os
import tempfile
import unittest

from dormitory.parsers import JSONFileParser


class TestParsers(unittest.TestCase):
    """Unit tests for the universal JSON parser."""

    def setUp(self):
        """Create a temporary JSON file with sample data before each test."""
        self.temp_file = tempfile.NamedTemporaryFile(
            mode="w+", delete=False, encoding="utf-8"
        )
        self.test_data = [
            {"id": 1, "name": "Room #1"},
            {"id": 2, "name": "Room #2"},
        ]
        json.dump(self.test_data, self.temp_file)
        self.temp_file.close()

    def tearDown(self):
        """Clean up the temporary file after each test execution."""
        if os.path.exists(self.temp_file.name):
            os.remove(self.temp_file.name)

    def test_json_file_parser(self):
        """Verify JSONFileParser correctly reads JSON into a list of dictionaries."""
        # Invoke the static parse method and verify it returns dictionaries, not tuples
        result = JSONFileParser.parse(self.temp_file.name)
        self.assertEqual(result, self.test_data)


if __name__ == "__main__":
    unittest.main()
# Import json module to handle creation, dumping, and parsing of JSON test data
import json
# Import os module to perform file system operations like deleting temporary files
import os
# Import tempfile module to safely create temporary files for isolated test runs
import tempfile
import unittest
# Import ElementTree module aliased as ET to parse and validate generated XML trees
import xml.etree.ElementTree as ET
from exporters import ExportFormatSelector, JSONExporter, XMLExporter
from parsers import RoomsJSONParser, StudentsJSONParser


class TestParsers(unittest.TestCase):
    """Unit tests for input JSON parsers defined in parsers.py."""
    def setUp(self):
        """Create temporary JSON files before each test execution."""
        # Create a named temporary file on disk for rooms test data in write mode
        self.temp_rooms = tempfile.NamedTemporaryFile(
            mode="w+", delete=False, encoding="utf-8"
        )
        # Define sample list of dictionaries representing room records
        rooms_data = [
            {"id": 1, "name": "Room #1"},
            {"id": 2, "name": "Room #2"},
        ]
        # Serialize and write the sample room dictionaries into the temporary file
        json.dump(rooms_data, self.temp_rooms)
        self.temp_rooms.close()

        # Create a named temporary file on disk for students test data in write mode
        self.temp_students = tempfile.NamedTemporaryFile(
            mode="w+", delete=False, encoding="utf-8"
        )
        # Define sample list of dictionaries representing student records
        students_data = [
            {
                "id": 101,
                "name": "John Doe",
                "birthday": "2000-01-01T00:00:00",
                "sex": "M",
                "room": 1,
            }
        ]
        # Serialize and write the sample student dictionaries into the temporary file
        json.dump(students_data, self.temp_students)
        self.temp_students.close()

    # Special teardown method that automatically executes AFTER each test method run
    def tearDown(self):
        """Clean up temporary files after each test execution."""
        # Check if the temporary rooms file exists on disk
        if os.path.exists(self.temp_rooms.name):
            os.remove(self.temp_rooms.name)
        # Check if the temporary students file exists on disk
        if os.path.exists(self.temp_students.name):
            os.remove(self.temp_students.name)

    def test_rooms_parser(self):
        """Verify RoomsJSONParser converts JSON array into tuples correctly."""
        # Instantiate RoomsJSONParser object
        parser = RoomsJSONParser()
        # Parse the temporary rooms JSON file and store returned tuples list
        result = parser.parse(self.temp_rooms.name)
        # Define expected tuple list output matching database column format
        expected = [(1, "Room #1"), (2, "Room #2")]
        # Assert that actual parser output equals expected list of tuples
        self.assertEqual(result, expected)

    def test_students_parser(self):
        """Verify StudentsJSONParser converts JSON array into tuples matching column order."""
        # Instantiate StudentsJSONParser object
        parser = StudentsJSONParser()
        # Parse the temporary students JSON file and store returned tuples list
        result = parser.parse(self.temp_students.name)
        # Define expected tuple list output matching database column format
        expected = [(101, "John Doe", "2000-01-01T00:00:00", "M", 1)]
        # Assert that actual parser output equals expected list of tuples
        self.assertEqual(result, expected)


# Define test suite class for exporters and factory inheriting from unittest.TestCase
class TestExporters(unittest.TestCase):
    """Unit tests for serializers and factory defined in exporters.py."""
    def setUp(self):
        """Prepare sample dictionary dataset and temporary output file path."""
        # Define mock analytical query result dataset as list of dictionaries
        self.test_data = [
            {"room_id": 1, "room_name": "Room #1", "student_count": 5}
        ]
        # Create a named temporary file path where exporter will write output
        self.temp_output = tempfile.NamedTemporaryFile(delete=False)
        self.temp_output.close()

    def tearDown(self):
        """Clean up temporary export output file."""
        # Check if exported output file exists on disk
        if os.path.exists(self.temp_output.name):
            os.remove(self.temp_output.name)

    def test_json_exporter(self):
        """Verify JSONExporter serializes dictionaries into valid JSON format."""
        # Instantiate JSONExporter object
        exporter = JSONExporter()
        # Export sample dictionary data into temporary output file path
        exporter.export(self.test_data, self.temp_output.name)

        # Open generated JSON output file in read mode with UTF-8 encoding
        with open(self.temp_output.name, "r", encoding="utf-8") as f:
            # Deserialize JSON content back into Python list of dictionaries
            data = json.load(f)
        # Assert loaded JSON data equals original input dictionary data
        self.assertEqual(data, self.test_data)

    def test_xml_exporter(self):
        """Verify XMLExporter serializes dictionaries into valid XML tree structure."""
        # Instantiate XMLExporter object
        exporter = XMLExporter()
        # Export sample dictionary data into temporary output file path
        exporter.export(self.test_data, self.temp_output.name)

        # Parse generated XML output file into ElementTree object
        tree = ET.parse(self.temp_output.name)
        # Get root XML node element
        root = tree.getroot()

        # Assert root element tag name is 'results'
        self.assertEqual(root.tag, "results")
        # Find all child elements with tag name 'item' under root node
        items = root.findall("item")
        # Assert exactly one 'item' element exists in XML structure
        self.assertEqual(len(items), 1)
        # Assert room_id child element text content equals '1'
        self.assertEqual(items[0].find("room_id").text, "1")
        # Assert room_name child element text content equals 'Room #1'
        self.assertEqual(items[0].find("room_name").text, "Room #1")
        # Assert student_count child element text content equals '5'
        self.assertEqual(items[0].find("student_count").text, "5")

    def test_export_format_selector(self):
        """Verify ExportFormatSelector factory instantiates matching exporters and raises ValueError for invalid formats."""
        # Request JSON exporter from factory using string argument 'json'
        json_exp = ExportFormatSelector.get_exporter("json")
        # Request XML exporter from factory using string argument 'xml'
        xml_exp = ExportFormatSelector.get_exporter("xml")

        # Assert returned object for 'json' is instance of JSONExporter class
        self.assertIsInstance(json_exp, JSONExporter)
        # Assert returned object for 'xml' is instance of XMLExporter class
        self.assertIsInstance(xml_exp, XMLExporter)

        # Context manager asserting ValueError exception is raised for invalid format
        with self.assertRaises(ValueError):
            # Pass unsupported format string 'csv' to verify exception handling
            ExportFormatSelector.get_exporter("csv")


if __name__ == "__main__":
    # Execute all test cases defined in TestCase classes
    unittest.main()
import json
import os
import tempfile
import unittest
import xml.etree.ElementTree as ET

from dormitory.exporters import ExportFormatSelector, JSONExporter, XMLExporter


class TestExporters(unittest.TestCase):
    """Unit tests for serializers and export factory."""

    def setUp(self):
        """Prepare sample dictionary dataset including a None value for XML bug verification."""
        self.test_data = [
            {"room_id": 1, "room_name": "Room #1", "student_count": 5, "empty_field": None}
        ]
        self.temp_output = tempfile.NamedTemporaryFile(delete=False)
        self.temp_output.close()

    def tearDown(self):
        """Clean up the temporary export output file."""
        if os.path.exists(self.temp_output.name):
            os.remove(self.temp_output.name)

    def test_json_exporter(self):
        """Verify JSONExporter serializes dictionaries into valid JSON format."""
        exporter = JSONExporter()
        exporter.export(self.test_data, self.temp_output.name)

        with open(self.temp_output.name, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertEqual(data, self.test_data)

    def test_xml_exporter(self):
        """Verify XMLExporter serializes dictionaries and correctly handles None values."""
        exporter = XMLExporter()
        exporter.export(self.test_data, self.temp_output.name)

        tree = ET.parse(self.temp_output.name)
        root = tree.getroot()

        self.assertEqual(root.tag, "results")

        items = root.findall("item")
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].find("room_id").text, "1")
        self.assertEqual(items[0].find("room_name").text, "Room #1")
        self.assertEqual(items[0].find("student_count").text, "5")

        # Verify that NULL (None) from the database is properly exported as an empty tag,
        # rather than the literal string "None"
        self.assertIsNone(items[0].find("empty_field").text)

    def test_export_format_selector(self):
        """Verify ExportFormatSelector factory instantiates matching exporters and raises ValueError."""
        json_exp = ExportFormatSelector.get_exporter("json")
        xml_exp = ExportFormatSelector.get_exporter("xml")

        self.assertIsInstance(json_exp, JSONExporter)
        self.assertIsInstance(xml_exp, XMLExporter)

        with self.assertRaises(ValueError):
            ExportFormatSelector.get_exporter("csv")


if __name__ == "__main__":
    unittest.main()
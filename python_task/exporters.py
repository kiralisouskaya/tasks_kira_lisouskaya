import json
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod


class BaseExporter(ABC):
    """Abstract base class defining the standard interface for all data exporters."""
    @abstractmethod
    def export(self, data: list[dict], output_path: str):
        """Define export method signature taking self, data dictionaries list, and target output path string"""
        pass


class JSONExporter(BaseExporter):
    """Exports query result dictionaries into formatted JSON files."""
    # Implement the export method to serialize list of dictionaries to JSON file format
    def export(self, data: list[dict], output_path: str):
        with open(output_path, "w", encoding="utf-8") as file:
            # Write list of dictionaries to file as JSON with 4-space indentation for readability
            json.dump(data, file, indent=4, ensure_ascii=False, default=str)


class XMLExporter(BaseExporter):
    """Exports query result dictionaries into formatted XML files."""
    def export(self, data: list[dict], output_path: str):
        """Implement the export method to serialize list of dictionaries to XML file format"""
        # Create the top-level root element for the XML document named results
        root = ET.Element("results")
        # Loop through every dictionary entry in the data list representing a database row
        for row in data:
            # Create a child element named item under the root results tag for each row
            item = ET.SubElement(root, "item")

            # Loop through key-value pairs inside each row dictionary
            for key, value in row.items():
                # Create a sub-element named after the dictionary key under the item tag
                child = ET.SubElement(item, str(key))
                # Set the text content of the sub-element to the string representation of the value
                child.text = str(value)

        # Indent the XML tree in-place so output file contains readable line breaks and spacing
        ET.indent(root, space="    ")

        # Build an ElementTree object wrapped around the root XML node
        tree = ET.ElementTree(root)
        tree.write(output_path, encoding="utf-8", xml_declaration=True)


class ExportFormatSelector:
    """Selects and returns the matching exporter object for JSON or XML."""
    @staticmethod
    def get_exporter(format_type: str) -> BaseExporter:
        """Define get_exporter method accepting format_type string and returning a BaseExporter instance"""
        # Convert format string to lowercase to handle inputs like JSON, Json, or XML safely
        fmt = format_type.lower()
        # Check if requested format is json
        if fmt == "json":
            # Instantiate and return a JSONExporter object
            return JSONExporter()
        # Check if requested format is xml
        elif fmt == "xml":
            # Instantiate and return an XMLExporter object
            return XMLExporter()
        # Raise ValueError if an unsupported format string was passed
        else:
            raise ValueError(f"Unsupported export format: {format_type}")
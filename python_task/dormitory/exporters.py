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
    def export(self, data: list[dict], output_path: str):
        with open(output_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False, default=str)


class XMLExporter(BaseExporter):
    """Exports query result dictionaries into formatted XML files."""
    def export(self, data: list[dict], output_path: str):
        root = ET.Element("results")

        for row in data:
            item = ET.SubElement(root, "item")
            for key, value in row.items():
                child = ET.SubElement(item, str(key))
                child.text = "" if value is None else str(value)

        ET.indent(root, space="    ")

        tree = ET.ElementTree(root)
        tree.write(output_path, encoding="utf-8", xml_declaration=True)


class ExportFormatSelector:
    """Selects and returns the matching exporter object for JSON or XML."""
    @staticmethod
    def get_exporter(format_type: str) -> BaseExporter:
        """Define get_exporter method accepting format_type string and returning a BaseExporter instance"""
        fmt = format_type.lower()

        if fmt == "json":
            return JSONExporter()
        elif fmt == "xml":
            return XMLExporter()
        else:
            raise ValueError(f"Unsupported export format: {format_type}")
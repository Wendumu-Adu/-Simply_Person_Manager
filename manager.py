import csv
import json
import xml.etree.ElementTree as ET
from pathlib import Path

class PersonManager:
    def __init__(self):
        self.persons = []
        self.data_dir = Path(__file__).resolve().parent / "data"
        self.data_dir.mkdir(exist_ok=True)

    def save_json(self, filename="persons.json"):
        filepath = self.data_dir / filename
        data = [{"name": p.name, "age": p.age, "email": p.email} for p in self.persons]
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def save_csv(self, filename="persons.csv"):
        filepath = self.data_dir / filename
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Name", "Age", "Email"]) 
            for p in self.persons:
                writer.writerow([p.name, p.age, p.email])

    def save_xml(self, filename="persons.xml"):
        filepath = self.data_dir / filename
        root = ET.Element("Persons")
        for p in self.persons:
            person_elem = ET.SubElement(root, "Person")
            ET.SubElement(person_elem, "Name").text = str(p.name)
            ET.SubElement(person_elem, "Age").text = str(p.age)
            ET.SubElement(person_elem, "Email").text = str(p.email)
        
        tree = ET.ElementTree(root)
        try:
            ET.indent(tree, space="  ")  
        except AttributeError:
            pass
        tree.write(filepath, encoding="utf-8", xml_declaration=True)
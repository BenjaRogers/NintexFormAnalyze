import xml.etree.ElementTree as ET
from ClassDefinitions.FieldClass import Field

# Workflow class to contain field reference objects
class WorkFlow:
    def __init__(self, filename: str):
        self.filename = filename
        self.field_elements = self.get_field_elements_list()
        self.field_objects = self.create_field_objects_list()

        self.num_fields = len(self.field_objects)

    # Parse workflow XML for field elements <FieldReference>
    def get_field_elements_list(self):
        tree = ET.parse(self.filename)
        root = tree.getroot()
        fields = root.findall(f"./ListReferences/ListReference/Fields/FieldReference")
        return fields

    # Iterate field elements and instantiate field objects
    def create_field_objects_list(self):
        field_objects = list()
        for field_element in self.field_elements:
            field_objects.append(Field(field_element))

        return field_objects

    # Replace with __str__ method
    def print_objects(self):
        for object in self.field_objects:
            print(object)

import xml.etree.ElementTree as ET
from ClassDefinitions.FieldClass import Field

class WorkFlow:
    def __init__(self, filename: str):
        self.filename = filename
        self.field_elements = self.get_field_elements_list()
        self.field_objects = self.create_field_objects_list()

        self.num_fields = len(self.field_objects)

    def get_field_elements_list(self):
        tree = ET.parse(self.filename)
        root = tree.getroot()
        fields = root.findall(f"./ListReferences/ListReference/Fields/FieldReference")
        return fields

    def TEST_ATTR(self):
        for field in self.field_elements:
            print(field.find("./InternalName").text)

    def create_field_objects_list(self):
        field_objects = list()
        for field_element in self.field_elements:
            field_objects.append(Field(field_element))

        return field_objects

    def print_objects(self):
        for object in self.field_objects:
            print(object)

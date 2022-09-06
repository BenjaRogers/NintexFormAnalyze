import xml.etree.ElementTree as ET


class Field:

    def __init__(self, element: ET):
        self.element = element
        self.internal_name = element.find("./InternalName").text
        self.display_name = element.find("./DisplayName").text
        self.type = element.find("./FieldType").text

    def __str__(self):
        string = f"{{\n" \
                 f"Internal Name : {self.internal_name}\n" \
                 f"Display Name : {self.display_name}\n" \
                 f"Type : {self.type}\n" \
                 f"}}\n \n"
        return string


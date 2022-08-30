import xml.etree.ElementTree as ET

formNS = '{http://schemas.datacontract.org/2004/07/Nintex.Forms}'
controlNS = '{http://schemas.datacontract.org/2004/07/Nintex.Forms.FormControls}'
controlIDNS = '{http://schemas.microsoft.com/2003/10/Serialization/Arrays}'

class Variable:

    def __init__(self, element: ET):
        self.expression = element.find(f"./{formNS}Expression").text
        self.id = element.find(f"./{formNS}Id").text
        self.name = element.find(f"./{formNS}Name").text
        self.type = element.find(f"./{formNS}Type").text
        self.connected = element.find(f"./{formNS}ConnectedTo").text

    def __str__(self):
        string = f"{{\n" \
                 f"Name : {self.name} \n" \
                 f"ID : {self.id} \n" \
                 f"Expression : {self.expression} \n" \
                 f"Connected : {self.connected} \n" \
                 f"Type : {self.type}\n" \
                 f"}}\n"

        return string
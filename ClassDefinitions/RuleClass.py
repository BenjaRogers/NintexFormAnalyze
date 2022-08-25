import xml.etree.ElementTree as ET

formNS = '{http://schemas.datacontract.org/2004/07/Nintex.Forms}'
controlNS = '{http://schemas.datacontract.org/2004/07/Nintex.Forms.FormControls}'
controlIDNS = '{http://schemas.microsoft.com/2003/10/Serialization/Arrays}'
class Rule:

    def __init__(self, element: ET):
        self.rule_type = element.find(f"./{formNS}RuleType").text
        self.title = element.find(f"./{formNS}Title").text
        self.expression_value = element.find(f"./{formNS}ExpressionValue").text
        self.control_id_list = list()

        self.element = element

        self.set_control_id_list()

        self.unique_id = element.find(f"./{formNS}Id").text

        self.element = None

    def set_control_id_list(self):
        control_elements = self.element.findall(f"./{formNS}ControlIds/")
        for each in control_elements:
            self.control_id_list.append(each.text)

    def __str__(self) -> str:
        string = f"{{\n"  \
                f"Type: {self.rule_type} \n" \
                f"ID: {self.unique_id} \n" \
                f"Title: {self.title} \n" \
                f"Expression : {self.expression_value} \n" \
                f"ID's : {self.control_id_list} \n}}"
        return string
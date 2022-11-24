import xml.etree.ElementTree as ET
import json
formNS = '{http://schemas.datacontract.org/2004/07/Nintex.Forms}'
controlNS = '{http://schemas.datacontract.org/2004/07/Nintex.Forms.FormControls}'
controlIDNS = '{http://schemas.microsoft.com/2003/10/Serialization/Arrays}'


# Variable objects for relevant Nintex form variable properties
class Variable:

    def __init__(self, element: ET):
        # self.expression = element.find(f"./{formNS}Expression").text - replaced by method set_variable_expression
        self.element = element
        self.expression = None
        self.id = element.find(f"./{formNS}Id").text
        self.name = element.find(f"./{formNS}Name").text
        self.type = element.find(f"./{formNS}Type").text
        self.connected = element.find(f"./{formNS}ConnectedTo").text
        self.set_variable_expression()

    # Summarization of variable properties when referenced by controls
    def get_occurrence_string(self):
        return f"{{Name: {self.name}, Type: {self.type}, Expression: {self.expression}}}"

    def get_occurrence_dict(self):
        return {"Name": self.name, "Type": self.type, "Expression": self.expression}

    # set expression value
    def set_variable_expression(self):
        expression_value = self.element.find(f"./{formNS}Expression").text
        clean_expression = expression_value.replace("&nbsp;", " ")
        clean_expression = clean_expression.replace("&amp;", "&")
        clean_expression = clean_expression.replace("&lt;", "<")
        clean_expression = clean_expression.replace("&le;", "<=")
        clean_expression = clean_expression.replace("&gt;", ">")
        clean_expression = clean_expression.replace("&ge;", ">=")

        self.expression = clean_expression
    # String representation of variable properties
    def __str__(self):
        # string = f"{{\n" \
        #          f"Name : {self.name} \n" \
        #          f"ID : {self.id} \n" \
        #          f"Expression : {self.expression} \n" \
        #          f"Connected : {self.connected} \n" \
        #          f"Type : {self.type}\n" \
        #          f"}}\n \n"
        #
        # return string
        return self.get_json_string()

    def get_json_string(self) -> str:
        dict = {
            "name": self.name,
            "id": self.id,
            "expression": self.expression,
            "connected": self.connected,
            "type": self.type
        }

        return json.dumps(dict, indent=4)

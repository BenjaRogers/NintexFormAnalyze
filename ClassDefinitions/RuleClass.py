import xml.etree.ElementTree as ET

formNS = '{http://schemas.datacontract.org/2004/07/Nintex.Forms}'
controlNS = '{http://schemas.datacontract.org/2004/07/Nintex.Forms.FormControls}'
controlIDNS = '{http://schemas.microsoft.com/2003/10/Serialization/Arrays}'

# Rule class for relevant Nintex rule properties - used to find if control is required for rule functionality
class Rule:

    def __init__(self, element: ET):
        self.rule_type = element.find(f"./{formNS}RuleType").text
        self.title = element.find(f"./{formNS}Title").text
        # self.expression_value = element.find(f"./{formNS}ExpressionValue").text - replaced by method set_rule_expression
        self.expression_value = None
        self.clean_expression_value = None
        self.hide = element.find(f"./{formNS}Hide").text
        self.disable = element.find(f"./{formNS}Disable").text
        self.control_id_list = list()
        self.control_name_list = list()
        self.element = element
        self.set_control_id_list()
        self.unique_id = element.find(f"./{formNS}Id").text
        self.set_rule_expression()


        self.element = None

    # Get list of controls this rule effects
    def set_control_id_list(self):
        control_elements = self.element.findall(f"./{formNS}ControlIds/")
        for each in control_elements:
            self.control_id_list.append(each.text)

    def set_control_name_list(self, control_object_list):
        for id in self.control_id_list:
            for control in control_object_list:
                if control.unique_id == id:
                    self.control_name_list.append(control.name)
                    break

    # Set rule expression value
    def set_rule_expression(self):
        expression_value = self.element.find(f"./{formNS}ExpressionValue").text
        self.expression_value = expression_value

        # Replace html special characters with literals
        if expression_value is not None:
            clean_expression = expression_value.replace("&nbsp;", " ")
            clean_expression = clean_expression.replace("&amp;", "&")
            clean_expression = clean_expression.replace("&lt;", "<")
            clean_expression = clean_expression.replace("&le;", "<=")
            clean_expression = clean_expression.replace("&gt;", ">")
            clean_expression = clean_expression.replace("&ge;", ">=")

            self.clean_expression_value = clean_expression

    # Summarization of rule properties for when it is referenced in control string representation
    def get_occurence_string(self) -> str:
        if self.rule_type == 'Formatting':
            return f"{{Name: {self.title}, Type: {self.rule_type}, Hide: {self.hide}, Disable: {self.disable}, Expression: {self.clean_expression_value}}}"

        if self.rule_type == 'Validation':
            return f"{{Name: {self.title}, Type: {self.rule_type}, Expression: {self.clean_expression_value}}}"

    # String representation of rule properties for writing to txt files & console
    def __str__(self) -> str:
        string = f"{{\n"  \
                f"type: {self.rule_type} \n" \
                f"id: {self.unique_id} \n" \
                f"title: {self.title} \n" \
                f"expression : {self.expression_value} \n" \
                f"clean expression : {self.clean_expression_value} \n" \
                f"effected control id's : {self.control_id_list} \n" \
                f"effected control names : {self.control_name_list} \n" \
                f"hide : {self.hide} \n " \
                f"disable : {self.disable} \n}} \n \n"
        return string
import xml.etree.ElementTree as ET
from ClassDefinitions.ControlClass import Control
from ClassDefinitions.RuleClass import Rule
from ClassDefinitions.VariableClass import Variable

class Form:

    def __init__(self, filename: str):
        self.formNS = '{http://schemas.datacontract.org/2004/07/Nintex.Forms}'
        self.controlNS = '{http://schemas.datacontract.org/2004/07/Nintex.Forms.FormControls}'
        self.filename = filename

        self.control_elements_list = self.get_control_elements_list()
        self.control_objects_list = self.create_control_objects_list()

        self.rule_elements_list = self.get_rule_elements_list()
        self.rule_objects_list = self.create_rule_objects_list()

        self.variable_elements_list = self.get_variable_elements_list()
        self.variable_objects_list = self.create_variable_objects_list()

        self.script = self.get_script()

    def get_script(self):
        tree = ET.parse(self.filename)
        root = tree.getroot()
        script = root.find(f"./{self.formNS}Script").text

        return script

    def get_control_elements_list(self):
        tree = ET.parse(self.filename)
        root = tree.getroot()
        data = ET.tostring(root)
        control_elements_list = root.findall(f"./{self.formNS}FormControls/{self.controlNS}FormControlProperties")

        return control_elements_list

    def create_control_objects_list(self):
        control_objects_list = list()
        for control_element in self.control_elements_list:
            control_objects_list.append(Control(control_element))

        return control_objects_list

    def get_rule_elements_list(self):
        tree = ET.parse(self.filename)
        root = tree.getroot()
        rules_elements_list = root.findall(f"./{self.formNS}Rules/{self.formNS}Rule")

        return rules_elements_list

    def create_rule_objects_list(self):
        rule_objects_list = list()
        for rule_element in self.rule_elements_list:
            rule_objects_list.append(Rule(rule_element))

        return rule_objects_list

    def get_variable_elements_list(self):
        tree = ET.parse(self.filename)
        root = tree.getroot()
        variable_elements_list = root.findall(f"./{self.formNS}UserFormVariables/{self.formNS}UserFormVariable")

        return variable_elements_list

    def create_variable_objects_list(self):
        variable_objects_list = list()
        for variable_element in self.variable_elements_list:
            variable_objects_list.append(Variable(variable_element))

        return variable_objects_list
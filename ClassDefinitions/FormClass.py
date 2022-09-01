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

        self.set_control_occurence_properties()

        self.unreferenced_controls = self.get_unreferenced_controls()
        self.unconnected_controls = self.get_unconnected_controls()
        self.uncon_unref_controls = self.get_unconnected_unreferenced_controls()

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

    def set_control_occurence_properties(self):
        for control in self.control_objects_list:
            control.get_control_occurences(self.control_objects_list)
            control.get_rule_occurences(self.rule_objects_list)

    def get_unreferenced_controls(self) -> list:
        unreferenced_controls = list()
        for control in self.control_objects_list:
            if len(control.control_formula_occurences) == 0 and len(control.control_sql_occurences) == 0 and \
                    len(control.rule_occurences) == 0 and control.simple_type == 'calculation':
                unreferenced_controls.append(control)

        return unreferenced_controls

    def get_unconnected_controls(self) -> list:
        unconnected_controls = list()
        for control in self.control_objects_list:
            if control.data_field is None and control.simple_type == "calculation":
                unconnected_controls.append(control)

        return unconnected_controls

    def get_unconnected_unreferenced_controls(self) -> list:
        uncon_unref = list()
        for control in self.unreferenced_controls:
            if control in self.unconnected_controls:
                uncon_unref.append(control)

        return uncon_unref

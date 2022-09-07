import xml.etree.ElementTree as ET
from ClassDefinitions.ControlClass import Control
from ClassDefinitions.RuleClass import Rule
from ClassDefinitions.VariableClass import Variable
from ClassDefinitions.WorkflowClass import WorkFlow

# Class to contain arrays of type Control, Rule, Field, Workflow and Variable and then do comparison
class Form:

    def __init__(self, form_filename: str, workflow_filenames: list):
        self.formNS = '{http://schemas.datacontract.org/2004/07/Nintex.Forms}'
        self.controlNS = '{http://schemas.datacontract.org/2004/07/Nintex.Forms.FormControls}'
        self.form_filename = form_filename
        self.workflow_filenames = workflow_filenames

        self.control_elements_list = self.get_control_elements_list()
        self.control_objects_list = self.create_control_objects_list()

        self.rule_elements_list = self.get_rule_elements_list()
        self.rule_objects_list = self.create_rule_objects_list()

        self.variable_elements_list = self.get_variable_elements_list()
        self.variable_objects_list = self.create_variable_objects_list()

        self.script = self.get_script()

        self.workflows = self.create_workflow()

        self.set_control_occurence_properties()

        self.unreferenced_controls = self.get_unreferenced_controls()
        self.unconnected_controls = self.get_unconnected_controls()
        self.uncon_unref_controls = self.get_unconnected_unreferenced_controls()

    # Parse form XML for script element @ script
    def get_script(self) -> str:
        tree = ET.parse(self.form_filename)
        root = tree.getroot()
        script = root.find(f"./{self.formNS}Script").text

        return script

    # Parse form XML for control elements <FormControlProperties> @ control_elements_list
    def get_control_elements_list(self) -> list:
        tree = ET.parse(self.form_filename)
        root = tree.getroot()
        data = ET.tostring(root)
        control_elements_list = root.findall(f"./{self.formNS}FormControls/{self.controlNS}FormControlProperties")

        return control_elements_list

    # Create list of Control objects @ control_objects_list
    def create_control_objects_list(self) -> list:
        control_objects_list = list()
        for control_element in self.control_elements_list:
            control_objects_list.append(Control(control_element))

        return control_objects_list

    # Parse form XML for rule elements <Rule> @ rule_elements_list
    def get_rule_elements_list(self) -> list:
        tree = ET.parse(self.form_filename)
        root = tree.getroot()
        rules_elements_list = root.findall(f"./{self.formNS}Rules/{self.formNS}Rule")

        return rules_elements_list

    # Create list of Rule objects @ rule_objects_list
    def create_rule_objects_list(self) -> list:
        rule_objects_list = list()
        for rule_element in self.rule_elements_list:
            rule_objects_list.append(Rule(rule_element))

        return rule_objects_list

    # Parse form XML for variable elements <UserFormVariable> @ variable_elements_list
    def get_variable_elements_list(self) -> list:
        tree = ET.parse(self.form_filename)
        root = tree.getroot()
        variable_elements_list = root.findall(f"./{self.formNS}UserFormVariables/{self.formNS}UserFormVariable")

        return variable_elements_list

    # Create List of Variable objects @ variable_objects_list
    def create_variable_objects_list(self) -> list:
        variable_objects_list = list()
        for variable_element in self.variable_elements_list:
            variable_objects_list.append(Variable(variable_element))

        return variable_objects_list

    # Create list of Workflow objects @ workflows
    def create_workflow(self) -> list:
        workflow_objects = list()
        for workflow_file in self.workflow_filenames:
            workflow_objects.append(WorkFlow(workflow_file))

        return workflow_objects

    # Iterate all controls and set control occurence properties in rules, variables, calculations, sql queries,
    # js script and associated SP column usage in workflows (still need to add wf occurence)
    def set_control_occurence_properties(self):
        for control in self.control_objects_list:
            control.get_control_occurences(self.control_objects_list, self.variable_objects_list)
            control.get_rule_occurences(self.rule_objects_list)
            control.get_script_occurences(self.script)

            for workflow in self.workflows:
                control.get_workflow_occurences(workflow.field_objects)

    # Create list of controls that are not referenced in rules, formulas or sql queries to write to txt files
    def get_unreferenced_controls(self) -> list:
        unreferenced_controls = list()
        for control in self.control_objects_list:
            if len(control.control_formula_occurences) == 0 and len(control.control_sql_occurences) == 0 and \
                    len(control.rule_occurences) == 0 and control.simple_type == 'calculation':
                unreferenced_controls.append(control)

        return unreferenced_controls

    # Create list of controls that are not connected to SP column to write to txt files
    def get_unconnected_controls(self) -> list:
        unconnected_controls = list()
        for control in self.control_objects_list:
            if control.data_field is None and control.simple_type == "calculation":
                unconnected_controls.append(control)

        return unconnected_controls

    # Create list of controls not referenced or connected to write to txt files
    def get_unconnected_unreferenced_controls(self) -> list:
        uncon_unref = list()
        for control in self.unreferenced_controls:
            if control in self.unconnected_controls:
                uncon_unref.append(control)

        return uncon_unref


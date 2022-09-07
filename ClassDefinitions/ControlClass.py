import xml.etree.ElementTree as ET
from ClassDefinitions.WorkflowClass import WorkFlow
""" CONTROL ID's
FormControlTypeUniqueId | i:type

c0a89c70-0781-4bd4-8623-f73675005e08 | d2p1:ImageFormControlProperties
c0a89c70-0781-4bd4-8623-f73675005e00 | d2p1:LabelFormControlProperties
c0a89c70-0781-4bd4-8623-f73675005e02 | d2p1:ChoiceFormControlProperties
c0a89c70-0781-4bd4-8623-f73675005e03 | d2p1:DateTimeFormControlProperties
c0a89c70-0781-4bd4-8623-f73675005e05 | d2p1:TextBoxFormControlProperties
c0a89c70-0781-4bd4-8623-f73675005e17 | d2p1:CalculationFormControlProperties
c0a89c70-0781-4bd4-8623-f73675005e06 | d2p1:MultiLineTextBoxFormControlProperties
c0a89c70-0781-4bd4-8623-f73675005e14 | d2p1:PanelFormControlProperties
c0a89c70-0781-4bd4-8623-f73675005e09 | d2p1:ButtonFormControlProperties
7733d5bf-11c6-4bdc-a430-79c3065a796c | d3p1:DataAccessFormControlProperties
c0a89c70-0781-4bd4-8623-f73675005e16 | d2p1:RepeaterFormControlProperties
c0a89c70-0781-4bd4-8623-f73675005e04 | d2p1:BooleanFormControlProperties
5f8b447a-4195-485b-9a04-477d7f24be73 | d3p1:AttachmentFormControlProperties
"""

"""
Class for controls
return string as jsonish - maybe make actual json?
"""
formNS = '{http://schemas.datacontract.org/2004/07/Nintex.Forms}'
controlNS = '{http://schemas.datacontract.org/2004/07/Nintex.Forms.FormControls}'
spControlNS = '{http://schemas.datacontract.org/2004/07/Nintex.Forms.SharePoint.FormControls}'

class Control:

    def __init__(self, element: ET):
        # Parse control type, unique ID, Name, and control type ID from XML element
        # ALL CONTROLS
        self.element = element
        self.typeC = element.attrib['{http://www.w3.org/2001/XMLSchema-instance}type']  # attrib type
        self.unique_id = element.find(f"./{controlNS}UniqueId").text  # element Unique ID
        self.name = element.find(f"{controlNS}Name").text  # element Name
        self.display_name = element.find(f"{controlNS}DisplayName").text
        self.control_id = element.find(f"{controlNS}FormControlTypeUniqueId").text  # element FormControlTypeUniqueID
        self.data_field = None
        self.jvar = None
        self.control_formula_occurences = list()
        self.control_sql_occurences = list()
        self.rule_occurences = list()
        self.variable_occurences = list()

        self.set_data_field()
        self.set_jvar()

        # Calc specific
        self.formula = None
        # DataAccess specific
        self.sql = None

        self.in_script = False
        self.in_workflow = False

        self.set_type_specific_properties()

        # Clear element attribute since it's been parsed
        self.element = None

    def set_type_specific_properties(self):
        if self.control_id == 'c0a89c70-0781-4bd4-8623-f73675005e08':
            self.simple_type = 'image'
        if self.control_id == 'c0a89c70-0781-4bd4-8623-f73675005e00':
            self.simple_type = 'label'
        if self.control_id == 'c0a89c70-0781-4bd4-8623-f73675005e02':
            self.simple_type = 'choice'
        if self.control_id == 'c0a89c70-0781-4bd4-8623-f73675005e03':
            self.simple_type = 'dateTime'
        if self.control_id == 'c0a89c70-0781-4bd4-8623-f73675005e05':
            self.simple_type = 'textBox'
        if self.control_id == 'c0a89c70-0781-4bd4-8623-f73675005e17':
            self.simple_type = 'calculation'
            self.set_calculation_control()
        if self.control_id == 'c0a89c70-0781-4bd4-8623-f73675005e06':
            self.simple_type = 'multiLine'
        if self.control_id == 'c0a89c70-0781-4bd4-8623-f73675005e14':
            self.simple_type = 'panel'
        if self.control_id == 'c0a89c70-0781-4bd4-8623-f73675005e09':
            self.simple_type = 'button'
        if self.control_id == '7733d5bf-11c6-4bdc-a430-79c3065a796c':
            self.simple_type = 'dataAccess'
            self.set_data_access()
        if self.control_id == 'c0a89c70-0781-4bd4-8623-f73675005e16':
            self.simple_type = 'repeater'
        if self.control_id == 'c0a89c70-0781-4bd4-8623-f73675005e04':
            self.simple_type = 'bool'
        if self.control_id == '5f8b447a-4195-485b-9a04-477d7f24be73':
            self.simple_type = 'attachment'

    def set_calculation_control(self):
        self.formula = self.element.find(f"{controlNS}Formula").text

    def set_data_access(self):
        self.sql = self.element.find(f"{spControlNS}SqlStatement").text

    def set_data_field(self):
        if self.element.find(f"{controlNS}DataFieldDisplayName") is not None:
            self.data_field = self.element.find(f"{controlNS}DataFieldDisplayName").text

    def set_jvar(self):
        if self.element.find(f"{controlNS}ExposedClientIdJavascriptVariable") is not None:
            self.jvar = self.element.find(f"{controlNS}ExposedClientIdJavascriptVariable").text

    def get_name(self) -> str:
        return self.name

    def get_unique_id(self) -> str:
        return self.unique_id

    def get_control_occurences(self, controls: list, variables: list):
        for control in controls:
            if control.formula is not None:
                if self.unique_id in control.formula:
                    self.control_formula_occurences.append(control.get_occurence_string('calc'))
            if control.sql is not None:
                if self.unique_id in control.sql:
                    self.control_sql_occurences.append(control.get_occurence_string('sql'))

        for variable in variables:
            if variable.expression is not None:
                if self.unique_id in variable.expression:
                    self.variable_occurences.append(variable.get_occurence_string())

    def get_rule_occurences(self, rules:list):
        for rule in rules:
            if rule.expression_value is not None:
                if self.unique_id in rule.expression_value:
                    self.rule_occurences.append(rule.get_occurence_string())

    def get_variable_occurences(self, variables:list):
        for variable in variables:
            if self.unique_id in variable.expression:
                self.variable_occurences.append(variable)

    def get_script_occurences(self, form_script: str):
        if self.jvar is not None:
            if self.jvar in form_script:
                self.in_script = True

    def get_workflow_occurences(self, field_references: list):
        for field in field_references:
            if self.data_field == field.display_name:
                self.in_workflow = True
                break


    def get_occurence_string(self, occurence_type: str) -> str:
        if occurence_type == 'calc':
            return f"{{Name: {self.name}, ID: {self.unique_id}, Formula: {self.formula}}}"

        if occurence_type == 'sql':
            return f"{{Name: {self.name}, ID: {self.unique_id}, SQL: {self.sql}}}"


    def __str__(self) -> str:
        string = f"{{\n"  \
                f"name : {self.name} \n" \
                f"unique id : {self.unique_id} \n" \
                f"control id : {self.control_id} \n" \
                f"type : {self.simple_type} \n" \
                f"formula : {self.formula} \n" \
                 f"sql : {self.sql} \n" \
                 f"Column Name : {self.data_field} \n" \
                 f"In Workflow : {self.in_workflow} \n" \
                 f"Rule Occurence : {self.rule_occurences} \n" \
                 f"Formula Occurence : {self.control_formula_occurences} \n" \
                 f"SQL Occurences : {self.control_sql_occurences} \n" \
                 f"Variable Occurences : {self.variable_occurences} \n" \
                 f"JavaScript Var : {self.jvar} \n" \
                 f"In Script : {self.in_script} \n" \
                 f"}}\n \n"

        return string

import xml.etree.ElementTree as ET
from ClassDefinitions.ControlClass import Control
from ClassDefinitions.RuleClass import Rule

formNS = '{http://schemas.datacontract.org/2004/07/Nintex.Forms}'
controlNS = '{http://schemas.datacontract.org/2004/07/Nintex.Forms.FormControls}'
# Parse xml for form control elements
def get_controls_list(filename: str) -> list:
    tree = ET.parse(filename)
    root = tree.getroot()
    data = ET.tostring(root)
    controls_list = root.findall(f"./{formNS}FormControls/{controlNS}FormControlProperties")

    return controls_list


# Call control constructor - probably doesnt need a method
def create_control_object(control_element: ET) -> Control:
    return Control(control_element)


# Parse XML for rule elements
def get_rule_list(filename: str) -> list:
    tree = ET.parse(filename)
    root = tree.getroot()
    rules_list = root.findall(f"./{formNS}Rules/{formNS}Rule")
    return rules_list


# Call Rule constructor - probably doesnt need to be a method
def create_rule_object(rule_element: ET) -> Rule:
    return Rule(rule_element)


# print list of children of root
def get_control_elements(filename: str):
    tree = ET.parse(filename)
    root = tree.getroot()
    data = ET.tostring(root)
    child_elements = root.findall(f"././{formNS}FormControls/{controlNS}FormControlProperties/")
    print(child_elements)


# get list of rules that have no control ID's in them
def get_unused_rules(rules_list: list) -> list:
    empty_rules = list()
    for rule in rules_list:
        if not rule.control_id_list:
            empty_rules.append(rule)

    return empty_rules


# Get formatting rules that don't hide or disable anything
def get_uneffective_rules(rules_list: list) -> list:
    une_rules = list()
    for rule in rules_list:
        if rule.hide == 'false' and rule.disable == 'false' and rule.rule_type == 'Formatting':
            une_rules.append(rule)

    return une_rules


# check if control has been referenced in control formulas, sql queries, or rule expressions
def get_unreferenced_controls(controls_list: list) -> list:
    unreferenced_controls = list()
    for control in controls_list:
        if len(control.control_formula_occurences) == 0 and len(control.control_sql_occurences)==0 and\
                len(control.rule_occurences) == 0 and control.simple_type == 'calculation':
            unreferenced_controls.append(control)

    return unreferenced_controls


# get list of controls that are not connected to sharepoint column
def get_unconnected_controls(controls_list: list) -> list:
    unconnected_controls = list()
    for control in controls_list:
        if control.data_field is None and control.simple_type == "calculation":
            unconnected_controls.append(control)

    return unconnected_controls


# get list of controls not referenced by form variables
def get_unreferenced_controls_vars(controls_list: list) -> list:
    unreferenced_controls = list()
    for control in controls_list:
        if len(control.variable_occurences) == 0 and control.simple_type != 'label':
            controls_list.append(control)

    return unreferenced_controls

# get list of controls that are not connected to sharepoint column &
def get_unconnected_unreferenced_controls(unconnected_list: list, unreferenced_list: list) -> list:
    uncon_unref = list()
    for control in unreferenced_list:
        if control in unconnected_list:
            uncon_unref.append(control)

    return uncon_unref

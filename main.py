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


# Random utility functions
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
        if rule.control_id_list == []:
            empty_rules.append(rule)

    return empty_rules

def get_unreferenced_controls(controls_list: list) -> list:
    unreferenced_controls = list()
    for control in controls_list:
        if len(control.control_formula_occurences) == 0 and len(control.control_sql_occurences)==0 and\
                len(control.rule_occurences) == 0 and control.simple_type == 'calculation':
            unreferenced_controls.append(control)
    return unreferenced_controls


def get_unconnected_controls(controls_list: list) -> list:
    unconnected_controls = list()
    for control in controls_list:
        if control.data_field is None and control.simple_type == "calculation":
            unconnected_controls.append(control)
    return unconnected_controls

def get_unconnected_unreferenced_controls(unconnected_list: list, unreferenced_list: list) -> list:
    uncon_unref = list()
    for control in unreferenced_list:
        if control in unconnected_list:
            uncon_unref.append(control)
    return uncon_unref

if __name__ == '__main__':

    input_filename = 'XML/IndividualTravelDev.xml'
    out_unused_rules = 'UnusedRules.txt'
    control_objects = list()
    rule_objects = list()

    # Parse all rule & control objects from XML file
    controls_list = get_controls_list(input_filename)
    rule_list = get_rule_list(input_filename)

    # Iterate xml ET to create list of control element objects -> ET
    for element in controls_list:
        control_objects.append(create_control_object(element))

    # Iterate xml ET to create list of rule element objects
    for element in rule_list:
        rule_objects.append(create_rule_object(element))

    # create list of rules with no associated controls
    unused_rules = get_unused_rules(rule_objects)

    # set occurence properties to control objects
    for control in control_objects:
        control.get_control_occurences(control_objects)
        control.get_rule_occurences(rule_objects)

    # create list of controls with no calc, sql associated controls & no connected sp column
    unreferenced_controls = get_unreferenced_controls(control_objects)
    unconnected_controls = get_unconnected_controls(control_objects)
    uncon_unref_controls = get_unconnected_unreferenced_controls(unconnected_controls, unreferenced_controls)


    print("Unreferenced controls:\n")
    for control in unreferenced_controls:
        print(control)
    print("############################################ \nUnconnected Controls\n")
    for control in unconnected_controls:
        print(control)
    print("############################################ \nUnconnected & Unreferenced Controls\n")
    for control in uncon_unref_controls:
        print(control)

    print(f"Unreferenced Length: {len(unreferenced_controls)}"
          f"Unconnected Length: {len(unconnected_controls)}"
          f"Unconnected & unreferenced length: {len(uncon_unref_controls)}")

    # for control in control_objects:
    #     print(control)
    # for unused_rule in unused_rules:
    #     print(unused_rule.title)



    print(len(rule_objects))
    print(len(control_objects))

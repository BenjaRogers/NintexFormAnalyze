import xml.etree.ElementTree as ET
from ClassDefinitions.ControlClass import Control
from ClassDefinitions.RuleClass import Rule
from utilities import *

formNS = '{http://schemas.datacontract.org/2004/07/Nintex.Forms}'
controlNS = '{http://schemas.datacontract.org/2004/07/Nintex.Forms.FormControls}'

def main2():
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

    print("Unused rules:\n")
    for rule in get_unused_rules(rule_objects):
        print(rule.title)
    print("Uneffective rules:\n")
    for rule in get_uneffective_rules(rule_objects):
        print(rule)
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

    for rule in rule_objects:
        print(rule)

    # for control in control_objects:
    #     print(control)
    # for unused_rule in unused_rules:
    #     print(unused_rule.title)



    print(len(rule_objects))
    print(len(control_objects))



if __name__ == '__main__':
    main2()


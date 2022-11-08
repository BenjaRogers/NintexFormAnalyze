import xml.etree.ElementTree as ET
from ClassDefinitions.ControlClass import Control
from ClassDefinitions.RuleClass import Rule
from ClassDefinitions.FormClass import Form
from utilities import *
import os

from ClassDefinitions.WorkflowClass import WorkFlow
formNS = '{http://schemas.datacontract.org/2004/07/Nintex.Forms}'
controlNS = '{http://schemas.datacontract.org/2004/07/Nintex.Forms.FormControls}'

def main2():
    # Add form xml file here
    input_filename = 'XML/Forms/TravelProd_194.xml'

    # File paths for output txt files
    output_directory = './output'

    # Open txt files
    out_all_rules = open(output_directory + '/AllRules.txt', 'w')
    out_ineffective_rules = open(output_directory + '/IneffectiveRules.txt', 'w')
    out_unused_rules = open(output_directory + '/UnusedRules.txt', 'w')
    out_all_controls = open(output_directory + '/AllControls.txt', 'w')

    # Strings to write to output files
    all_rules_str = ""
    ineffective_rules_str = ""
    unused_rules_str = ""
    all_controls_str = ""

    control_objects = list()
    rule_objects = list()


    # Parse all control, rule & variable elements from XML file
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
        all_controls_str += str(control)

    out_all_controls.write(all_controls_str)
    out_all_controls.close()

    # # create list of controls with no calc, sql associated controls & no connected sp column
    # unreferenced_controls = get_unreferenced_controls(control_objects)
    # unconnected_controls = get_unconnected_controls(control_objects)
    # uncon_unref_controls = get_unconnected_unreferenced_controls(unconnected_controls, unreferenced_controls)
    #
    # print("Unused rules:\n")
    # for rule in get_unused_rules(rule_objects):
    #     print(rule.title)
    # print("Uneffective rules:\n")
    # for rule in get_uneffective_rules(rule_objects):
    #     print(rule)
    # print("Unreferenced controls:\n")
    # for control in unreferenced_controls:
    #     print(control)
    # print("############################################ \nUnconnected Controls\n")
    # for control in unconnected_controls:
    #     print(control)
    # print("############################################ \nUnconnected & Unreferenced Controls\n")
    # for control in uncon_unref_controls:
    #     print(control)
    #
    # print(f"Unreferenced Length: {len(unreferenced_controls)}"
    #       f"Unconnected Length: {len(unconnected_controls)}"
    #       f"Unconnected & unreferenced length: {len(uncon_unref_controls)}")
    #
    # for rule in rule_objects:
    #     print(rule)
    #
    # for control in control_objects:
    #     print(control)
    # # for unused_rule in unused_rules:
    # #     print(unused_rule.title)



    print(len(rule_objects))
    print(len(control_objects))



if __name__ == '__main__':
    ## wf = WorkFlow("XML/Travel_Authorization_New.xml")
    #
    # input_form_filename = 'XML/Forms/TravelProd_194.xml'
    form_relative_path = "./XML/Forms"
    workflows_relative_path = "./XML/Workflows"
    # input_workflow_filenames = ["XML/Workflows/Authorization_Workflow_Complete.nwf", "XML/Workflows/Reimbursement_Workflow_Complete.nwf", "XML/Workflows/Test_TR_Review.nwf"]
    input_workflow_filenames = get_workflow_filepath(workflows_relative_path)
    input_form_filename = get_form_filepath(form_relative_path)
    output_directory = './output'

    # Open txt files
    out_all_rules = open(output_directory + '/AllRules.txt', 'w')
    # out_ineffective_rules = open(output_directory + '/IneffectiveRules.txt', 'w')
    # out_unused_rules = open(output_directory + '/UnusedRules.txt', 'w')

    out_all_controls = open(output_directory + '/AllControls.txt', 'w')
    out_unconnected_controls = open(output_directory + '/UnconnectedControls.txt', 'w')
    out_unreferenced_controls = open(output_directory + '/UnreferencedControls.txt', 'w')
    out_uncon_unref_controls = open(output_directory + '/UnconnectedUnreferencedControls.txt', 'w')
    out_all_vars = open(output_directory + '/AllVariables.txt', 'w')
    out_script = open(output_directory + '/Script.txt', 'w')

    out_all_fields = open(output_directory + '/AllFields.txt', 'w')

    # Strings to write to output files
    all_rules_str = ""
    ineffective_rules_str = ""
    unused_rules_str = ""

    all_controls_str = ""
    unconnected_controls_str = ""
    unreferenced_controls_str = ""
    uncon_unref_str = ""

    all_variables_str = ""

    all_fields_str = ""


    # Create form object
    form = Form(input_form_filename, input_workflow_filenames)

    # Create allcontrols string & write to file
    for variable in form.variable_objects_list:
        all_variables_str += str(variable)
    out_all_vars.write(all_variables_str)
    out_all_vars.close()

    # Create all_rules string & write to file
    for rule in form.rule_objects_list:
        all_rules_str += str(rule)
    out_all_rules.write(all_rules_str)
    out_all_vars.close()

    # Create all_controls string & write to file
    for control in form.control_objects_list:
        all_controls_str += str(control)
    out_all_controls.write(all_controls_str)
    out_all_controls.close()

    # Create unconnected_controls string & write to file
    for control in form.unconnected_controls:
        unconnected_controls_str += str(control)
    out_unconnected_controls.write(unconnected_controls_str)
    out_unconnected_controls.close()

    # Create unreferenced_controls string & write to file
    for control in form.unreferenced_controls:
        unreferenced_controls_str += str(control)
    out_unreferenced_controls.write(unreferenced_controls_str)
    out_unreferenced_controls.close()

    # Create unreferenced & unconnected controls string & write to file
    for control in form.uncon_unref_controls:
        uncon_unref_str += str(control)
    out_uncon_unref_controls.write(uncon_unref_str)
    out_uncon_unref_controls.close()

    # Create all_fields string and write to file
    # for field in wf.field_objects:
    #     all_fields_str += str(field)
    # out_all_fields.write(all_fields_str)
    # out_all_fields.close()

    if form.script is not None:
        out_script.write(form.script)
    out_script.close()







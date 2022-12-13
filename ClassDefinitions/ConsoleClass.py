from ClassDefinitions.FormClass import Form
from ClassDefinitions.ControlClass import Control
from treelib import Tree

class Console:
    def __init__(self, form: Form):
        self.form = form

    # Prompt id/name of control -> control json & referenced/occurrence trees until input == 0
    # CASE SENSITIVE
    def main_loop(self):
        inp = 1
        searched_control = None
        while inp != "0":
            inp = input("Enter control Name or ID: \n -> ")

            searched_control = self.search_control_object(inp)

            if searched_control:
                print(searched_control)

                # Build & print referenced/occurrence Trees for searched control
                control_id_list = list()
                control_id_referenced_list = list()

                print("\nTree of controls that searched control references:")
                print(self.build_control_referenced_tree_recursive(searched_control, control_id_list))
                print("\nTree of controls that reference searched control:")
                print(self.build_control_occurrence_tree_recursive(searched_control, control_id_referenced_list))

            else:
                if inp == "0":
                    print("Exit")
                else:
                    print("This control doesn't exist")

    def search_control_object(self, query: str) -> Control:
        for control in self.form.control_objects_list:
            if query == control.name or query == control.unique_id:
                return control

    # Build Tree for all controls that searched control uses in its calculation
    def build_control_referenced_tree_recursive(self, control_object: Control, control_id_list: list) -> Tree:
        tree = Tree()
        node_id = self.generate_node_id(control_id_list, control_object.unique_id)
        tree.create_node(control_object.name, node_id)

        if len(control_object.referenced_controls_id) > 0:
            for ref_control in control_object.referenced_controls_id:
                ref_control_object = self.search_control_object(ref_control)

                tree.paste(node_id, self.build_control_referenced_tree_recursive(ref_control_object, control_id_list))

        return tree

    # Build Tree for all controls that reference searched control in it's calculation.
    def build_control_occurrence_tree_recursive(self, control_object: Control, control_id_list: list) -> Tree:
        tree = Tree()
        node_id = self.generate_node_id(control_id_list, control_object.unique_id)
        tree.create_node(control_object.name, node_id)

        if len(control_object.control_occurrences_names) > 0:
            for ref_control in control_object.control_occurrences_id:
                ref_control_object = self.search_control_object(ref_control)

                tree.paste(node_id, self.build_control_occurrence_tree_recursive(ref_control_object, control_id_list))

        return tree

    # Generate unique id for node so control can be multiple nodes in same tree
    def generate_node_id(self, control_id_list: list, control_unique_id: str) -> str:
        if control_unique_id in control_id_list:
            id_count = control_id_list.count(control_unique_id)
            node_id = control_unique_id + f'({id_count + 1})'
            control_id_list.append(control_unique_id)
            return node_id

        control_id_list.append(control_unique_id)
        return control_unique_id

# create parent node
# get all children of parent
# create sub tree if there are children - else attach to parent
# once all sub trees are created attach to parent
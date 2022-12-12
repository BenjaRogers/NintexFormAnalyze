import ClassDefinitions.FormClass

# Check formulas for dropped brackets, parenthesis &
# Parent class for Control and rule linter
# Idk if this is really what linting is but I think it works in context
class Linter:
    def __init__(self, object_list: list, output_relative_path: str):
        self.object_list = object_list
        self.output_string = ""
        self.output_relative_path = output_relative_path

    def check_brackets(self, object_formula, object_clean_formula, object_name):
        open_bracket_count = object_formula.count('[')
        close_bracket_count = object_formula.count(']')

        if open_bracket_count > close_bracket_count:
            return f"//{object_name} missing closing bracket \n{object_name} = {object_clean_formula} \n"

        if open_bracket_count < close_bracket_count:
            return f"//{object_name} missing opening bracket \n{object_name} = {object_clean_formula} \n"

        return ""

    def check_parenthesis(self, object_formula, object_clean_formula, object_name):
        open_par = object_formula.count('(')
        close_par = object_formula.count(')')

        if open_par > close_par:
            return f"//{object_name} missing closing parenthesis \n{object_name} = {object_clean_formula} \n"

        if open_par < close_par:
            return f"//{object_name} missing opening parenthesis \n{object_name} = {object_clean_formula} \n"

        return ""

    def check_double_quote(self, object_formula, object_clean_formula, object_name):
        quote_count = object_formula.count('"')

        if quote_count % 2 == 0:
            return ""

        else:
            return f"//{object_name} missing double quotation mark \n{object_name} = {object_clean_formula} \n"

    def check_single_quote(self, object_formula, object_clean_formula, object_name):
        quote_count = object_formula.count("'")

        if quote_count % 2 == 0:
            return ""

        else:
            return f"//{object_name} missing single quotation mark \n{object_name} = {object_clean_formula} \n"

# Subclass of parent Linter, check for errors in calculation control formulas
class ControlLinter(Linter):
    def __init__(self, control_objects_list):
        super().__init__(control_objects_list, "./output/ControlErrors.js")

        output_file = open(self.output_relative_path, 'w')

        for object in self.object_list:
            if object.simple_type == "calculation":
                self.build_error_string(object)

        output_file.write(self.output_string)
        output_file.close()

    def build_error_string(self, object):
        self.output_string += str(self.check_brackets(object.formula, object.clean_formula, object.name))
        self.output_string += str(self.check_parenthesis(object.formula, object.clean_formula, object.name))
        self.output_string += str(self.check_double_quote(object.formula, object.clean_formula, object.name))
        self.output_string += str(self.check_single_quote(object.formula, object.clean_formula, object.name))

# Subclass of parent Linter, check for errors in rule expressions
class RuleLinter(Linter):
    def __init__(self, rule_objects_list):
        super().__init__(rule_objects_list, "./output/RuleErrors.js")

        output_file = open(self.output_relative_path, 'w')

        for object in self.object_list:
            if object.expression_value is not None:
                self.build_error_string(object)

        output_file.write(self.output_string)
        output_file.close()

    def build_error_string(self, object):
        self.output_string += str(self.check_brackets(object.expression_value, object.clean_expression_value, object.title))
        self.output_string += str(self.check_parenthesis(object.expression_value, object.clean_expression_value, object.title))
        self.output_string += str(self.check_double_quote(object.expression_value, object.clean_expression_value, object.title))
        self.output_string += str(self.check_single_quote(object.expression_value, object.clean_expression_value, object.title))
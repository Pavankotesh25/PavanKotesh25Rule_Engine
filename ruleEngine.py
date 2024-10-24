# Define a simple Node structure
class Node:
    def __init__(self, type, value=None, left=None, right=None):
        self.type = type
        self.value = value
        self.left = left
        self.right = right
        
    def __str__(self):
        if self.type == "operator":
            return f"({self.left} {self.value} {self.right})"
        return str(self.value)

# Parse condition strings into AST nodes
def parse_condition(condition):
    try:
        condition = condition.strip()  # Trim whitespace
        if ">" in condition:
            left, right = condition.split(">", 1)  # Split only at the first ">"
            return Node(type="operand", value=(">", left.strip(), right.strip()))
        elif "<" in condition:
            left, right = condition.split("<", 1)  # Split only at the first "<"
            return Node(type="operand", value=("<", left.strip(), right.strip()))
        elif "==" in condition:
            left, right = condition.split("==", 1)  # Split only at the first "=="
            return Node(type="operand", value=("==", left.strip(), right.strip()))
        elif "!=" in condition:
            left, right = condition.split("!=", 1)  # Split only at the first "!="
            return Node(type="operand", value=("!=", left.strip(), right.strip()))
        else:
            raise ValueError(f"Invalid condition format: {condition}")
    except ValueError as e:
        print(f"Error in parsing condition: {e}")
        return None

# Create a rule string into an AST
def create_rule(rule_string):
    try:
        rule_string = rule_string.strip()  # Trim whitespace
        # Split the rule string on logical operators
        if "AND" in rule_string:
            left, right = rule_string.split("AND", 1)
            left_node = create_rule(left.strip())
            right_node = create_rule(right.strip())
            return Node(type="operator", value="AND", left=left_node, right=right_node)
        elif "OR" in rule_string:
            left, right = rule_string.split("OR", 1)
            left_node = create_rule(left.strip())
            right_node = create_rule(right.strip())
            return Node(type="operator", value="OR", left=left_node, right=right_node)
        else:
            return parse_condition(rule_string)
    except Exception as e:
        print(f"Error in creating rule: {e}")
        return None

# Evaluate a rule against a data set
def evaluate_rule(ast, data):
    if ast is None:
        return False
    if ast.type == "operand":
        operator, left, right = ast.value
        left_val = data.get(left)

        # Strip quotes if the right value is a string (e.g., 'Sales' to Sales)
        right_val = right.strip("'").strip('"')  # Remove quotes around strings

        # Determine the type of right_val for comparison
        if right_val.isdigit():
            right_val = int(right_val)
        elif right_val.replace('.', '', 1).isdigit():
            right_val = float(right_val)

        # Handle left_val being a number
        if isinstance(left_val, (int, float)) and isinstance(right_val, (int, float)):
            if operator == ">":
                return left_val > right_val
            elif operator == "<":
                return left_val < right_val
            elif operator == "==":
                return left_val == right_val
            elif operator == "!=":
                return left_val != right_val
        elif isinstance(left_val, str) and isinstance(right_val, str):
            if operator == "==":
                return left_val == right_val
            elif operator == "!=":
                return left_val != right_val
            # Additional logic could be added for < or > on strings if needed
        else:
            print(f"TypeError: Invalid comparison between {type(left_val).__name__} and {type(right_val).__name__}")
            return False
    elif ast.type == "operator":
        left_result = evaluate_rule(ast.left, data)
        right_result = evaluate_rule(ast.right, data)
        if ast.value == "AND":
            return left_result and right_result
        elif ast.value == "OR":
            return left_result or right_result
    return False

# Combining multiple rules into a single AST with AND/OR logic
def combine_rules(rules, operator="AND"):
    try:
        if not rules:
            raise ValueError("No rules to combine")
        root = rules[0]
        for rule in rules[1:]:
            if root and rule:
                # Combine rules with the provided operator ("AND" or "OR")
                root = Node(type="operator", value=operator, left=root, right=rule)
            else:
                raise ValueError("Invalid rule in combination")
        return root
    except Exception as e:
        print(f"Error in combining rules: {e}")
        return None

# Testing the code

# Define individual rules
rule_string1 = "age > 30 AND department == 'Sales'"
rule_string2 = "salary > 50000 OR experience > 5"
rule_string3 = "age < 25 AND department == 'Marketing'"
invalid_rule = "age >> 30"  # Invalid rule for testing

# Create ASTs for the rules
ast1 = create_rule(rule_string1)
ast2 = create_rule(rule_string2)
ast3 = create_rule(rule_string3)
invalid_ast = create_rule(invalid_rule)

print("AST for rule 1:", ast1)
print("AST for rule 2:", ast2)
print("AST for rule 3:", ast3)

# Combine multiple rules with AND logic
combined_ast_and = combine_rules([ast1, ast2, ast3], operator="AND")
print("\nCombined AST with AND:", combined_ast_and)

# Combine multiple rules with OR logic
combined_ast_or = combine_rules([ast1, ast2, ast3], operator="OR")
print("\nCombined AST with OR:", combined_ast_or)

# Define sample user data
data = {"age": 35, "department": "Sales", "salary": 60000, "experience": 3}
data2 = {"age": 22, "department": "Marketing", "salary": 30000, "experience": 1}

# Evaluate the combined rule for the user data (AND)
result_and = evaluate_rule(combined_ast_and, data)
print(f"\nUser eligibility (for combined rules with AND): {result_and}")

# Evaluate the combined rule for the user data (OR)
result_or = evaluate_rule(combined_ast_or, data)
print(f"User eligibility (for combined rules with OR): {result_or}")

# Test with new data (AND and OR)
result2_and = evaluate_rule(combined_ast_and, data2)
print(f"User eligibility (for new data with AND): {result2_and}")

result2_or = evaluate_rule(combined_ast_or, data2)
print(f"User eligibility (for new data with OR): {result2_or}")

# Test the invalid rule
print("\nTesting invalid rule:")
if invalid_ast:  # Check if the AST for the invalid rule was created
    result_invalid = evaluate_rule(invalid_ast, data)
    print(f"Evaluation result for invalid rule: {result_invalid}")
else:
    print("Invalid rule AST was not created; skipping evaluation.")

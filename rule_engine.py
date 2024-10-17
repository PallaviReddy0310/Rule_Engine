import re


class Node:
    def __init__(self, node_type, left=None, right=None, value=None):
        self.type = node_type  # "operator" or "operand"
        self.left = left  # Left child (for operators)
        self.right = right  # Right child (for operators)
        self.value = value  # Value for operands

    def to_dict(self):
        """Convert the Node to a dictionary for serialization."""
        node_dict = {
            'type': self.type,
            'value': self.value
        }
        if self.left:
            node_dict['left'] = self.left.to_dict()
        if self.right:
            node_dict['right'] = self.right.to_dict()
        return node_dict

    @classmethod
    def from_dict(cls, node_dict):
        """Create a Node from a dictionary."""
        if node_dict is None:
            return None
        node_type = node_dict['type']
        value = node_dict.get('value')
        left = cls.from_dict(node_dict.get('left'))
        right = cls.from_dict(node_dict.get('right'))
        return cls(node_type, left, right, value)


def create_rule(rule_string):
    # Tokenize the input string
    tokens = re.split(r'(\sAND\s|\sOR\s|\(|\))', rule_string)
    tokens = [token.strip() for token in tokens if token.strip()]  # Clean up whitespace

    output_stack = []  # For the final AST nodes
    operator_stack = []  # For operators and parentheses

    def precedence(op):
        if op == 'AND':
            return 2
        elif op == 'OR':
            return 1
        return 0

    for token in tokens:
        if token == '(':
            operator_stack.append(token)
        elif token == ')':
            while operator_stack and operator_stack[-1] != '(':
                operator = operator_stack.pop()
                right = output_stack.pop()
                left = output_stack.pop()
                output_stack.append(Node('operator', left=left, right=right, value=operator))
            operator_stack.pop()  # Pop the '('
        elif token in ['AND', 'OR']:
            while (operator_stack and operator_stack[-1] != '(' and
                   precedence(operator_stack[-1]) >= precedence(token)):
                operator = operator_stack.pop()
                right = output_stack.pop()
                left = output_stack.pop()
                output_stack.append(Node('operator', left=left, right=right, value=operator))
            operator_stack.append(token)
        else:
            # This is an operand
            output_stack.append(Node('operand', value=token))

    # Remaining operators in the stack
    while operator_stack:
        operator = operator_stack.pop()
        right = output_stack.pop()
        left = output_stack.pop()
        output_stack.append(Node('operator', left=left, right=right, value=operator))

    return output_stack[0] if output_stack else None


def combine_rules(rules):
    if not rules:
        return None

    root = create_rule(rules[0])

    for rule_string in rules[1:]:
        new_rule_ast = create_rule(rule_string)
        root = Node('operator', left=root, right=new_rule_ast, value="AND")  # Combining with AND

    return root


def evaluate_rule(node, data):
    if node.type == 'operand':
        # Parse the condition (e.g., "age > 30") and evaluate it
        operand = node.value
        print(operand)
        field, op, value = re.split(r'([><=]+)', operand)
        field, value = field.strip(), value.strip()
        field_value = data.get(field)
        print(value, field_value)

        if op == '>':
            return field_value > int(value)
        elif op == '<':
            return field_value < int(value)
        elif op == '=':
            return field_value == value.strip("'")

    elif node.type == 'operator':
        if node.value == 'AND':
            return evaluate_rule(node.left, data) and evaluate_rule(node.right, data)
        elif node.value == 'OR':
            return evaluate_rule(node.left, data) or evaluate_rule(node.right, data)

    return False

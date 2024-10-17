# Step 1: Define the rules as strings
from database import store_rule, retrieve_rule
from rule_engine import create_rule, combine_rules, Node, evaluate_rule

rule1 = "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)"
rule2 = "((age > 30 AND department = 'Marketing')) AND (salary > 20000 OR experience > 5)"

# Step 2: Create the AST from the rules
ast_rule1 = create_rule(rule1)
ast_rule2 = create_rule(rule2)

# Check if the ASTs are created successfully
if not ast_rule1 or not ast_rule2:
    print("Error creating AST for one or both rules.")
else:
    print("ASTs created successfully.")

# Step 3: Combine the rules
combined_rule = combine_rules([rule1, rule2])

# Optional: Store the combined rule in the database
store_rule("combined_rule", "Combined rules for evaluation", combined_rule, {"author": "admin", "status": "active"})

# Step 4: Retrieve the rule from the database
retrieved_rule = retrieve_rule("combined_rule")
print("Retrieved Rule:", retrieved_rule)

# Convert the retrieved AST back to Node objects
ast_node = Node.from_dict(retrieved_rule['ast'])

# Step 5: Check if ast_node is valid before evaluating
if ast_node:
    # Sample data for testing
    sample_data = {
        "age": 35,               # Satisfies age > 30
        "department": 'Sales',    # Satisfies department = 'Sales'
        "salary": 60000,         # Satisfies salary > 50000
        "experience": 6          # Satisfies experience > 5
    }

    # Evaluate the rule with this sample data
    result = evaluate_rule(ast_node, sample_data)
    print("Evaluation Result:", result)  # Expected: True
else:
    print("Error: The AST structure is invalid.")

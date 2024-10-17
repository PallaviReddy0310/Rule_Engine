from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://localhost:27017/")
db = client.rule_engine


def store_rule(rule_id, description, ast, metadata):
    # Convert the AST to a dictionary using the `to_dict` method
    ast_dict = ast.to_dict() if ast else None

    # Check if the rule already exists
    existing_rule = db.rules.find_one({"_id": rule_id})

    if existing_rule:
        # Update the existing rule
        db.rules.update_one(
            {"_id": rule_id},
            {
                "$set": {
                    "description": description,
                    "ast": ast_dict,
                    "metadata": metadata
                }
            }
        )
        print(f"Updated rule with ID: {rule_id}")
    else:
        # Insert the new rule
        rule = {
            "_id": rule_id,
            "description": description,
            "created_at": datetime.utcnow(),
            "ast": ast_dict,
            "metadata": metadata
        }
        db.rules.insert_one(rule)
        print(f"Inserted new rule with ID: {rule_id}")


def retrieve_rule(rule_id):
    return db.rules.find_one({"_id": rule_id})


def modify_rule(rule_id, new_rule_string):
    from rule_engine import create_rule, Node
    # Create the new AST from the rule string
    new_ast = create_rule(new_rule_string)

    # Convert the new AST to a dictionary using the `to_dict` method
    new_ast_dict = new_ast.to_dict()

    # Update the existing rule in the database
    db.rules.update_one(
        {"_id": rule_id},
        {
            "$set": {
                "ast": new_ast_dict,  # Store the serialized AST here
                "description": "Updated rule for marketing"  # Optional: Update description if needed
            }
        }
    )


def delete_rule(rule_id):
    db.rules.delete_one({"_id": rule_id})

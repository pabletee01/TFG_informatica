import yaml as ym
import os
import sys
from mongodb.read_collection import read_habitat
from mongodb.create_collection import insert_habitat_curated
from cerberus import Validator

# Format that each category in the configuration file must follow:
SCHEMA = {
    "tag": {"type": "string", "required": True},
    "requirements": {
        "type": "list",
        "schema": {
            "type": "dict",
            "oneof_schema": [  
                {
                    "or": {
                        "type": "list",
                        "schema": {
                            "type": "dict",
                            "allowed": ["diet", "kingdom", "type", "order"],
                            "schema": {
                                "diet": {"type": "string"},
                                "kingdom": {"type": "string"},
                                "type": {"type": "string"},
                                "order": {"type": "string"}
                            }
                        }
                    }
                },
                {
                    "and": {
                        "type": "list",
                        "schema": {
                            "type": "dict",
                            "allowed": ["diet", "kingdom", "type"],
                            "schema": {
                                "diet": {"type": "string"},
                                "kingdom": {"type": "string"},
                                "type": {"type": "string"},
                                "order": {"type": "string"}
                            }
                        }
                    }
                }
            ]
        }
    },
    "relations": {
        "type": "list",
    }
}


# Loads engine configuration from yaml file on config/classifier.yaml
def engine_loader(classifier: str):
    filea = os.getcwd() + "/config/" + classifier
    with open(filea, 'r') as file:
        engine_data = ym.load(file, Loader=ym.FullLoader)

    # Empty configuration file
    if engine_data is None:
        return None

    v = Validator(SCHEMA)

    # Validating each category
    errors = []
    is_error_f = True
    for _ , details in engine_data.items():
        is_error = v.validate(details)
        if not is_error:
            is_error_f = False
            errors.append(v.errors.items())


    if is_error_f:
        return engine_data
    else:
        print("Validation errors:")
        for error in errors:
            for field, errors in error:
                print(f"- In {field}:", file=sys.stderr)
                for error in errors:
                    print(f"   {error}", file=sys.stderr)
            return None

    

# Classifies animals in the categories created on config/classifier.yaml
def classifier(c_name: str, cout_name: str, config_file: str):
    all_documents = read_habitat(c_name)

    engine_config = engine_loader(config_file)

    # Checking format errors in configuration file
    if engine_config == None:
        return False

    animal_list_curated = []

    n = 0

    # Iterating over each animal of the document
    for animal in all_documents:
        print(f"{n}: {animal}")

        diet = animal['diet'].split('|')

        animal['class'] = []

        print(diet)
        n += 1

        # Iterating over each category defined in configuration
        for category, details in engine_config.items():

            # Iterating over each rule 
            for rule in details['requirements']:
                rule_k = rule.keys()

                # Initializing flags
                flag_and = 0
                flag_or = 0

                # Or case
                if 'or' in rule_k:

                    flag_or = 0
                    for value in rule['or']:
                        key = list(value.keys())[0] # Obtaining key of the rule

                        if value[key] in animal[key]:
                            flag_or = 1
                # And case
                else:
                    
                    flag_and = 1
                    for value in rule['and']:
                        key = list(value.keys())[0] # Obtaining key of the rule

                        if value[key] not in animal[key]:
                            flag_and = 0
                
                if flag_or == 1:
                    animal['class'].append(category)

                if flag_and == 1:
                    animal['class'].append(category)
        
        print(animal)

        animal_list_curated.append(animal)

        # Inserting the habitat in the categorized database
        insert_habitat_curated(animal_list_curated, cout_name)
    return True

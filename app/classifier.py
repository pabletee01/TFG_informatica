import yaml as ym
import os
import sys
from mongodb.read_collection import read_habitat, read_habitat_curated
from mongodb.create_collection import insert_habitat_curated
from cerberus import Validator
from app.logger import logger

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
        logger.error("Validation errors:")
        for error in errors:
            for field, errors in error:
                logger.error(f"- In {field}:")
                for error in errors:
                    logger.error(f"   {error}")
            return None
        
# Validates a YAML file containing microhabitat classifications.
def engine_loader_habitat(filepath: str) -> bool:
    filea = os.getcwd() + "/config_habitat/" + filepath
    # Opening and loading configuration file
    with open(filea, "r", encoding="utf-8") as f:
        data = ym.safe_load(f)

    # Checking configuration structure
    if not isinstance(data, dict):
        raise ValueError("YAML root must be a dictionary.")

    expected_keys = {"terrestrial", "aquatic"}
    if set(data.keys()) != expected_keys:
        raise ValueError(f"YAML must contain exactly these keys: {expected_keys}")

    for key in expected_keys:
        if not isinstance(data[key], list):
            raise ValueError(f"The value of '{key}' must be a list.")
        for item in data[key]:
            if not isinstance(item, str):
                raise ValueError(f"All items in '{key}' must be strings.")

    return data

    

# Classifies animals in the categories created on config/classifier.yaml
def classifier(c_name: str, cout_name: str, config_file: str):
    all_documents = read_habitat(c_name)

    try:
        engine_config = engine_loader(config_file)
    except FileNotFoundError as e:
        logger.error(f"Error: configuration file not found {e}")
        return False


    # Checking format errors in configuration file
    if engine_config == None:
        return False

    animal_list_curated = []

    n = 0

    # Iterating over each animal of the document
    for animal in all_documents:
        logger.debug(f"{n}: {animal}")

        diet = animal['diet'].split('|')

        animal['class'] = []

        logger.debug(diet)
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
        
        logger.debug(animal)

        animal_list_curated.append(animal)

    # Inserting the habitat in the categorized database
    insert_habitat_curated(animal_list_curated, cout_name)
    return True


def classifier_habitat(c_name: str, c_out: str, habitat_config):
    all_documents = read_habitat_curated(c_name)
    
    animal_list_curated = []
    
    try:
        engine_config = engine_loader_habitat(habitat_config)
    except FileNotFoundError as e:
        logger.error(f"Error: configuration file not found {e}")
        return False
    
    if engine_config == None:
        return False
    
    n = 0
    
    for animal in all_documents:
        
        logger.debug(f"{n}: {animal}")
    
        animal['habitat'] = []
        
        # obtaining species' niche
        niche = animal['niche'].split('|')

        # Obtaining animals' habitat from configuration file
        for n in niche:
            if n in engine_config['terrestrial']:
                animal['habitat'].append('terrestial')
            if n in engine_config['aquatic']:
                animal['habitat'].append('aquatic')
         
        # deleting dulicates       
        animal['habitat'] = list(set(animal['habitat']))
                
        logger.debug(animal)

        animal_list_curated.append(animal)
        
    insert_habitat_curated(animal_list_curated, c_out)
    return True

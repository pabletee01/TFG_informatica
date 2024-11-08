import yaml as ym
import os
import json
from mongodb.read_collection import read_habitat
from mongodb.create_collection import insert_habitat_curated


# Loads engine configuration from yaml file on config/classifier.yaml
def engine_loader(classifier: str):
    filea = os.getcwd() + "/config/" + classifier
    with open(filea, 'r') as file:
        engine_data = ym.load(file, Loader=ym.FullLoader)

    print(json.dumps(engine_data, indent=2))
    return engine_data

# Classifies animals in the categories created on config/classifier.yaml
def classifier(c_name: str, cout_name: str, config_file: str):
    all_documents = read_habitat(c_name)

    engine_config = engine_loader(config_file)

    animal_list_curated = []

    n = 0

    # Iterating over each animal of the document
    for animal in all_documents:
        print(f"{n}: {animal}")

        diet = animal['diet'].split('|')

        animal['class'] = set()

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
                    animal['class'].add(category)

                if flag_and == 1:
                    animal['class'].add(category)
        
        print(animal)
        # Converting to list to make it work on mongodb
        animal['class'] = list(animal['class'])
        animal_list_curated.append(animal)

        # Inserting the habitat in the categorized database
        insert_habitat_curated(animal_list_curated, cout_name)





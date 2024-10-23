import yaml as ym
import os
import json
from mongodb.read_collection import read_habitat

def engine_loader():
    filea = os.getcwd() + "/config/classifier.yaml"
    with open(filea, 'r') as file:
        engine_data = ym.load(file, Loader=ym.FullLoader)

    print(json.dumps(engine_data, indent=2))
    return engine_data

def classifier(c_name: str, cout_name: str):
    all_documents = read_habitat(c_name)
    for document in all_documents:
        print(document)

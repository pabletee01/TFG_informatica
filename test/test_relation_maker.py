import pytest
import pymongo
from pprint import pprint
from app.classifier import classifier
from app.formatter import formatter
from app.classifier import classifier_habitat
from mongodb.complete_collection import clean_categories
from mongodb.complete_collection import clean_habitat
from mongodb.read_collection import read_habitat_curated
from app.relation_maker import calculate_relations
from app.matrix_maker import matrix_maker
from app.app import obtain_min_max_mass

@pytest.fixture(scope="function")
def mongo_db_non_curated():
 
    client = pymongo.MongoClient("mongodb://localhost:27017/")  
    db = client['ANMdb_non_curated']  
    collection = db["test_collection"]

    collection.delete_many({})
    yield db
    collection.delete_many({})

    client.close()  # Cerrar la conexión con la base de datos al finalizar la prueba

@pytest.fixture(scope="function")
def mongo_db_curated():

    client = pymongo.MongoClient("mongodb://localhost:27017/")  
    db = client['ANMdb_curated']
    collection = db["test_collection"]
    collection2 = db["test_collection2"]

    collection.delete_many({})
    collection2.delete_many({})
    yield db
    collection.delete_many({})
    collection2.delete_many({})

    client.close()  # Cerrar la conexión con la base de datos al finalizar la prueba

# Method used in the tests to determine if they pass or not 
def AUX_method(csv_file: str, C :float, iter: int, white_list: dict, black_list: dict):
    
    # Loading habitat
    formatter(csv_file, "test_collection")

    classifier("test_collection", "test_collection", "classifier.yaml")
    
    classifier_habitat("test_collection","test_collection2", "habitat_configuration.yaml")
    
    clean_categories('test_collection2')
    clean_habitat('test_collection2')
    
    # Obtaining all species' names
    
    names = []
    
    habitat_names = read_habitat_curated('test_collection2')
    
    for l_being in habitat_names:
        print(l_being)
        names.append(l_being['name'])
        
    print(names)
    
    print(f"white list: {white_list}")
    print(f"black list: {black_list}")
    
    white_list_keys = list(white_list.keys())
    
    black_list_flag = False
    
    # Testing the dictionaries

    # white list
    for x in range(iter):
        habitat = read_habitat_curated('test_collection2')
        matrix_h = matrix_maker("classifier.yaml")
        final_matrix = []
        min, max = obtain_min_max_mass('test_collection2')
        for l_being in habitat:
            relations = []
            habitataux = read_habitat_curated('test_collection2')
            calculate_relations(l_being, matrix_h, relations, habitataux, C, max, min)
            l_being_set = (l_being['name'], relations)
            final_matrix.append(l_being_set)

        # Testing white list
        white_list_keys_aux = white_list_keys.copy()
        for key in white_list_keys_aux:
            wl = white_list[key]
            
            list_numbers = []
            
            for name in wl:
                list_numbers.append(names.index(name))

            list_relations = []
            
            for name in final_matrix:
                if name[0] == key:
                    list_relations = name[1]
            
            list_numbers_aux = list_numbers.copy()
            
            for n in list_numbers_aux:
                if len(list_relations) > 0:
                    if list_relations[n][2] == 1:
                        index = list_numbers.index(n)
                        list_numbers.remove(n)
                        print(wl, index)
                        elem = wl[index]
                        wl.remove(elem)
                    
            print(list_numbers)
            
            if list_numbers == []:
                white_list_keys.remove(key)
            else:
                white_list[key]=wl.copy()
            
        # Testing black list
        for key in black_list.keys():
            bl = black_list[key]
            
            list_numbers = []
            
            for name in bl:
                list_numbers.append(names.index(name))
            
            for name in final_matrix:
                if name[0] == key:
                    list_relations = name[1]
            
            print(list_relations)
            print(bl)
            print(list_numbers)
            
            list_numbers_aux = list_numbers.copy()
            
            for n in list_numbers_aux:
                if list_relations[n][2] == 1:
                    black_list_flag = True
                    
    
    print(white_list)
    print(white_list_keys)
    print(black_list_flag)
    return True if len(white_list_keys) == 0 and not(black_list_flag) else False

# Method used in the tests to show frequencies of the relations made by the algorithm
def AUX_method_frequencies(csv_file: str, C :float, iter: int, white_list: dict, file: str):
    
    # Loading habitat
    formatter(csv_file, "test_collection")

    classifier("test_collection", "test_collection", "classifier.yaml")
    
    classifier_habitat("test_collection","test_collection2", "habitat_configuration.yaml")
    
    clean_categories('test_collection2')
    clean_habitat('test_collection2')
    
    # Obtaining all species' names
    
    names = []
    
    habitat_names = read_habitat_curated('test_collection2')
    
    for l_being in habitat_names:
        print(l_being)
        names.append(l_being['name'])
        
    print(names)
    
    print(f"white list: {white_list}")
    
    white_list_keys = list(white_list.keys())
    
    result_d = {}
    
    # Creating final dictionary
    for wlk in white_list_keys:
        result_d[wlk] = []
        for target in white_list[wlk]:
            result_d[wlk].append([target, 0])

    
    print(result_d)
    # Testing the dictionaries

    # white list
    for x in range(iter):
        habitat = read_habitat_curated('test_collection2')
        matrix_h = matrix_maker("classifier.yaml")
        final_matrix = []
        min, max = obtain_min_max_mass('test_collection2')
        for l_being in habitat:
            relations = []
            habitataux = read_habitat_curated('test_collection2')
            calculate_relations(l_being, matrix_h, relations, habitataux, C, max, min)
            l_being_set = (l_being['name'], relations)
            final_matrix.append(l_being_set)

        # Obtaining frequencies
        white_list_keys_aux = white_list_keys.copy()
        for key in white_list_keys_aux:
            wl = white_list[key]
            
            list_numbers = []

            list_relations = []
            
            for name in wl:
                list_numbers.append(names.index(name))
            
            for name in final_matrix:
                if name[0] == key:
                    list_relations = name[1]
            
            #print(list_relations)
            #print(wl)
            #print(list_numbers)
            
            list_numbers_aux = list_numbers.copy()
            
            # Contar aquí
            for n in list_numbers_aux:
                if len(list_relations) > 0:
                    if list_relations[n][2] == 1:
                        index = list_numbers.index(n)
                        print(wl, index)
                        result_d[key][index][1] += 1
                    
            #print(list_numbers)

                    
    with open(file, "w") as f:
        pprint(result_d, f)

    return True

def test_relation_maker_ok(mongo_db_non_curated, mongo_db_curated):
    white_list = {
        "Bacteria2": ["Bacteria1", "Bacteria3"],
    }
    black_list = {
        "Bacteria3": ["Bacteria1", "Bacteria2"]
    }

    assert AUX_method("test_ok.csv",1,100, white_list, black_list)

# Checking if not related by category organisms create relations
def test_relation_maker_not_related_category(mongo_db_non_curated, mongo_db_curated):
    black_list = {
        "Bacteria2": ["Bacteria1"],
        "Bacteria3": ["Bacteria4"]
    }
    
    assert AUX_method("test1.csv",1,100,{},black_list)

# Checking if organisms living in distinct niches predate each other
def test_relation_maker_different_niche_never_related(mongo_db_non_curated, mongo_db_curated):

    white_list = {
        "Bacteria5": ["Bacteria1", "Bacteria2"]
    }

    black_list = {
        "Bacteria3": ["Bacteria1", "Bacteria2"],
        "Bacteria4": ["Bacteria1", "Bacteria2"]
    }

    assert AUX_method("test2.csv",1,100,white_list,black_list)
    

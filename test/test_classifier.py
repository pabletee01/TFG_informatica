import pytest
import pymongo
from app.classifier import classifier
from app.formatter import formatter

# Test MongoDB Database for integration testing purposes
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

    collection.delete_many({})
    yield db
    collection.delete_many({})

    client.close()  # Cerrar la conexión con la base de datos al finalizar la prueba

# Insert one habitat
def test_classifier_ok(mongo_db_non_curated, mongo_db_curated):

    formatter("Zona-0_Las_Hoyas-C1.csv", "test_collection")

    result = classifier("test_collection", "test_collection", "classifier.yaml")

    # Getting number of lines in the curated collection
    collection = mongo_db_curated["test_collection"]
    inserted_data = list(collection.find({}))

    # 159 lines in Zona-0_Las_Hoyas-C1.csv 
    assert len(inserted_data) == 159 and result == True

# Wrong format in configuration file
def test_classifier_wrong_format_of_config_file(mongo_db_non_curated, mongo_db_curated, capfd):
    formatter("Zona-0_Las_Hoyas-C1.csv", "test_collection")

    result = classifier("test_collection", "test_collection", "classifier_wrong_format.yaml")

    # Getting number of lines in the curated collection
    collection = mongo_db_curated["test_collection"]
    inserted_data = list(collection.find({}))

    # 0 lines in Zona-0_Las_Hoyas-C1.csv 
    assert len(inserted_data) == 0 and result == False

# Empty engine configuration file.
def test_classifier_empty_config_file(mongo_db_non_curated, mongo_db_curated, capfd):
    formatter("Zona-0_Las_Hoyas-C1.csv", "test_collection")

    result = classifier("test_collection", "test_collection", "classifier_empty.yaml")

    # Getting number of lines in the curated collection
    collection = mongo_db_curated["test_collection"]
    inserted_data = list(collection.find({}))

    # 0 lines in Zona-0_Las_Hoyas-C1.csv 
    assert len(inserted_data) == 0 and result == False
    
# Non existent configuration file
def test_classifier_non_existent_config_file(mongo_db_non_curated, mongo_db_curated, capfd):
    formatter("Zona-0_Las_Hoyas-C1.csv", "test_collection")

    result = classifier("test_collection", "test_collection", "classifier_wrong_name.yaml")

    # Getting number of lines in the curated collection
    collection = mongo_db_curated["test_collection"]
    inserted_data = list(collection.find({}))

    # 0 lines in Zona-0_Las_Hoyas-C1.csv 
    assert len(inserted_data) == 0 and result == False
import pytest
import pymongo
from app.formatter import formatter

# Testing module of the method used to store csv information in the mongoDB database

# Test MongoDB Database for integration testing purposes
@pytest.fixture(scope="function")
def mongo_db():

    client = pymongo.MongoClient("mongodb://localhost:27017/")  
    db = client['ANMdb_non_curated']  
    collection = db["test_collection"]

    collection.delete_many({})
    yield db
    collection.delete_many({})

    client.close()  # Cerrar la conexión con la base de datos al finalizar la prueba

# Insert one habitat
def test_formatter_ok(mongo_db):

    result = formatter("Zona-0_Las_Hoyas-C1.csv", "test_collection")

    collection = mongo_db["test_collection"]
    inserted_data = list(collection.find({}))

    # 159 lines in Zona-0_Las_Hoyas-C1.csv
    assert len(inserted_data) == 159 and result == True

# Insert two habitats on the same collection
def test_formatter_various_inserts_ok(mongo_db):

    formatter("Zona-0_Las_Hoyas-C1.csv", "test_collection")
    result = formatter("Zona-0_Las_Hoyas-C1.csv", "test_collection")

    collection = mongo_db["test_collection"]
    inserted_data = list(collection.find({}))

    # 159 lines in Zona-0_Las_Hoyas-C1.csv, non repeated lines
    assert len(inserted_data) == 159 and result == True

# Non existent CSV file test
def test_formatter_wrong_csv_filename(mongo_db, capfd):

    result = formatter("Non_existent_file.csv", "test_collection")

    strerr = str(capfd.readouterr().err)
    expected = "Non_existent_file.csv not found in data/habitats directory\n"
    # 159 lines in Zona-0_Las_Hoyas-C1.csv
    assert strerr == expected and result == False

# Wrong format in the first line of CSV
def test_formatter_wrong_csv_format_in_header(mongo_db, capfd):

    result = formatter("Zona-0_Las_Hoyas-C1_wrong_format_in_header.csv", "test_collection")

    strerr = str(capfd.readouterr().err)

    # The formatter function must return error.
    assert result == False and "Unexpected error while reading" in strerr

# Wrong format in any line of the CSV file except the first one
def test_formatter_wrong_csv_format(mongo_db, capfd):

    result = formatter("Zona-0_Las_Hoyas-C1_wrong_format.csv", "test_collection")

    strerr = str(capfd.readouterr().err)

    # The formatter function must return error.
    assert result == False and "Unexpected error while reading" in strerr

# Non Integer values in fields weight and size
def test_formatter_non_float_values(mongo_db, capfd):
    result = formatter("Zona-0_Las_Hoyas-C1_non_float_values.csv", "test_collection")

    strerr = str(capfd.readouterr().err)

    assert result == False and "could not convert string to float:" in strerr
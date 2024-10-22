import pymongo

# Method used to store habitats in the mongodb database
def insert_habitat(habitat: list, name: str):

    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['ANMdb_non_curated']
    collection = db[name]

    for animal in habitat:
        insert_result = collection.insert_one(animal)

    return
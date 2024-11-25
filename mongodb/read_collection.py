import pymongo

# Method used to read habitats in the mongodb database
def read_habitat(name: str):

    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['ANMdb_non_curated']
    collection = db[name]

    all_documents = collection.find({})

    return all_documents


def read_habitat_curated(name: str):

    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['ANMdb_curated']
    collection = db[name]

    all_documents = collection.find({})

    return all_documents
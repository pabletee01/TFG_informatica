import pymongo

# Method used to read habitats in the mongodb database
def read_habitat(name: str):

    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['ANMdb_non_curated']
    collection = db[name]

    # Delete the collection in case there's data
    all_documents = collection.find({})

    return all_documents
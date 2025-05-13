import pymongo

def copy_habitat_curated(name_in: str, name_out: str):

    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['ANMdb_curated']
    
    collection_origin = db[name_in]
    collection_destiny = db[name_out]

    # Delete the collection in case there's data
    collection_destiny.delete_many({})

    docs = collection_origin.find()
    

    collection_destiny.insert_many(docs)

    return
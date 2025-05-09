import pymongo

def update_category(name: str, id, category: str):
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['ANMdb_curated']
    collection = db[name]
    
    final = []
    final.append(category)
    # Updating collection with new class
    collection.update_one(
            {"_id": id},
            {"$set": {"class": final}}
        )
    
def update_habitat(name: str, id, habitat: str):
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['ANMdb_curated']
    collection = db[name]
    
    final = []
    final.append(habitat)
    # Updating collection with new class
    collection.update_one(
            {"_id": id},
            {"$set": {"habitat": final}}
        )
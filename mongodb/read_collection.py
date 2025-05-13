import pymongo
from collections import Counter
from app.logger import logger

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

def read_habitat_no_category(name: str):

    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['ANMdb_curated']
    collection = db[name]

    all_documents = collection.find({"class": []})

    return all_documents

def read_habitat_no_habitats(name: str):

    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['ANMdb_curated']
    collection = db[name]

    all_documents = collection.find({"habitat": []})

    return all_documents

def read_habitat_from_type(name: str,type_key: str, type: str):
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['ANMdb_curated']
    collection = db[name]
    
    all_documents = collection.find({
        type_key: type,
        "class": {"$ne": []}
    })
    
    category_counter = Counter()
    
    for doc in all_documents:
        categories = doc.get("class", [])
        category_counter.update(categories)
    
    # Picking the most frequent category    
    if category_counter:   
        categoria = category_counter.most_common(1)[0][0]
        return categoria
    
    return None


def read_habitat_from_type_niche(name: str, type_key: str, type: str):
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['ANMdb_curated']
    collection = db[name]
    
    all_documents = collection.find({
        type_key: type,
        "habitat": {"$ne": []}
    })
    
    category_counter = Counter()
    
    for doc in all_documents:
        categories = doc.get("habitat", [])
        logger.debug(categories)
        category_counter.update(categories)
        
    
    logger.debug(category_counter)
    # Picking the most frequent category    
    if category_counter:   
        categoria = category_counter.most_common(1)[0][0]
        return categoria
    
    return None

    
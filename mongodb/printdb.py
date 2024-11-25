import pymongo
from create_collection import insert_relation_matrix

# Conectar al servidor de MongoDB en localhost
"""client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["ANMdb_non_curated"]
collection = db["Zona-0_Las_Hoyas-C1"]

# Consultar un documento
for item in collection.find():
    print(item)

client.close()"""

habitat = \
[
    [1,2,3],
    [4,5,6],
    [7,8,9]         
]

insert_relation_matrix(habitat, "test")

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["ANMdb_matrix"]
collection = collection = db["test"]

for item in collection.find():
    print(item['matrix'])

collection.delete_many({})

client.close()

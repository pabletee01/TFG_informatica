import pymongo

import pymongo

# Conectar al servidor de MongoDB en localhost
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["ANMdb_non_curated"]
collection = db["Zona-0_Las_Hoyas-C1"]

# Consultar un documento
for item in collection.find():
    print(item)

client.close()
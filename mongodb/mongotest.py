import pymongo

# Conectar al servidor de MongoDB en localhost
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["test"]
collection = db["testCollection"]

# Insertar un documento en la colección
document = {"nombre": "Juan", "edad": 30}
insert_result = collection.insert_one(document)
print(f'Documento insertado con ID: {insert_result.inserted_id}')

# Consultar un documento
for item in collection.find():
    print(item)



client.close()
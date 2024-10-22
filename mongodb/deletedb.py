import pymongo

# Conectar al servidor de MongoDB en localhost
client = pymongo.MongoClient("mongodb://localhost:27017/")

# Acceder a la base de datos "test"
db = client["test"]

# Acceder a la colección "testCollection"
collection = db["testCollection"]

# Borrar todos los documentos de la colección
delete_result = collection.delete_many({})  # Un diccionario vacío elimina todos los documentos
print(f'Documentos eliminados: {delete_result.deleted_count}')

# Cerrar la conexión
client.close()

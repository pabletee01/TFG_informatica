import pymongo
from app.logger import logger
# Conectar al servidor de MongoDB en localhost
client = pymongo.MongoClient("mongodb://localhost:27017/")

# Acceder a la base de datos "test"

db = client["ANMdb_non_curated"]

# Acceder a la colección "testCollection"
collection = db["Zona-0_Las_Hoyas-C1"]

# Borrar todos los documentos de la colección
delete_result = collection.delete_many({})  # Un diccionario vacío elimina todos los documentos
logger.debug(f'Documentos eliminados: {delete_result.deleted_count}')

# Cerrar la conexión
client.close()

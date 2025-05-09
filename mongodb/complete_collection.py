from app.logger import logger
from mongodb.read_collection import read_habitat_no_category
from mongodb.read_collection import read_habitat_no_habitats 
from mongodb.read_collection import read_habitat_from_type
from mongodb.read_collection import read_habitat_from_type_niche
from mongodb.read_collection import read_habitat_curated
from mongodb.update_collection import update_category
from mongodb.update_collection import update_habitat

# Function to complete organism's categories with similar ones
def clean_categories(name: str):
    logger.info("Completing categories")
    
    # looking for uncategorized organisms
    habitat = list(read_habitat_no_category(name))
       

    # Checking for type simmilarities in a loop of increasing generality
    for lb in habitat:
        logger.info(f"Animal {lb['name']}")
        for type_key in ["type3", "type2", "type"]:
            similars = None
            tipo = lb[type_key]
            # This read has to be from an auxiliar collection
            similars = read_habitat_from_type(name, type_key, tipo)
            
            if similars:
                break
        logger.info(f"Similars {similars}")  
        # if similars dict has some categories, the blank gets filled with the most frequent
        if similars:
            update_category(name,lb['_id'],similars)
            logger.info(f"Updated {lb['name']} with {similars} category.")
            
    
        
    


# Funtion to complete organim's habitats with similar ones
def clean_habitat(name: str):
    logger.info("Completing habitats")

    # Looking for organisms with no habitat
    habitat = list(read_habitat_no_habitats(name))

    # Checking for type simmilarities in a loop of increasing generality
    for lb in habitat:
        logger.info(f"Animal {lb['name']}")
        for type_key in ["type3", "type2", "type"]:
            similars = None
            tipo = lb[type_key]
            # This read has to be from an auxiliar collection
            similars = read_habitat_from_type_niche(name, type_key, tipo)

            if similars:
                break
        logger.info(f"Similars {similars}")    
        if similars:
            update_habitat(name,lb['_id'],similars)
            logger.info(f"Updated {lb['name']} with {similars} habitat.")


from app.classifier import engine_loader
from app.logger import logger

def matrix_maker(config_file: str):

    try:
        config = engine_loader(config_file)
    except FileNotFoundError as e:
        logger.error(f"Error: configuration file not found")
        return False
    except Exception as e:
        logger.error(f"Unexpected error while loading the configuration file: {e}")
        return False

    if config == None:
        return False

    categories = []

    matrix = {}
    
    for category, _ in config.items():
        categories.append(category)
        matrix[category] = {}

    logger.debug(categories)

    for category, details in config.items():
        if 'relations' in details.keys():
            for element in details['relations']:
                # Key del elemento
                key = list(element.keys())[0]
                matrix[category][key] = element[key]

    logger.debug(matrix)
    return matrix
 
    
from app.classifier import engine_loader

def matrix_maker(config_file: str):

    try:
        config = engine_loader(config_file)
    except FileNotFoundError as e:
        print(f"Error: configuration file not found")
        return False
    except Exception as e:
        print(f"Unexpected error while loading the configuration file: {e}")
        return False

    if config == None:
        return False

    categories = []

    matrix = {}
    
    for category, _ in config.items():
        categories.append(category)
        matrix[category] = {}

    print(categories)

    for category, details in config.items():
        if 'relations' in details.keys():
            for element in details['relations']:
                # Key del elemento
                key = list(element.keys())[0]
                matrix[category][key] = element[key]

    print(matrix)
    return matrix
 
    
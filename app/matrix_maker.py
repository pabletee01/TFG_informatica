from mongodb.read_collection import read_habitat_curated

def matrix_maker(c_name: str, cout_name: str, config_file: str):

    
    habitat = read_habitat_curated(c_name)
    
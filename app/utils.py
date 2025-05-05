import pandas as pd
import random as rn
from app.formatter import formatter
from app.classifier import classifier
from mongodb.read_collection import read_habitat_curated
from app.relation_maker import calculate_relations
from app.matrix_maker import matrix_maker
from app.app import obtain_min_max_mass
from app.metrics import analyze_network, save_metrics



# Used to create a predation matrix.
def create_matrix(N: int):
    matrix = [[0 for _ in range(N)] for _ in range(N)] 
    return matrix

# Used to create random animals for testing purposes.
def create_random_list(N: int):
    animals = [round(rn.random(), 4)  for _ in range(N)]
    return animals
    
# Creates Gephi node CSV.
def create_csv(matrix: list, name: str):
    
    shape = len(matrix)
    
    id = []
    label = []
    size = []
    
    for i in range(shape):
        id.append(i+1)
        label.append(matrix[i][0])
        size.append(10)
    
    source = []
    target = []
    typer = []
    
    
    for i in range(shape):
        for j in range(shape):
            if matrix[i][1][j][2] == 1:
                source.append(i+1)
                target.append(j+1)
                typer.append(matrix[i][1][j][0])
    
    node_map = pd.DataFrame({
        "Id": id,
        "Label": label,
        "Size": size
    })
    
    arrow_map = pd.DataFrame({
        "Source": source,
        "Target": target,
        "Type": typer
    })
    
    arrow_map.to_csv("data/results/"+name+"_arrow_map.csv", index = False)
    node_map.to_csv("data/results/"+name+"_node_map.csv", index = False)
    
    print("CSV file created succesfully")
    
    
def load_habitat_method(selected_values: list, C: float):
    
    habitat_file = selected_values[0]
    cl = selected_values[1]
    
    if not selected_values[0] or not selected_values[1]:
        print("Habitat or configuration files not selected")
        return
    
    if not formatter(habitat_file,"collection1") or not classifier("collection1","collection2",cl):
        print("Application failed to load the habitat. Returning...")
        return
    
    habitat = read_habitat_curated('collection2')
    matrix_h = matrix_maker(cl)
    final_matrix = []
    min, max = obtain_min_max_mass('collection2')
    for l_being in habitat:
        print(l_being)
        relations = []
        habitataux = read_habitat_curated('collection2')
        calculate_relations(l_being, matrix_h, relations, habitataux, C, max, min)
        l_being_set = (l_being['name'], relations)
        final_matrix.append(l_being_set)
    print(final_matrix)
    
    # Name of the result files
    habitat_result_name = habitat_file.removesuffix(".csv")
    
    # Storing node map data
    create_csv(final_matrix,habitat_result_name)
    
    # Creating metrics file
    node_df = pd.read_csv("data/results/"+habitat_result_name+"_node_map.csv")
    arrow_df = pd.read_csv("data/results/"+habitat_result_name+"_arrow_map.csv")
    metrics = analyze_network(arrow_df, node_df)
    save_metrics(metrics, "data/metrics/"+habitat_result_name+"_metrics")
    
    print("Processing finished")
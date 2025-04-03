import pandas as pd
import random as rn

# Used to create a predation matrix.
def create_matrix(N: int):
    matrix = [[0 for _ in range(N)] for _ in range(N)] 
    return matrix

# Used to create random animals for testing purposes.
def create_random_list(N: int):
    animals = [round(rn.random(), 4)  for _ in range(N)]
    return animals
    
# Creates Gephi node CSV.
def create_csv(matrix: list):
    
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
    
    
    for i in range(shape):
        for j in range(shape):
            if matrix[i][1][j][2] == 1:
                source.append(i+1)
                target.append(j+1)
    
    node_map = pd.DataFrame({
        "Id": id,
        "Label": label,
        "Size": size
    })
    
    arrow_map = pd.DataFrame({
        "Source": source,
        "Target": target
    })
    
    arrow_map.to_csv("data/arrow_map.csv", index = False)
    node_map.to_csv("data/node_map.csv", index = False)
    
    print("CSV file created succesfully")
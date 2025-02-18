import numpy as np
import pymongo

# Method to obtain ni value with the living being's mass
def calculate_ni(min_mass: float, max_mass: float, mass: float):
    # Checking for wrong values
    if min_mass <= 0:
        min_mass = 1.0
    if max_mass <= 0:
        max_mass = 1.0
    if mass <= 0:
        mass = 1.0

    log_mass = np.log10(mass)
    log_max_mass = np.log10(max_mass)
    log_min_mass = np.log10(min_mass)

    ni = (log_mass - log_min_mass) / (log_max_mass - log_min_mass)

    return ni
    

# Method to obtain max mass and min mass from an habitat using mongo queries
def obtain_min_max_mass(name: str):

    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['ANMdb_curated']
    collection = db[name]

    # Obtaining max and min values of the collection:
    min_max = collection.aggregate([
        {"$group": {"_id": None, "min_weight": {"$min": "$weight"}, "max_weight": {"$max": "$weight"}}}
    ])

    # Iterating in the aggrgation to rescue the values.
    result = next(min_max, None)
    if result:
        return result["min_weight"], result["max_weight"]
    return None, None

# Method to calculate feeding range
def calculate_ri(C):
    ni = np.random.uniform(0,1)
    return 1-(1-ni)**(1/2*C)

# Method to calculate feeding optimum
def calculate_ci(ri, ni):
    return np.random.uniform(ri/2, ni)

# Method to find if an species predates another one
def generate_relation(ri, ci, ni2):

    low = ci - ri/2
    top = ci + ri/2
    if low < ni2 < top:
        return 1
    else:
        return 0

# Method to fill the Matrix with predatory relations.
def fill_matrix(list, matrix, C):

    positionx = 0
    positiony = 0

    for ni in list:
        ri = calculate_ri(C)
        ci = calculate_ci(ri, ni)
        print(f"{positionx+1}-> ni: {ni}, ri: {ri}, ci: {ci}")
        for ni2 in list:
            matrix[positionx][positiony] = generate_relation(ri, ci, ni2)
            positiony += 1
        positiony = 0
        positionx += 1
import numpy as np

# Method to calculate feeding range
def calculate_ri(C):
    return np.random.beta(1, 2*C)

# Method to calculate feeding optimum
def calculate_ci(ri, ni):
    return np.random.uniform(ri/2, ni)

#Method to find if an species predates another one
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
        print(f"ni: {ni}, ri: {ri}, ci: {ci}")
        for ni2 in list:
            matrix[positionx][positiony] = generate_relation(ri, ci, ni2)
            positiony += 1
        positiony = 0
        positionx += 1
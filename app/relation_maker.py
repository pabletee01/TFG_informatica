# 1 > 3 > 2 in the matrix

def calculate_relations(l_being: dict, matrix: dict, relations: list, habitat):
    classes = l_being['class']

    # dictionary where we store each type of 
    # predation for the corresponding class 
    # consumed by the living being
    prey = {}

    for cl in classes:
        prey.update(matrix[cl])

    print(prey)
    # recopiling all predatory interactions of the given living being.
    
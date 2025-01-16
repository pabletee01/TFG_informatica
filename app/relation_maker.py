# 1 > 3 > 2 in the matrix
# dict to set predatory relation without conditionals
priorities = {
    0: {1:1,2:2,3:3},
    1: {1:1,2:1,3:1},
    2: {1:1,2:2,3:3},
    3: {1:1,2:3,3:3},
}

def calculate_relations(l_being: dict, matrix: dict, relations: list, habitat):
    classes = l_being['class']

    # dictionary where we store each type of 
    # predation for the corresponding class 
    # consumed by the living being
    prey = {}

    for cl in classes:
        # If it already exists, the type of predation is managed with different priorities
        dict_matrix = matrix[cl]
        for cat in dict_matrix.keys():
            if cat in prey.keys():
                prey[cat] = priorities[prey[cat]][dict_matrix[cat]]
            else:
                prey[cat] = dict_matrix[cat]
    print(matrix)
    print(prey)
    print(classes)
    # recopiling all predatory interactions of the given living being.
    for lb in habitat:
        # Relation set to not predatory by default
        rel = 0
        for cat in lb['class']:
            # Calculating the value of predation type based on categories and priorities
            if cat in prey.keys():
                print(lb['name'] + ' predation type: ' + str(prey[cat]))
                rel = priorities[rel][prey[cat]]
        print(rel)
        relations.append(rel)
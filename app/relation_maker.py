# 1 > 3 > 2 in the matrix

def calculate_relations(l_being: dict, matrix: dict, relations: list, habitat):
    classes = l_being['class']

    # dictionary where we store each type of 
    # predation for the corresponding class 
    # consumed by the living being
    prey = {}

    for cl in classes:
        # If it already exists, the type of predation is managed with different priorities
        if cl in prey.keys():
            # Most prioritized
            if prey[cl] == 1:
                prey[cl] = 1
            # Mid priority
            elif prey[cl] == 3:
                if matrix[cl] == 1:
                    prey[cl] = 1
                else:
                    prey[cl] = 2
            # Least priority
            elif prey[cl] == 2:
                if matrix[cl] == 1:
                    prey[cl] = 1
                if matrix[cl] == 3:
                    prey[cl] = 3
                else:
                    prey[cl] = 2
        else:
            prey.update(matrix[cl])

    print(prey)
    # recopiling all predatory interactions of the given living being.
    
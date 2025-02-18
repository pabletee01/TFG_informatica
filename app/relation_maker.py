from app.app import calculate_ci, calculate_ri, generate_relation
import random as ran
# 1 > 3 > 2 in the matrix

# dict to set predatory relation without conditionals
priorities = {
    0: {1:1,2:2,3:3}, 
    1: {1:1,2:1,3:1},
    2: {1:1,2:2,3:3},
    3: {1:1,2:3,3:3},
}

# Method used to calculate the predatory relations between one live being and all other species in the habitat
def calculate_relations(l_being: dict, matrix: dict, relations: list, habitat, connectivity_factor: float, max_mass, min_mass):
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
                if prey[cat][0] != priorities[prey[cat][0]][dict_matrix[cat]]:
                    prey[cat][1] = cl
                    print('Hola')
                prey[cat][0] = priorities[prey[cat][0]][dict_matrix[cat]]
            else:
                prey[cat] = [dict_matrix[cat], cl]

    # Calculation of the number of categories that consume other living beings associated to the living being to obtain the probability that is going to be needed
    # to determine if a predatory relation is established or not.
    
    

    print(matrix)
    print(prey)
    print(classes)

    habitat_l = []
    # recopiling all predatory interactions of the given living being.
    for lb in habitat:
        # Relation set to not predatory by default
        habitat_l.append(dict(lb))
        rel = [0,'']
        for cat in lb['class']:
            # Calculating the value of predation type based on categories and priorities
            if cat in prey.keys():
                print(lb['name'] + ' predation type: ' + str(prey[cat][0]))
                if rel[0] != priorities[rel[0]][prey[cat][0]]:
                    rel[1] = prey[cat][1]
                rel[0] = priorities[rel[0]][prey[cat][0]]
        
        print(rel)
        # 1 in rel means predation is determined by the connectivity factor:
        relations.append(rel)

    # Calculating the frecuency of each category appearing in all the living being relations.
    frequencies = {}
    for r in relations:
        if r[1] in frequencies.keys():
            frequencies[r[1]] += 1
        else:
            frequencies[r[1]] = 1
    if '' in frequencies.keys():
        frequencies[''] = 0

    total_frequencies = 0

    for fr_cat in frequencies.keys():
        total_frequencies += frequencies[fr_cat]

    if total_frequencies != 0:
        for fr_cat in frequencies.keys():
            frequencies[fr_cat] = frequencies[fr_cat] / total_frequencies

    print(frequencies, total_frequencies)

    # Calculating the final interactions between each living being
    counter = 0
    for r in relations:
        random_number = ran.random()
        frequency = frequencies[r[1]]
        
        if random_number < frequency:
            # Relation depends on conectivity factor
            if r[0] == 1:
                r.append(1)
            # relation depends on ANM's result
            if r[0] == 2:
                r.append(1)
            # relation depends on inverse ANM's result
            if r[0] == 3:
                r.append(1)
        else:
            r.append(0)

        counter += 1
    print(habitat_l)

    
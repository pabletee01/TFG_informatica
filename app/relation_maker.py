from app.app import calculate_ci, generate_relation, calculate_ni, calculate_ci_inverse, calculate_ri_inverse, generate_relation_inverse, calculate_ri
import random as ran
from app.logger import logger
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
                prey[cat][0] = priorities[prey[cat][0]][dict_matrix[cat]]
            else:
                prey[cat] = [dict_matrix[cat], cl]

    # Calculation of the number of categories that consume other living beings associated to the living being to obtain the probability that is going to be needed
    # to determine if a predatory relation is established or not.

    logger.debug(matrix)
    logger.debug(prey)
    logger.debug(classes)

    habitat_l = []
    
    
    
    # recopiling all predatory interactions of the given living being.
    for lb in habitat:
        habitat_flag = False
        
        # Checking if both living beings share habitat
        for niche in l_being['habitat']:
            if niche in lb['habitat']:
                habitat_flag = True
                logger.debug(str(l_being['name'])+"----->"+str(lb['name']))
                logger.debug(str(l_being['habitat'])+"------"+str(lb['habitat']))
        
        habitat_l.append(dict(lb))
        
        # Relation set to not predatory by default
        rel = [0,'']
        if habitat_flag:
            for cat in lb['class']:
                # Calculating the value of predation type based on categories and priorities
                if cat in prey.keys():
                    logger.debug(lb['name'] + ' predation type: ' + str(prey[cat][0]))
                    if rel[0] != priorities[rel[0]][prey[cat][0]]:
                        rel[1] = prey[cat][1]
                    rel[0] = priorities[rel[0]][prey[cat][0]]
        
        logger.debug(rel)
        # 1 in rel means predation is determined by the connectivity factor:
        relations.append(rel)

    # Calculating the frecuency of each category appearing in all the living being relations.
    frequencies = {}
    for r in relations:
        if r[0] in frequencies.keys():
            frequencies[r[0]] += 1
        else:
            frequencies[r[0]] = 1
    if 0 in frequencies.keys():
        frequencies[0] = 0

    total_frequencies = 0

    for fr_cat in frequencies.keys():
        total_frequencies += frequencies[fr_cat]

    if total_frequencies != 0:
        for fr_cat in frequencies.keys():
            frequencies[fr_cat] = frequencies[fr_cat] / total_frequencies

    logger.debug(f"{frequencies}, {total_frequencies}")

    # Calculating the final interactions between each living being
    counter = 0
    # Obtaining ni value for the main living being
    ni1 = calculate_ni(min_mass ,max_mass ,l_being['weight'])
    ri_value = calculate_ri(connectivity_factor, ni1)
    ci = calculate_ci(ri_value, ni1)
    ri_inverse = calculate_ri_inverse(connectivity_factor, ni1)
    ci_inverse = calculate_ci_inverse(ri_inverse, ni1)
    logger.debug("ni value: "+str(ni1))
    logger.debug("ri value: "+str(ri_value))
    logger.debug("ci value: "+str(ci))
    logger.debug("ri inverse value: "+str(ri_inverse))
    logger.debug("ci inverse value: "+str(ci_inverse))
    logger.debug(l_being)
    for r in relations:
        random_number = ran.random()
        frequency = frequencies[r[0]]
        
        if random_number < frequency:
            # Relation depends on conectivity factor
            if r[0] == 1:
                random_number_case_1 = ran.random()
                if random_number_case_1 < connectivity_factor:
                    r.append(1)
                else:
                    r.append(0)   
            # relation depends on ANM's result
            if r[0] == 2:
                ni2 = calculate_ni(min_mass ,max_mass ,habitat_l[counter]['weight'])
                r.append(generate_relation(ri_value,ci,ni2))
            # relation depends on inverse ANM's result
            if r[0] == 3:
                ni2 = calculate_ni(min_mass ,max_mass ,habitat_l[counter]['weight'])
                r.append(generate_relation_inverse(ri_inverse, ci_inverse, ni2))
        else:
            r.append(0)

        counter += 1

    
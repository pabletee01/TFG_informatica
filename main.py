import argparse
from app.utils import create_matrix, create_random_list, create_csv
from app.app import fill_matrix
from app.formatter import formatter
from app.classifier import classifier
from app.matrix_maker import matrix_maker
from mongodb.read_collection import read_habitat_curated
from app.relation_maker import calculate_relations
from app.app import obtain_min_max_mass
from app.app import calculate_ni
from app.app import calculate_ri
from app.app import calculate_ri_inverse
import pytest

C = 0.15

def main():

    parser = argparse.ArgumentParser(description="ANM Application")
    parser.add_argument(
        "-t", "--test", action="store_true", help="Run the tests instead of the application."
    )
    parser.add_argument(
        "-c", "--classifier", action="store_true", help="Start testing classifier."
    )
    parser.add_argument(
        "-m", "--matrix_maker", action="store_true", help="Start testing matrix maker."
    )
    parser.add_argument(
        "-r", "--relation_maker", action="store_true", help="Start testing relation maker."
    )
    parser.add_argument(
        "-n", "--ni_maker", action="store_true", help="Testing the calculation of the ni value."
    )
    parser.add_argument(
        "-g", "--generation_test", action="store_true", help="Testing how the distributions work."
    )

    args = parser.parse_args()

    # Test mode
    if args.test:
        print("Running tests")
        pytest.main(['-v'])
    elif args.classifier:
        formatter("Zona-2_Marismas_Nacionales-C1.csv","collection1")
        classifier("collection1","collection1","classifier.yaml")
    elif args.matrix_maker:
        formatter("Zona-2_Marismas_Nacionales-C1.csv","collection1")
        classifier("collection1","collection2","classifier.yaml")
        matrix_maker("classifier.yaml")
    elif args.ni_maker:
        formatter("Zona-0_Las_Hoyas-C1.csv","collection1")
        classifier("collection1","collection2","classifier.yaml")
        habitat = read_habitat_curated('collection2')
        min, max =obtain_min_max_mass('collection2')
        insect = habitat[90]
        insect2 = habitat[91]
        insect3 = habitat[92]
        insect4 = habitat[93]
        print(insect['name'],min, max, insect['weight'],calculate_ni(min, max, insect['weight']))
        print(insect2['name'],min, max, insect2['weight'],calculate_ni(min, max, insect2['weight']))
        print(insect3['name'],min, max, insect3['weight'],calculate_ni(min, max, insect3['weight']))
        print(insect4['name'],min, max, insect4['weight'],calculate_ni(min, max, insect4['weight']))
        print('test_high_weight',min,max,max, calculate_ni(min,max,max))
        print('test_low_weight',min,max, min, calculate_ni(min,max, min))
    elif args.relation_maker:
        formatter("Zona-0_Las_Hoyas-C1.csv","collection1")
        classifier("collection1","collection2","classifier.yaml")
        habitat = read_habitat_curated('collection2')
        matrix_h = matrix_maker("classifier.yaml")
        insect = habitat[154]
        print(insect)
        relations = []
        min, max = obtain_min_max_mass('collection2')
        print(insect['name'],min, max, insect['weight'],calculate_ni(min, max, insect['weight']))
        calculate_relations(insect, matrix_h, relations, habitat, C, max, min)
        print(relations)
    elif args.generation_test:
        i = 0.0
        for z in range(10000):
            i += calculate_ri(C,0.9)
        print(f"normal: {i/10000}")
        i = 0.0
        for z in range(10000):
            i += calculate_ri_inverse(C,0.9)
        print(f"inverse: {i/10000}")
    # Normal mode
    else:
        print("Starting ANM application...")
        habitat_file=input("Enter the habitat's file name: ")
        formatter(habitat_file,"collection1")
        classifier("collection1","collection2","classifier.yaml")
        habitat = read_habitat_curated('collection2')
        matrix_h = matrix_maker("classifier.yaml")
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
        create_csv(final_matrix)
        print("App finished")

if __name__ == "__main__":
    main()
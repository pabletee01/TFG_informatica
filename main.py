import argparse
from app.utils import create_matrix, create_random_list, create_csv
from app.app import fill_matrix
from app.formatter import formatter
from app.classifier import classifier
import pytest

C = 0.3

def main():

    parser = argparse.ArgumentParser(description="ANM Application")
    parser.add_argument(
        "-t", "--test", action="store_true", help="Run the tests instead of the application"
    )
    parser.add_argument(
        "-c", "--classifier", action="store_true", help="Start testing classifier"
    )

    args = parser.parse_args()

    # Test mode
    if args.test:
        print("Running tests")
        pytest.main(['-v'])
    elif args.classifier:
        formatter("Zona-2_Marismas_Nacionales-C1.csv","collection1")
        classifier("collection1","")
    # Normal mode
    else:

        print("Starting ANM application...")
        N = int(input("Introduce the number of animals to generate: "))
        animals = create_random_list(N)
        print(animals)
        matrix = create_matrix(N)

        fill_matrix(animals, matrix, C)
        for fila in matrix:
            print(fila)
            
        create_csv(matrix)
        
        print("App finished")

if __name__ == "__main__":
    main()
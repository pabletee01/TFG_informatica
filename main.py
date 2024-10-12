from app.utils import create_matrix, create_random_list
from app.app import fill_matrix

def main():
    print("Starting ANM application...")
    N = int(input("Introduce the number of animals to generate: "))
    animals = create_random_list(N)
    print(animals)
    matrix = create_matrix(N)
    for fila in matrix:
        print(fila)

    fill_matrix(animals, matrix, 0.15)
    for fila in matrix:
        print(fila)
    print("App finished")

if __name__ == "__main__":
    main()
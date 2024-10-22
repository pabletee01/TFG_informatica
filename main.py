from app.utils import create_matrix, create_random_list, create_csv
from app.app import fill_matrix
from app.formatter import formatter

C = 10

def main():
    file = "Zona-0_Las_Hoyas-C1.csv"
    c_name = "Zona-0_Las_Hoyas-C1"
    formatter(file, c_name)


    """print("Starting ANM application...")
    N = int(input("Introduce the number of animals to generate: "))
    animals = create_random_list(N)
    print(animals)
    matrix = create_matrix(N)

    fill_matrix(animals, matrix, C)
    for fila in matrix:
        print(fila)
        
    create_csv(matrix)
    
    print("App finished")"""

if __name__ == "__main__":
    main()
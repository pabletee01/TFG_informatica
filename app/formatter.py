from mongodb.create_collection import insert_habitat
import pandas as pd
import os

# Method used to read a csv file and store it in the mongodb database
def formatter(file: str, c_name: str):
    # Obtaining the path of the CSV file
    file = os.getcwd() + "/data/habitats/" + file

    df = pd.read_csv(file, header=None)

    animal_list = []

    # Iterating the dataframe to store data in a dic
    for _ , row in df.iterrows():
        animal = {
            'name': row[0],        # elem0
            'kingdom': row[1],     # elem1
            'weight': row[6],      # elem6
            'size': row[7],        # elem7
            'diet': row[8]         # elem8
        }
        animal_list.append(animal)

    print(animal_list)

    insert_habitat(animal_list, c_name)

    return

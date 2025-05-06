from mongodb.create_collection import insert_habitat
import pandas as pd
import os
import sys
from app.logger import logger

N_CSV_COLUMNS = 10

# Method used to read a csv file and store it in the mongodb database
def formatter(file: str, c_name: str):
    # Obtaining the path of the CSV file
    filea = os.getcwd() + "/data/habitats/" + file

    try:
        df = pd.read_csv(filea, header=None, on_bad_lines='error')
    except FileNotFoundError:
        logger.error(f"{file} not found in data/habitats directory", file=sys.stderr)
        return False
    except Exception as e:
        logger.error(f"Unexpected error while reading {file}: {e}", file=sys.stderr)
        return False

    animal_list = []

    # Iterating the dataframe to store data in a dic
    try:
        for _ , row in df.iterrows():
            for item in row:
                if pd.isna(item):
                    raise Exception(f"Wrong format in CSV {file}")
            animal = {
                'name': row[0],        # elem0 scientific name
                'kingdom': row[1],     # elem1 kingdom of the organism
                'order': row[2],       # elem2 order of the animal
                'type': row[3],        # elem3 organism type.
                'weight': float(row[6]),      # elem6 Absolute mass of the organism 
                'size': float(row[7]),        # elem7 Absolute size of the organism
                'diet': row[8]         # elem8 Diet
            }
            animal_list.append(animal)
    except Exception as e:
        logger.error(f"Unexpected error while reading {file}: {e}", file=sys.stderr)
        return False

    # Inserting the newly formed habitat in the database
    insert_habitat(animal_list, c_name)

    return True

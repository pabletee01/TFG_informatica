import pytest
import pymongo
from app.classifier import classifier
from app.formatter import formatter
from app.matrix_maker import matrix_maker


# Insert one habitat
def test_matrix_maker_ok():
    
    matrix = matrix_maker("classifier.yaml")

    # 159 lines in Zona-0_Las_Hoyas-C1.csv 
    assert isinstance(matrix, dict)

# Wrong format in configuration file
def test_matrix_maker_empty_config_file():
    
    matrix = matrix_maker("classifier_empty.yaml")

    # 0 lines in Zona-0_Las_Hoyas-C1.csv 
    assert matrix == False

# Empty engine configuration file.
def test_matrix_maker_wrong_format_of_config_file():
    
    matrix = matrix_maker("classifier_wrong_format.yaml")

    # 0 lines in Zona-0_Las_Hoyas-C1.csv 
    assert matrix == False
    
def test_matrix_maker_wrong_name_config_file():
    
    matrix = matrix_maker("classifier_wrong_name.yaml")

    # 0 lines in Zona-0_Las_Hoyas-C1.csv 
    assert matrix == False
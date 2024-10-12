import numpy as np
import random as rn

def create_matrix(N: int):
    matrix = [[0 for _ in range(N)] for _ in range(N)] 
    return matrix

def create_random_list(N: int):
    animals = [round(rn.random(), 4)  for _ in range(N)]
    return animals
    
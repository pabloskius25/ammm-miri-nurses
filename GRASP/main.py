import sys
import json
from random import random
import constructive as constructive
import localsearch as localsearch
import numpy as np


def grasp(config, data):
    max_itr = config['max_grasp_iterations']
    best_solution_value = sys.maxint
    for i in range(0, max_itr):
        alpha = random()
        sol, feasible = constructive.construct(data, alpha)
        if not feasible:
            continue
        sol = localsearch.local(data, sol)
        new_solution_value = get_cost_from_solution(sol)
        if new_solution_value < best_solution_value:
            best_solution_value = new_solution_value
            best_solution = sol
    return np.array(best_solution)


def get_cost_from_solution(sol):
    total_nurses = 0
    for i in sol:
        if np.sum(i) > 0:
            ++total_nurses
    return total_nurses


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit('Usage: python main.py <configurationFile> <dataFile>')
    else:
        with open(sys.argv[1]) as config_file:
            with open(sys.argv[2]) as data_file:
                print grasp(json.load(config_file), json.load(data_file))

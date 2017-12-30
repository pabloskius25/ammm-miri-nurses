import sys
import json
from random import random
import constructive as constructive
import localsearch as localsearch
import numpy as np
import time


def grasp(config, data):
    max_itr = config['max_grasp_iterations']
    best_solution_value = sys.maxint

    print("Starting candidates creation...")
    possible_schedules = constructive.create_candidate_schedules(data)
    print("Candidates creation finished...")

    for i in range(0, max_itr):
        print("Starting iteration " + str(i) + "...")
        alpha = random()
        if i == max_itr - 1:
            alpha = 1
        sol, feasible = constructive.construct(data, possible_schedules, alpha)
        if not feasible:
            continue
        sol = localsearch.local(data, sol)
        new_solution_value = get_cost_from_solution(sol)
        if new_solution_value < best_solution_value:
            if best_solution_value != sys.maxint:
                print("Improvement of the solution by " +
                      str(best_solution_value - new_solution_value))
            best_solution_value = new_solution_value
            best_solution = sol
    result = {
                "solution": best_solution,
                "value": best_solution_value
             }
    return result


def get_cost_from_solution(sol):
    total_nurses = 0
    for i in sol:
        if np.sum(i) > 0:
            total_nurses += 1
    return total_nurses


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit('Usage: python main.py <configurationFile> <dataFile>')
    else:
        with open(sys.argv[1]) as config_file:
            with open(sys.argv[2]) as data_file:
                start_time = time.time()
                solution = grasp(json.load(config_file), json.load(data_file))
                solution["executionTime"] = time.time() - start_time
                with open('solution.json', 'w') as fp:
                    json.dump(solution, fp, sort_keys=True, indent=4)

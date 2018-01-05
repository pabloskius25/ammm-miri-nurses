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
    best_solution = None
    total_time_constructive = 0
    total_time_localsearch = 0

    possible_schedules = constructive.create_candidate_schedules(data)

    for i in range(max_itr):
        alpha = random()
        if i == max_itr - 1:
            alpha = 1

        start_time = time.time()
        sol, feasible = constructive.construct(data, possible_schedules, alpha,
                                               i)
        total_time_constructive += time.time() - start_time
        if not feasible:
            continue

        start_time = time.time()
        sol = localsearch.local_search(data, sol, i)
        total_time_localsearch += time.time() - start_time
        new_solution_value = get_cost_from_solution(sol)

        if new_solution_value < best_solution_value:
            best_solution_value = new_solution_value
            best_solution = sol

    if best_solution is None:
        return None

    start_time = time.time()
    best_solution = localsearch.deep_local_search(data, best_solution)
    time_deeplocalsearch = time.time() - start_time
    cost = get_cost_from_solution(best_solution)

    result = {
                "fitness": get_fitness_from_solution(data, best_solution,
                                                     cost),
                "nursesNeeded": cost,
                "constructiveTime": total_time_constructive,
                "localSearchTime": total_time_localsearch,
                "deepLocalSearchTime": time_deeplocalsearch,
                "nNurses": data['nNurses'],
                "nHours": data['nHours']
             }

    return result


def get_cost_from_solution(sol):
    total_nurses = 0
    for i in sol:
        if np.sum(i) > 0:
            total_nurses += 1
    return total_nurses


def get_fitness_from_solution(data, sol, value):
    demand = data["demand"]
    return 1000 * value + (sum([sum(i) for i in sol]) - sum(demand))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit('Usage: python main.py <configurationFile>')
    else:
        with open(sys.argv[1]) as config_file:
            global_config = json.load(config_file)
            for instance in global_config:
                with open(instance['dataFile']) as data_file:
                    print('\n File ' + str(instance['dataFile']) + '\n')
                    start_time = time.time()
                    solution = grasp(instance['config'], json.load(data_file))

                    if solution is None:
                        solution = {
                            "error": "No solution found"
                        }

                    solution["executionTime"] = time.time() - start_time
                    with open(instance['outputFile'], 'w') as solution_file:
                        json.dump(solution, solution_file, sort_keys=True,
                                  indent=4)

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
    total_time_localsearch = 0;

    print("Starting candidates creation...")
    possible_schedules = constructive.create_candidate_schedules(data)
    print("Candidates creation finished...")

    for i in range(0, max_itr):
        print("Starting iteration " + str(i) + "...")

        alpha = random()
        if i == max_itr - 1:
            alpha = 1
        print("Alpha: " + str(alpha))

        start_time = time.time()
        sol, feasible = constructive.construct(data, possible_schedules, alpha)
        total_time_constructive += time.time() - start_time
        if not feasible:
            continue

        start_time = time.time()
        sol, improved = localsearch.local(data, sol)
        total_time_localsearch += time.time() - start_time
        new_solution_value = get_cost_from_solution(sol)

        if improved:
            print("Solution improved by local search")

        if new_solution_value < best_solution_value:
            best_solution_value = new_solution_value
            best_solution = sol

    if best_solution is None:
        return None

    start_time = time.time()
    best_solution = localsearch.deep_local(data, best_solution)
    time_deeplocalsearch = time.time() - start_time
    cost = get_cost_from_solution(best_solution)

    result = {
                "solution": best_solution,
                "fitness": get_fitness_from_solution(data, best_solution,
                                                     cost),
                "value": cost,
                "constructiveTime": total_time_constructive,
                "localSearchTime": total_time_localsearch,
                "deepLocalSearchTime": time_deeplocalsearch
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
    if len(sys.argv) != 4:
        sys.exit('Usage: python main.py <configurationFile> <dataFile> ' +
                 '<solutionFile>')
    else:
        with open(sys.argv[1]) as config_file:
            with open(sys.argv[2]) as data_file:
                start_time = time.time()
                solution = grasp(json.load(config_file), json.load(data_file))

                if solution is None:
                    sys.exit('Solution not found')

                solution["executionTime"] = time.time() - start_time
                with open(sys.argv[3], 'w') as solution_file:
                    json.dump(solution, solution_file, sort_keys=True,
                              indent=4)

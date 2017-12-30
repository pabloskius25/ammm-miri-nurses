import numpy as np
from operator import itemgetter
import random
import constraints
import math


def construct(data, alpha):
    sol = []
    demand = data["demand"]
    n_nurses = data["nNurses"]
    n = 0
    possible_schedules = create_candidate_schedules(data)
    while n < n_nurses:
        compute_greedy_cost(possible_schedules, sol, demand)
        possible_schedules = sorted(possible_schedules, key=itemgetter('gc'),
                                    reverse=True)
        max_gc = possible_schedules[0]['gc']
        min_gc = possible_schedules[len(possible_schedules)-1]['gc']
        rcl = []
        for candidate in possible_schedules:
            if candidate['gc'] >= min_gc + alpha * (max_gc - min_gc):
                rcl.append(candidate)
        chosen = random.choice(rcl)['schedule']
        sol.append(chosen)
        if is_solution_feasible(sol, demand):
            return sol, True
        ++n
    return sol, False


def create_candidate_schedules(data):
    num_hours = data["nHours"]
    candidate_schedules = []

    for i in range(1, int(math.pow(2, num_hours) - 1)):
        candidate = get_schedule_combination(i, num_hours)

        if constraints.check_constraints(candidate, data):
            candidate_dict = {'schedule': candidate, 'gc': 0}
            candidate_schedules.append(candidate_dict)

    return candidate_schedules


def get_schedule_combination(n, hours):
    aux = [int(digit) for digit in bin(n)[2:]]
    return ([0]*(hours-len(aux))) + aux


def compute_greedy_cost(candidates, sol, demand):
    sol_array = np.array(sol)
    for candidate in candidates:
        greedy_cost = 0
        schedule = candidate['schedule']
        for i in range(0, len(schedule)):
            if schedule[i] == 1 and (len(sol_array) == 0 or
                                     np.sum(sol_array[:, i]) < demand[i]):
                greedy_cost += 1
        candidate['gc'] = greedy_cost


def is_solution_feasible(sol, demand):
    sol_array = np.array(sol)
    for i in range(0, len(demand)):
        if demand[i] > np.sum(sol_array[:, i]):
            return False
    return True

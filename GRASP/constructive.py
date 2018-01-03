import numpy as np
import random
import constraints
import math
import sys
from progress.bar import ShadyBar
import main


def construct(data, possible_schedules, alpha, iteration):
    sol = []
    demand = data["demand"]
    n_nurses = data["nNurses"]

    bar = FancyBar('Constructive of iteration ' + str(iteration),
                   max=n_nurses,
                   suffix='%(percent)d%% --> %(fitness_message)s')

    for n in range(n_nurses):
        compute_greedy_cost(possible_schedules, sol, demand)

        min_gc = sys.maxint
        max_gc = 0

        for schedule in possible_schedules:
            if schedule['gc'] > max_gc:
                max_gc = schedule['gc']
            if schedule['gc'] < min_gc:
                min_gc = schedule['gc']

        rcl = []
        for candidate in possible_schedules:
            if candidate['gc'] >= min_gc + alpha * (max_gc - min_gc):
                rcl.append(candidate)
        chosen = random.choice(rcl)['schedule']
        sol.append(chosen)
        if is_solution_feasible(sol, demand):
            bar.dynamic_message = "Solution: " + str(main.get_cost_from_solution(sol)) + " nurses"
            bar.index = bar.max
            bar.update()
            bar.finish()
            return sol, True
        bar.next()

    bar.dynamic_message = "No Solution"
    bar.next()
    bar.finish()

    return sol, False


def create_candidate_schedules(data):
    num_hours = data["nHours"]
    candidate_schedules = []
    max_number = int(math.pow(2, num_hours) - 1)

    bar = ShadyBar('        Creating candidates', max=max_number - 1,
                   suffix='%(percent).2f%%')

    for i in range(1, max_number):
        candidate = get_schedule_combination(i, num_hours)

        if constraints.check_constraints(candidate, data):
            candidate_dict = {'schedule': candidate, 'gc': 0}
            candidate_schedules.append(candidate_dict)

        bar.next()

    bar.finish()
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


class FancyBar(ShadyBar):
    dynamic_message = ''

    @property
    def fitness_message(self):
        return self.dynamic_message

    def complete_progress(self):
        self.index = self.max

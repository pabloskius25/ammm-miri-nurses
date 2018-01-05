import numpy as np
import copy
import constraints
from progress.bar import ShadyBar
import main


def local_search(data, original_solution, iteration):
    return local(data, original_solution, iteration, 1, 1)[0]


def deep_local_search(data, original_solution):
    return local(data, original_solution, -1, 3, 3)[0]


def local(data, original_solution, iteration, original_depth, depth):
    if depth == 0:
        return original_solution, 0

    demand = data["demand"]
    best_sol = None
    best_improvement = 0
    best_fitness = 0

    if original_depth == depth:
        message = ('          Deep Local Search' if iteration == -1
                   else '   Local Search iteration ' + str(iteration))
        bar = FancyBar(message, max=len(original_solution),
                       suffix='%(percent)d%% --> %(fitness_message)s')

    # Try to reassign the schedule of each nurse
    for nurse in range(len(original_solution)):
        new_solution = copy.deepcopy(original_solution)
        schedule_to_reassign = original_solution[nurse]
        del new_solution[nurse]

        if reassign_schedule_to_someone_else(data, new_solution,
                                             schedule_to_reassign, demand):
            sol, improvement = local(data, new_solution, iteration,
                                     original_depth, depth - 1)
            improvement += 1  # We add the improvement we got in the if clause
            cost = main.get_cost_from_solution(sol)
            fitness = main.get_fitness_from_solution(data, sol, cost)
            if (improvement > best_improvement or
               (improvement == best_improvement and fitness > best_fitness)):
                best_sol = sol
                best_improvement = improvement
                best_fitness = fitness
                if original_depth == depth:
                    bar.dynamic_message = "Solution: " + str(cost) + " nurses"
        if original_depth == depth:
            bar.next()

    if best_sol is not None:
        if original_depth == depth:
            bar.finish()
        return best_sol, best_improvement
    elif original_depth == depth:
        bar.dynamic_message = "Solution not improved"
        bar.next()
        bar.finish()

    return original_solution, 0


def reassign_schedule_to_someone_else(data, new_solution, schedule_to_reassign,
                                      demand):
    for hour in range(0, len(schedule_to_reassign)):
        # Check if the nurse was actually working at that hour
        if schedule_to_reassign[hour] == 0:
            continue
        # Check if that hour is demanded to be worked
        new_solution_array = np.array(new_solution)
        if np.sum(new_solution_array[:, hour]) >= demand[hour]:
            continue

        if not try_to_reassign_hour(data, hour, new_solution):
            return False

    return True


def try_to_reassign_hour(data, hour, new_solution):
    for nurse in range(0, len(new_solution)):
        # Check if the candidate nurse is already working at that hour
        if new_solution[nurse][hour] == 1:
            continue
        candidate_schedule = copy.deepcopy(new_solution[nurse])
        candidate_schedule[hour] = 1
        if constraints.check_constraints(candidate_schedule, data):
            new_solution[nurse] = candidate_schedule
            return True
    return False


def get_best_candidate(tuples, data):
    best_sol = None
    best_improvement = 0
    best_fitness = 0
    for (sol, improvement) in tuples:
        cost = main.get_cost_from_solution(sol)
        fitness = main.get_fitness_from_solution(data, sol, cost)
        if improvement > best_improvement or (improvement == best_improvement
           and fitness > best_fitness):
            best_sol = sol
            best_improvement = improvement
            best_fitness = fitness
    return best_sol, best_improvement


class FancyBar(ShadyBar):
    dynamic_message = ''

    @property
    def fitness_message(self):
        return self.dynamic_message

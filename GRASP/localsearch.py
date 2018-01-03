import numpy as np
import copy
import constraints
from progress.bar import ShadyBar
import main


def deep_local(data, original_solution):
    sol = original_solution
    improved = True
    while improved:
        sol, improved = local(data, sol, -1)

    return sol


def local(data, original_solution, iteration):
    demand = data["demand"]

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
            bar.dynamic_message = "Solution: " + str(main.get_cost_from_solution(new_solution)) + " nurses"
            bar.index = bar.max
            bar.update()
            bar.finish()
            return new_solution, True
        bar.next()

    bar.dynamic_message = "Solution not improved"
    bar.next()
    bar.finish()

    return original_solution, False


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


class FancyBar(ShadyBar):
    dynamic_message = ''

    @property
    def fitness_message(self):
        return self.dynamic_message

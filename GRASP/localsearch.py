import numpy as np
import copy
import constraints


def deep_local(data, original_solution):
    print("Starting deep local search")
    sol = original_solution
    improved = True
    while improved:
        sol, improved = local(data, sol)

    return sol


def local(data, original_solution):
    print("Starting local search...")
    demand = data["demand"]

    # Try to reassign the schedule of each nurse
    for nurse in range(0, len(original_solution)):
        new_solution = copy.deepcopy(original_solution)
        schedule_to_reassign = original_solution[nurse]
        del new_solution[nurse]

        if reassign_schedule_to_someone_else(data, new_solution,
                                             schedule_to_reassign, demand):
            return new_solution, True

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

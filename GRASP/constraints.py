import numpy as np


def check_constraints(candidate, data):
    num_hours = data["nHours"]
    min_hours = data["minHours"]
    max_hours = data["maxHours"]
    max_consec = data["maxConsec"]
    max_presence = data["maxPresence"]

    total_hours = np.sum(candidate)
    first_working_hour = candidate.index(1)
    last_working_hour = len(candidate) - 1 - candidate[::-1].index(1)

    # Check minHours
    if total_hours < min_hours:
        return False

    # Check maxHours
    if total_hours > max_hours:
        return False

    # Check maxPresence
    if last_working_hour - first_working_hour > max_presence:
        return False

    # Check maxConsec
    if not check_max_consec_constraint(num_hours, max_consec, candidate):
        return False

    # Check 2 Consecutive Rests
    if not check_two_consecutive_rests_constraint(num_hours,
                                                  first_working_hour,
                                                  last_working_hour,
                                                  candidate):
        return False

    return True


def check_max_consec_constraint(num_hours, max_consec, candidate):
    for i in range(0, num_hours - max_consec):
        if np.sum(candidate[i:i + (max_consec + 1)]) > max_consec:
            return False
    return True


def check_two_consecutive_rests_constraint(num_hours, first_working_hour,
                                           last_working_hour, candidate):
    for i in range(0, num_hours - 1):
        if i < first_working_hour or i > last_working_hour:
            continue
        if np.sum(candidate[i:i + 2]) == 0:
            return False
    return True

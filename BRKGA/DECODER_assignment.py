import sys
import constraints
from progress.bar import ShadyBar


def getChromosomeLength(problem):
    return int(problem["nNurses"] * problem["nHours"])


def decode(population, data, generation):
    bar = FancyBar(generation, max=len(population),
                   suffix='%(percent)d%% --> %(fitness_message)s')

    best_fitness = sys.maxint

    for i in range(len(population)):
        bar.next()
        ind = population[i]
        solution, fitness = decoder_assignment(data, ind['chr'])
        ind['solution'] = solution
        ind['fitness'] = fitness
        if fitness < best_fitness:
            best_fitness = fitness
            bar.dynamic_message = "Best fitness: " + str(fitness)

    bar.finish()
    return(population)


def decoder_assignment(problem, chromosome):
    nurses = problem["nNurses"]
    hours = problem["nHours"]
    minHours = problem["minHours"]
    maxHours = problem["maxHours"]
    maxConsec = problem["maxConsec"]
    maxPresence = problem["maxPresence"]
    numNurses = nurses
    nursesRanges = range(0, problem["nNurses"])
    hoursRange = range(0, problem["nHours"])

    solution = [0]*(nurses * hours)
    d = problem["demand"]
    demand = d[:]
    demandedHours = sum(demand)
    workingNurses = 0

    for n in nursesRanges:
        workedHours = 0
        consecWorking = 0
        presence = 0
        startedTurn = False
        isWorking = False
        restedPrev = True
        for h in hoursRange:
            if presence >= maxPresence or workedHours >= maxHours:
                break

            if demand[h] > numNurses:
                return None, sys.maxint
            elif not startedTurn:
                sp = 0.5 * chromosome[(n*hours) + h]
                dm = demand[h] / (1. * numNurses)
                sp += 0.5 * (dm)
                if sp > 0.5:
                    workingNurses += 1
                    startedTurn = True
                    isWorking = True
                    consecWorking += 1
                    workedHours += 1
                    presence += 1
                    demand[h] = (demand[h] - 1 if demand[h] > 0 else 0)
                    solution[(n*hours) + h] = 1
            elif isWorking:
                sp = 0.3 * chromosome[(n*hours) + h]
                dm = sum(demand[h: hours-1]) / (1. * numNurses * (hours-h))
                sp += 0.2 * (dm)
                solution[(n*hours) + h] = 1
                correct = constraints.check_constraints(solution[(n*hours):
                                                        (n*hours) + hours-1],
                                                        problem)
                sp += (0.5 if not correct else 0)
                solution[(n*hours) + h] = 0
                sp = (sp - 0.5 if workedHours < minHours else sp)

                if sp > 0.8:
                    if workedHours < minHours:
                        if (consecWorking + 1) >= maxConsec:
                            restedPrev = True
                            consecWorking = 0
                            presence += 1
                            continue
                        restedPrev = False
                        demand[h] = (demand[h] - 1 if demand[h] > 0 else 0)
                        solution[(n*hours) + h] = 1
                        consecWorking += 1
                        workedHours += 1
                        presence += 1
                    else:
                        isWorking = False
                        break

                elif sp > 0.6 and not restedPrev:
                    restedPrev = True
                    consecWorking = 0
                    presence += 1
                else:
                    if (presence + 1) >= maxPresence:
                        break
                    if (consecWorking + 1) >= maxConsec:
                        restedPrev = True
                        consecWorking = 0
                        presence += 1
                        continue

                    restedPrev = False
                    demand[h] = (demand[h] - 1 if demand[h] > 0 else 0)
                    solution[(n*hours) + h] = 1
                    consecWorking += 1
                    workedHours += 1
                    presence += 1
        numNurses -= 1
        correct = True
        if(sum(solution[(n*hours): (n*hours) + hours-1]) > 0):
            correct = constraints.check_constraints(solution[(n*hours):
                                                    (n*hours) + hours-1],
                                                    problem)
        if not correct:
            return None, sys.maxint

    if sum(demand) > 0:
        # bar.dynamic_message = "Incomplete result with: " + str(sum(demand))
        return None, sys.maxint
    fitness = (1000) * workingNurses + (sum(solution) - demandedHours)
    return solution, fitness


class FancyBar(ShadyBar):
    dynamic_message = ''

    @property
    def fitness_message(self):
        return self.dynamic_message

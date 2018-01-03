import sys
import json
import math
import time
import matplotlib.pyplot as plt

import BRKGA as brkga  # BRKGA framework (problem independent)
import DECODER_assignment as decoder  # Decoder algorithm (problem-dependent)


def printSolutiuon(solution, nurses, hours):
    nursesRanges = range(0, nurses)
    hoursRange = range(0, hours)
    print("\n")
    for n in nursesRanges:
        sn = "Schedule of nurse " + str(n) + ":"
        for h in hoursRange:
            sn += " " + str(solution[(n*hours) + h])
        print(sn)
    print("\n")


def solve_brkga(problem, config):
    # initializations
    numIndividuals = int(config['numIndividuals'])
    numElite = int(math.ceil(numIndividuals*config['eliteProp']))
    numMutants = int(math.ceil(numIndividuals *
                               config['mutantProp']))
    numCrossover = max(numIndividuals-numElite-numMutants, 0)
    maxNumGen = int(config['maxNumGen'])
    ro = float(config['inheritanceProb'])
    evol = []

    # Main body
    chrLength = decoder.getChromosomeLength(problem)

    population = brkga.initializePopulation(numIndividuals,
                                            chrLength)
    for i in range(maxNumGen):
        population = decoder.decode(population, problem,
                                    'Generation ' + str(i))

        evol.append(brkga.getBestFitness(population)['fitness'])

        if numElite > 0:
            elite, nonelite = brkga.classifyIndividuals(population,
                                                        numElite)
        else:
            elite = []
            nonelite = population

        if numMutants > 0:
            mutants = brkga.generateMutantIndividuals(numMutants,
                                                      chrLength)
        else:
            mutants = []

        if numCrossover > 0:
            crossover = brkga.doCrossover(elite, nonelite, ro,
                                          numCrossover)
        else:
            crossover = []

        population = elite + crossover + mutants

    population = decoder.decode(population, problem, 'Last Generation')
    bestIndividual = brkga.getBestFitness(population)

    return bestIndividual, evol


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit('Usage: python main.py <configurationFile>')
    else:
        with open(sys.argv[1]) as config_file:
            global_config = json.load(config_file)
            for instance in global_config:
                with open(instance['dataFile']) as data_file:
                    problem = json.load(data_file)
                    config = instance['config']

                    start_time = time.time()
                    bestIndividual, evol = solve_brkga(problem, config)

                    chrLength = decoder.getChromosomeLength(problem)

                    plt.plot(evol)
                    plt.xlabel('number of generations')
                    plt.ylabel('Fitness of best individual')
                    plt.axis([0, len(evol), 0, (1000) * problem['nNurses'] +
                             (chrLength) + 5])
                    # plt.imsave(sys.argv[3] + ".png")

                    total_time = time.time() - start_time
                    numIndividuals = int(config['numIndividuals'])
                    maxNumGen = int(config['maxNumGen'])
                    solution = {
                        "nursesNeeded": bestIndividual['fitness']/1000,
                        "fitness": bestIndividual['fitness'],
                        "executionTime": total_time,
                        "numIndividuals": numIndividuals,
                        "maxNumGen": maxNumGen,
                        "nNurses": problem['nNurses'],
                        "nHours": problem['nHours']
                    }

                    with open(instance['outputFile'], 'w') as solution_file:
                        json.dump(solution, solution_file, sort_keys=True,
                                  indent=4)

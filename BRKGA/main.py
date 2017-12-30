import sys
import json
import math
import time
import matplotlib.pyplot as plt

import BRKGA as brkga # BRKGA framework (problem independent)
import DECODER_assignment as decoder # Decoder algorithm (problem-dependent)


def printSolutiuon(solution, nurses, hours):
    nursesRanges = range(0,nurses)
    hoursRange = range(0, hours)
    print("\n")
    for n in nursesRanges:
        sn = "Schedule of nurse " + str(n) + ":"        
        for h in hoursRange:
            sn += " " + str(solution[(n*hours) + h])
        print(sn)
    print("\n")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit('Usage: python main.py <configurationFile> <dataFile>')
    else:
        with open(sys.argv[1]) as config_file:
            with open(sys.argv[2]) as data_file:
                t = time.time()
                problem = json.load(data_file)
                config = json.load(config_file)
                # initializations
                numIndividuals=int(config['numIndividuals'])
                numElite=int(math.ceil(numIndividuals*config['eliteProp']))
                numMutants=int(math.ceil(numIndividuals*config['mutantProp']))
                numCrossover=max(numIndividuals-numElite-numMutants,0)
                maxNumGen=int(config['maxNumGen'])
                ro=float(config['inheritanceProb'])
                evol=[]

                # Main body
                chrLength=decoder.getChromosomeLength(problem)

                population=brkga.initializePopulation(numIndividuals,chrLength)

                i=0
                while (i<maxNumGen):
                    print i

                    population = decoder.decode(population,problem)

                    evol.append(brkga.getBestFitness(population)['fitness'])

                    if numElite>0:
                        elite, nonelite = brkga.classifyIndividuals(population,numElite)
                    else: 
                        elite = []
                        nonelite = population

                    if numMutants>0: mutants = brkga.generateMutantIndividuals(numMutants,chrLength)
                    else: mutants = []

                    if numCrossover>0: crossover = brkga.doCrossover(elite,nonelite,ro,numCrossover)
                    else: crossover=[]

                    population=elite + crossover + mutants
                    i+=1
                    
                population = decoder.decode(population, problem)
                bestIndividual = brkga.getBestFitness(population)
                plt.plot(evol)
                plt.xlabel('number of generations')
                plt.ylabel('Fitness of best individual')
                print(evol)
                plt.axis([0, len(evol), 0, (1000) * problem['nNurses'] +  (chrLength) +5])
                plt.show()
                print(time.time() - t)
                print bestIndividual
                printSolutiuon(bestIndividual['solution'], problem['nNurses'], problem['nHours'])
                
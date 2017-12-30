import os, random
import numpy as np

# Generate instances based on read configuration. 
class InstanceGenerator(object):
    def __init__(self, config):
        self.config = config
    
    def generate(self):
        instancesDirectory = self.config.instancesDirectory
        fileNamePrefix = self.config.fileNamePrefix
        fileNameExtension = self.config.fileNameExtension
        numInstances = self.config.numInstances
        
        numNurses = self.config.numNurses
        numHours = self.config.numHours
        
        if(not os.path.isdir(instancesDirectory)):
            raise Exception('Directory(%s) does not exist' % instancesDirectory)
        
        pin = []

        for h in xrange(0, numHours):
            if h < numHours/2:
                pin += [h] *  (80/ (numHours/2)) 
            else:
                pin += [h] * (20/ (numHours/2 + numHours%2))
            
        for i in xrange(0, numInstances):
            print "----------------------------- Instance " + str(i) + " -----------------------------"
            instancePath = os.path.join(instancesDirectory, '%s_%d.%s' % (fileNamePrefix, i, fileNameExtension))
            instancePathJson = os.path.join(instancesDirectory, '%s_%d.json' % (fileNamePrefix, i))
            fInstance = open(instancePath, 'w')
            fInstanceJson = open(instancePathJson, 'w')
            
            schedule = np.zeros((numNurses, numHours), dtype=np.int)
            nurseWorks = np.zeros(numNurses, dtype=np.int)
            demandH = np.zeros(numHours, dtype=np.int)
            maxPresence = 0
            maxWorkHours = 0
            minWorkHours = numHours
            maxConsec = 0
            
            for n in xrange(0, numNurses):
                nurseWorks[n] = random.randint(1, 1)
                if nurseWorks[n] == 1:
                    print "A la enfermera " + str(n) + " le ha tocado trabajar"
                    hin = random.choice(pin)
                    print "   Hora de entrada " + str(hin + 1)
                    
                    pout = []
                    rang = numHours -  hin
                    
                    for h in xrange(hin, numHours):
                        if h < numHours/2:
                            pout += [h] *  (20/ (rang/2)) 
                        else:
                            pout += [h] * (80/ (rang/2 + rang%2))
                    
                    hout = random.randint(hin, numHours - 1)
                    print "   Hora de salida " + str(hout + 1)
                    presence = (hout-hin+1)
                    maxDesc = presence/3
                    numDes = 0
                    puedeGastarDescanso = True
                    consec = 0
                    
                    for h in xrange(0, numHours):
                        if h < hin or h > hout:
                            schedule[n][h] = 0
                        elif h == hin:
                            schedule[n][h] = 1
                            puedeGastarDescanso = True
                            demandH[h] += 1
                            consec += 1
                        elif h == hout:
                            schedule[n][h] = 1
                            demandH[h] += 1
                            consec +=1
                        elif numDes < maxDesc and puedeGastarDescanso:
                            isDes =  random.randint(0, 1)
                            if isDes == 1:
                                schedule[n][h] = 0
                                puedeGastarDescanso = False
                                numDes += 1
                                if consec > maxConsec:
                                    maxConsec = consec
                                consec = 0
                            else:
                                schedule[n][h] = 1
                                puedeGastarDescanso = True
                                demandH[h] += 1
                                consec += 1
                        else:
                            schedule[n][h] = 1
                            puedeGastarDescanso = True
                            demandH[h] += 1
                            consec += 1
                    
                    print "   Num horas descanso " + str(numDes)
                    workHours = presence - numDes
                    
                    if presence > maxPresence:
                        maxPresence = presence
                    
                    if workHours > maxWorkHours:
                        maxWorkHours = workHours
                    
                    if workHours < minWorkHours:
                        minWorkHours = workHours
                        
                    if consec > maxConsec:
                        maxConsec = consec
                            
            
            print "Max presence constraint " + str(maxPresence)
            print "Max work hours constraint " + str(maxWorkHours)
            print "Min work hours constraint " + str(minWorkHours)
            print "Max consec work hours constraint " + str(maxConsec)
            
            print "Demand H"
            
            col = "     "
            for v in demandH:
                col += str(v) + " "
            
            print col
            
            print "Schedule"
            col = "Hour "
            for h in xrange(0 ,numHours):
                col += str(h+1) + " " 
            print col
            
            no = 0
            for nh in schedule:
                col = "Nur" + str(no) + " "
                for v in nh:
                    col += str(v) + " "
                print col
                no += 1
            
            fInstance.write('nHours=%d;\n' % numHours)
            fInstance.write('nNurses=%d;\n' % numNurses)
            fInstance.write('demand=[%s];\n' % (' '.join(map(str, demandH))))
            fInstance.write('minHours=%d;\n' % minWorkHours)
            fInstance.write('maxHours=%d;\n' % maxWorkHours)
            fInstance.write('maxConsec=%d;\n' % maxConsec)
            fInstance.write('maxPresence=%d;\n' % maxPresence)
            
            fInstanceJson.write('{\n')
            fInstanceJson.write('    "nHours": %d,\n' % numHours)
            fInstanceJson.write('    "nNurses": %d,\n' % numNurses)
            fInstanceJson.write('    "demand": [%s],\n' % (', '.join(map(str, demandH))))
            fInstanceJson.write('    "minHours": %d,\n' % minWorkHours)
            fInstanceJson.write('    "maxHours": %d,\n' % maxWorkHours)
            fInstanceJson.write('    "maxConsec": %d,\n' % maxConsec)
            fInstanceJson.write('    "maxPresence": %d\n' % maxPresence)
            fInstanceJson.write('}\n')
            
            # translate vector of floats into vector of strings and concatenate that strings separating them by a single space character
            fInstance.close()
            fInstanceJson.close()
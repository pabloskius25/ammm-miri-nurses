class ValidateConfig(object):
    @staticmethod
    def validate(data):
        # Validate that mandatory input parameters were found
        for paramName in ['instancesDirectory', 'fileNamePrefix', 'fileNameExtension', 'numInstances',
                          'numNurses', 'numHours']:
            if(not data.__dict__.has_key(paramName)):
                raise Exception('Parameter(%s) not contained in Configuration' % str(paramName))
        
        instancesDirectory = data.instancesDirectory
        if(len(instancesDirectory) == 0): raise Exception('Value for instancesDirectory is empty')

        fileNamePrefix = data.fileNamePrefix
        if(len(fileNamePrefix) == 0): raise Exception('Value for fileNamePrefix is empty')

        fileNameExtension = data.fileNameExtension
        if(len(fileNameExtension) == 0): raise Exception('Value for fileNameExtension is empty')

        numInstances = data.numInstances
        if(not isinstance(numInstances, (int, long)) or (numInstances <= 0)):
            raise Exception('numInstances(%s) has to be a positive integer value.' % str(numInstances))

        numNurses = data.numNurses
        if(not isinstance(numNurses, (int, long)) or (numNurses <= 0)):
            raise Exception('numNurses(%s) has to be a positive integer value.' % str(numNurses))
        
        numHours = data.numHours
        if(not isinstance(numHours, (int, long)) or (numHours <= 0)):
            raise Exception('numHours(%s) has to be a positive integer value.' % str(numHours))
        
    @staticmethod
    def ss(data):
        

        minNumCoresPerCPU = data.minNumCoresPerCPU
        if(not isinstance(minNumCoresPerCPU, (int, long)) or (minNumCoresPerCPU <= 0)):
            raise Exception('minNumCoresPerCPU(%s) has to be a positive integer value.' % str(minNumCoresPerCPU))

        maxNumCoresPerCPU = data.maxNumCoresPerCPU
        if(not isinstance(maxNumCoresPerCPU, (int, long)) or (maxNumCoresPerCPU <= 0)):
            raise Exception('maxNumCoresPerCPU(%s) has to be a positive integer value.' % str(maxNumCoresPerCPU))

        minCapacityPerCore = data.minCapacityPerCore
        if(not isinstance(minCapacityPerCore, (int, long, float)) or (minCapacityPerCore <= 0)):
            raise Exception('minCapacityPerCore(%s) has to be a positive float value.' % str(minCapacityPerCore))

        maxCapacityPerCore = data.maxCapacityPerCore
        if(not isinstance(maxCapacityPerCore, (int, long, float)) or (maxCapacityPerCore <= 0)):
            raise Exception('maxCapacityPerCore(%s) has to be a positive float value.' % str(maxCapacityPerCore))

        numTasks = data.numTasks
        if(not isinstance(numTasks, (int, long)) or (numTasks <= 0)):
            raise Exception('numTasks(%s) has to be a positive integer value.' % str(numTasks))

        minNumThreadsPerTask = data.minNumThreadsPerTask
        if(not isinstance(minNumThreadsPerTask, (int, long)) or (minNumThreadsPerTask <= 0)):
            raise Exception('minNumThreadsPerTask(%s) has to be a positive integer value.' % str(minNumThreadsPerTask))

        maxNumThreadsPerTask = data.maxNumThreadsPerTask
        if(not isinstance(maxNumThreadsPerTask, (int, long)) or (maxNumThreadsPerTask <= 0)):
            raise Exception('maxNumThreadsPerTask(%s) has to be a positive integer value.' % str(maxNumThreadsPerTask))

        minResourcesPerThread = data.minResourcesPerThread
        if(not isinstance(minResourcesPerThread, (int, long, float)) or (minResourcesPerThread <= 0)):
            raise Exception('minResourcesPerThread(%s) has to be a positive float value.' % str(minResourcesPerThread))

        maxResourcesPerThread = data.maxResourcesPerThread
        if(not isinstance(maxResourcesPerThread, (int, long, float)) or (maxResourcesPerThread <= 0)):
            raise Exception('maxResourcesPerThread(%s) has to be a positive float value.' % str(maxResourcesPerThread))

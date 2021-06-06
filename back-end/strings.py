from itertools import combinations

def getFilterText(criterionWeights, filter):
    weightsList = []
    weightsDict = {}
    for i in criterionWeights:
        weightsList.append(criterionWeights[i])
        weightsDict[criterionWeights[i]] = i
    comb = combinations(weightsList, 2)
    finalDict = {}
    for i in list(comb):
        firstValue = float(i[0])
        secondValue = float(i[1])
        res = (firstValue - secondValue) * 100 / secondValue
        if(firstValue>secondValue):
            message = str(weightsDict[i[0]]) + ' > ' + str(weightsDict[i[1]])
        elif(firstValue<secondValue):
            message = str(weightsDict[i[1]]) + ' > ' + str(weightsDict[i[0]])
        else:
            continue
        finalDict[message] = str(round(res, 2))
    return finalDict

def getDisplayName(filter):
    if(filter == 'stdDev'):
        return 'Consistency'
    elif(filter == 'errorRate'):
        return 'Error Rate'
    elif(filter  == 'elapsed'):
        return 'Elapsed Time'
    elif(filter == 'Connect'):
        return 'Connection Time'
    elif(filter == 'CPU'):
        return 'CPU Utilization'
    else:
        return filter


import databaseCommands as db
from pandas import DataFrame
from sklearn import linear_model
import numpy as np
import strings

def startProcessing(serviceType, instanceType, predictorValues, predictorNames):
    inputList = []
    print('predictorValues')
    print(predictorValues)
    print('predictorNames')
    print(predictorNames)
    predictorNames = predictorNames.split(",")
    print(predictorNames)
    elapsed = db.getElapsedForML(instanceType, serviceType)
    if('elapsed' in predictorNames):
        inputList.insert(predictorNames.index('elapsed'), elapsed)
    else:
        lastElement = elapsed
        lastElementName = 'elapsed'
    throughput = db.getThroughputForML(instanceType, serviceType)
    if('Throughput' in predictorNames):
        inputList.insert(predictorNames.index('Throughput'), throughput)
    else:
        lastElement = throughput
        lastElementName = 'Throughput'
    latency = db.getLatencyForML(instanceType, serviceType)
    if('Latency' in predictorNames):
        inputList.insert(predictorNames.index('Latency'), latency)
    else:
        lastElement = latency
        lastElementName = 'Latency'
    connect = db.getConnectForML(instanceType, serviceType)
    if('Connect' in predictorNames):
        inputList.insert(predictorNames.index('Connect'), connect)
    else:
        lastElement = connect
        lastElementName = 'Connect'
    stdDev = db.getStandardDeviationForML(instanceType, serviceType)
    if('stdDev' in predictorNames):
        inputList.insert(predictorNames.index('stdDev'), stdDev)
    else:
        lastElement = stdDev
        lastElementName = 'stdDev'
    errorRate = db.getErrorRateForML(instanceType, serviceType)
    if('errorRate' in predictorNames):
        inputList.insert(predictorNames.index('errorRate'), errorRate)
    else:
        lastElement = errorRate
        lastElementName = 'errorRate'
    inputList.append(lastElement)
    return (inputList, lastElementName)

def runML(serviceType, instanceType, predictorValues, predictorNames):
    res = startProcessing(serviceType, instanceType, predictorValues, predictorNames)
    ipList = res[0]
    lastElement = res[1]
    predictorValues = predictorValues.split(",")
    predictorNames = predictorNames.split(",")
    predictorValues = [float(i) for i in predictorValues]
    X = [ipList[:-1]]
    xarray = np.array(ipList[:-1], 'float')
    xarray = np.transpose(xarray)
    y = [ipList[-1]]
    yarray = np.array(ipList[-1], 'float')
    yarray = np.transpose(yarray)
    regr = linear_model.LinearRegression()
    regr.fit(xarray, yarray)
    predictedValue = regr.predict([predictorValues])
    print(predictedValue)
    predictedValueStr = 'For the entered values of '
    selectedValuesDict = {}
    finalDict = {}
    for i in range(0, len(predictorValues)):
        selectedValuesDict[strings.getDisplayName(str(predictorNames[i]))] = round(float(predictorValues[i]), 2)
    selectedValuesDict = str(selectedValuesDict)[1:-1]
    finalSVDict = {}
    finalSVDict["selectedValues"] = {selectedValuesDict}
    predictedValueDict = {}
    finalPVDict = {}
    pv = float(str(predictedValue)[1:-1])
    pvNo = str(round(pv, 2))
    predictedValueDict[strings.getDisplayName(str(lastElement))] = pvNo
    predictedValueDict = str(predictedValueDict)[1:-1]
    finalPVDict["predictedValues"] = {predictedValueDict}
    predictedValueRes = str(finalPVDict)[1:-1]
    selectedValuesRes = str(finalSVDict)[1:-1]
    finalData = selectedValuesRes + ', ' + predictedValueRes
    finalData = str(finalData)
    finalData = finalData.replace('"', '')
    finalData = finalData.replace("'", '"')
    finalData = '{' + finalData + '}'
    return finalData

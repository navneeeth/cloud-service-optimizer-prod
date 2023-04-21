import mysql.connector
import ahp
import time
from itertools import combinations
from credentials import host, database_name, username, password, port, auth_plugin

db =mysql.connector.connect(host=host,
database=database_name, user=username, password=password, port=port, auth_plugin=auth_plugin)
mycursor = db.cursor()

def dbInsert(statement, data):
    mycursor.execute(statement, data)

def dbSelect(statement):
    mycursor.execute(statement)
    result = mycursor.fetchall()
    return result

def isDuplicatePNumber(pno):
    mycursor.execute('select * from taskStatus where pno=\''+pno+'\';')
    result = mycursor.fetchall()
    print(result)
    if result == []:
        return False
    else:
        return True

def isDuplicateSNumber(sno):
    mycursor.execute('select * from sessionDetails where sno=\''+sno+'\';')
    result = mycursor.fetchall()
    if result == []:
        return False
    else:
        return True

def insertPNumber(pno):
    mycursor.execute('insert into taskStatus values(\''+pno+'\', \'Pending\');')
    db.commit()

def insertSNumber(sno, endpointID):
    mycursor.execute('insert into sessionDetails values(\''+sno+'\', \'Pending\', \''+endpointID+'\');')
    db.commit()

def logAPICall(name, timestamp):
    mycursor.execute('insert into APILogs values(\''+name+'\', \''+timestamp+'\');')
    db.commit()

def getFiles(endpointID):
    mycursor.execute('select files from endpointLogs where endpointID=\''+str(endpointID)+'\';')
    result = mycursor.fetchall()
    return result

def updateFiles(endpointID, filesString):
    mycursor.execute('update endpointLogs set files = \''+str(filesString)+'\' where endpointID = \''+str(endpointID)+'\';')
    db.commit()

def updateSession(sessionID):
    mycursor.execute('update sessionDetails set status = \'Complete\' where sno = \''+str(sessionID)+'\';')
    db.commit()

def insertEC2Logs(index, elapsed, responseCode, responseMessage, success, latency, connect, instanceType, endpointID, sessionID, timestamp):
    mycursor.execute('insert into ec2logs values(\''+str(index)+'\', \''+str(elapsed)+'\', \''+str(responseCode)+'\', \''+str(responseMessage)+'\', \''+str(success)+'\', \''+str(latency)+'\', \''+str(connect)+'\', \''+str(instanceType)+'\', \''
    +str(endpointID)+'\', \''+str(sessionID)+'\', \''+str(timestamp)+'\');')
    db.commit()

def insertEC2Performance(index, cpu, memory, instanceType, endpointID, sessionID, timestamp):
    mycursor.execute('insert into ec2performance values(\''+str(index)+'\', \''+str(cpu)+'\', \''+str(memory)+'\', \''+str(instanceType)+'\', \''
    +str(endpointID)+'\', \''+str(sessionID)+'\', \''+str(timestamp)+'\');')
    db.commit()

def insertEC2Summary(index, label, numberOfSamples, average, minVal, maxVal, stdDev, errorRate, throughput, receivedKBPS, sentKBPS, avgBytes, endpointID, sessionID, instanceType, timestamp):
    mycursor.execute('insert into ec2summary values(\''+str(index)+'\', \''+str(label)+'\', \''+str(numberOfSamples)+'\', \''+str(average)+'\', \''+str(minVal)+'\', \''+str(maxVal)+'\', \''+str(stdDev)+'\', \''+str(errorRate)+'\', \''
    +str(throughput)+'\', \''+str(receivedKBPS)+'\', \''+str(sentKBPS)+'\', \''+str(avgBytes)+'\', \''+str(endpointID)+'\', \''+str(sessionID)+'\', \''+str(instanceType)+'\', \''+str(timestamp)+'\');')
    db.commit()

def checkPassword(endpointID, password):
    mycursor.execute('select password from endpointAccess where endpointID=\''+str(endpointID)+'\';')
    result = mycursor.fetchall()
    result = str(result)
    result = result[3:-4]
    if(password==result):
        return 1
    else:
        return 0

def logLogin(endpointID, timestamp):
    mycursor.execute('insert into loginLogs values(\''+str(endpointID)+'\', \''+str(timestamp)+'\');')
    db.commit()

def getNoOfSamples(instanceType, serviceType):
    mycursor.execute('select summarySize from save'+str(serviceType)+' where instanceType = \''+str(instanceType)+'\';')
    noResult = mycursor.fetchall()
    noResultList = []
    for i in noResult:
        noResultList.append(str(i)[2:-3])
    noResultList = [float(ele) for ele in noResultList]
    return noResultList

def getNoOfPerformanceSamples(instanceType, serviceType):
    mycursor.execute('select performanceSize from save'+str(serviceType)+' where instanceType = \''+str(instanceType)+'\';')
    noResult = mycursor.fetchall()
    noResultList = []
    for i in noResult:
        noResultList.append(str(i)[2:-3])
    noResultList = [float(ele) for ele in noResultList]
    return noResultList

def getOverallThroughput(instanceType, serviceType):
    tpResultList = getThroughputs(instanceType, serviceType)
    noResultList = getNoOfSamples(instanceType, serviceType)
    tpProductsList = []
    for i in range(0, len(tpResultList)):
        tpProductsList.append(tpResultList[i]*noResultList[i])
    totalNumberOfSamples = 0
    tpProductsSum = 0
    for ele in range(0, len(noResultList)):
        totalNumberOfSamples = totalNumberOfSamples + noResultList[ele]
        tpProductsSum = tpProductsSum + tpProductsList[ele]
    if(len(noResultList) == 0):
        overallThroughput = 0
    else:
        overallThroughput = tpProductsSum / totalNumberOfSamples
    return str(overallThroughput)

def getNumberOfSamples(instanceType, serviceType):
    mycursor.execute('select numberOfSamples from '+str(serviceType)+'summary where instanceType = \''+str(instanceType)+'\';')
    noResult = mycursor.fetchall()
    noResultList = []
    for i in noResult:
        noResultList.append(str(i)[2:-3])
    noResultList = [float(ele) for ele in noResultList]
    return noResultList

def getThroughputs(instanceType, serviceType):
    mycursor.execute('select throughput from save'+str(serviceType)+' where instanceType = \''+str(instanceType)+'\';')
    tpResult = mycursor.fetchall()
    tpResultList = []
    for i in tpResult:
        tpResultList.append(str(i)[2:-3])
    tpResultList = [float(ele) for ele in tpResultList]
    return tpResultList

def getLatency(instanceType, serviceType):
    mycursor.execute('select Latency from '+str(serviceType)+'logs where instanceType = \''+str(instanceType)+'\';')
    result = mycursor.fetchall()
    resultList = []
    for i in result:
        resultList.append(str(i)[2:-3])

    resultList = [float(ele) for ele in resultList]
    if(len(resultList)==0):
        avg = 0
    else:
        avg = sum(resultList)/len(resultList)
    return str(avg)

def getErrorRates(instanceType, serviceType):
    mycursor.execute('select errorRate from save'+str(serviceType)+' where instanceType = \''+str(instanceType)+'\';')
    erResult = mycursor.fetchall()
    erResultList = []
    for i in erResult:
        erResultList.append(str(i)[2:-4])
    erResultList = [float(ele) for ele in erResultList]
    return erResultList

def getOverallErrorRate(instanceType, serviceType):
    erResultList = getErrorRates(instanceType, serviceType)
    noResultList = getNoOfSamples(instanceType, serviceType)
    erProductsList = []
    for i in range(0, len(erResultList)):
        erProductsList.append(erResultList[i]*noResultList[i])
    totalNumberOfSamples = 0
    erProductsSum = 0
    for ele in range(0, len(noResultList)):
        totalNumberOfSamples = totalNumberOfSamples + noResultList[ele]
        erProductsSum = erProductsSum + erProductsList[ele]
    if(len(noResultList) == 0):
        overallErrorRate = 0
    else:
        overallErrorRate = erProductsSum / totalNumberOfSamples
    return str(overallErrorRate)

def getElapsed(instanceType, serviceType):
    mycursor.execute('select elapsed from '+str(serviceType)+'logs where instanceType = \''+str(instanceType)+'\';')
    result = mycursor.fetchall()
    resultList = []
    for i in result:
        resultList.append(str(i)[2:-3])
    resultList = [float(ele) for ele in resultList]
    if(len(resultList)==0):
        avg = 0
    else:
        avg = sum(resultList)/len(resultList)
    return str(avg)

def getElapsedValues(instanceType, serviceType):
    mycursor.execute('select elapsed from save'+str(serviceType)+' where instanceType = \''+str(instanceType)+'\';')
    sdResult = mycursor.fetchall()
    sdResultList = []
    for i in sdResult:
        sdResultList.append(str(i)[2:-3])
    sdResultList = [float(ele) for ele in sdResultList]
    return sdResultList

def getLatencyValues(instanceType, serviceType):
    mycursor.execute('select Latency from save'+str(serviceType)+' where instanceType = \''+str(instanceType)+'\';')
    sdResult = mycursor.fetchall()
    sdResultList = []
    for i in sdResult:
        sdResultList.append(str(i)[2:-3])
    sdResultList = [float(ele) for ele in sdResultList]
    return sdResultList

def getConnectValues(instanceType, serviceType):
    mycursor.execute('select Connect from save'+str(serviceType)+' where instanceType = \''+str(instanceType)+'\';')
    sdResult = mycursor.fetchall()
    sdResultList = []
    for i in sdResult:
        sdResultList.append(str(i)[2:-3])
    sdResultList = [float(ele) for ele in sdResultList]
    return sdResultList

def getCPUValues(instanceType, serviceType):
    mycursor.execute('select cpu from save'+str(serviceType)+' where instanceType = \''+str(instanceType)+'\';')
    sdResult = mycursor.fetchall()
    sdResultList = []
    for i in sdResult:
        sdResultList.append(str(i)[2:-3])
    sdResultList = [float(ele) for ele in sdResultList]
    return sdResultList

def getMemoryValues(instanceType, serviceType):
    mycursor.execute('select memory from save'+str(serviceType)+' where instanceType = \''+str(instanceType)+'\';')
    sdResult = mycursor.fetchall()
    sdResultList = []
    for i in sdResult:
        sdResultList.append(str(i)[2:-3])
    sdResultList = [float(ele) for ele in sdResultList]
    return sdResultList

def getStoredElapsed(instanceType, serviceType):
    sdResultList = getElapsedValues(instanceType, serviceType)
    noResultList = getNoOfSamples(instanceType, serviceType)
    sdProductsList = []
    for i in range(0, len(sdResultList)):
        sdProductsList.append(sdResultList[i]*noResultList[i])
    totalNumberOfSamples = 0
    sdProductsSum = 0
    for ele in range(0, len(noResultList)):
        totalNumberOfSamples = totalNumberOfSamples + noResultList[ele]
        sdProductsSum = sdProductsSum + sdProductsList[ele]
    if(len(noResultList) == 0):
        overallElapsed = 0
    else:
        overallElapsed = sdProductsSum / totalNumberOfSamples
    return str(overallElapsed)

def getStoredLatency(instanceType, serviceType):
    sdResultList = getLatencyValues(instanceType, serviceType)
    noResultList = getNoOfSamples(instanceType, serviceType)
    sdProductsList = []
    for i in range(0, len(sdResultList)):
        sdProductsList.append(sdResultList[i]*noResultList[i])
    totalNumberOfSamples = 0
    sdProductsSum = 0
    for ele in range(0, len(noResultList)):
        totalNumberOfSamples = totalNumberOfSamples + noResultList[ele]
        sdProductsSum = sdProductsSum + sdProductsList[ele]
    if(len(noResultList) == 0):
        overallLatency = 0
    else:
        overallLatency = sdProductsSum / totalNumberOfSamples
    return str(overallLatency)

def getStoredConnect(instanceType, serviceType):
    sdResultList = getConnectValues(instanceType, serviceType)
    noResultList = getNoOfSamples(instanceType, serviceType)
    sdProductsList = []
    for i in range(0, len(sdResultList)):
        sdProductsList.append(sdResultList[i]*noResultList[i])
    totalNumberOfSamples = 0
    sdProductsSum = 0
    for ele in range(0, len(noResultList)):
        totalNumberOfSamples = totalNumberOfSamples + noResultList[ele]
        sdProductsSum = sdProductsSum + sdProductsList[ele]
    if(len(noResultList) == 0):
        overallConnect = 0
    else:
        overallConnect = sdProductsSum / totalNumberOfSamples
    return str(overallConnect)

def getStoredCPU(instanceType, serviceType):
    sdResultList = getCPUValues(instanceType, serviceType)
    noResultList = getNoOfPerformanceSamples(instanceType, serviceType)
    sdProductsList = []
    for i in range(0, len(sdResultList)):
        sdProductsList.append(sdResultList[i]*noResultList[i])
    totalNumberOfSamples = 0
    sdProductsSum = 0
    for ele in range(0, len(noResultList)):
        totalNumberOfSamples = totalNumberOfSamples + noResultList[ele]
        sdProductsSum = sdProductsSum + sdProductsList[ele]
    if(len(noResultList) == 0 or totalNumberOfSamples == 0):
        overallCPU = 0
    else:
        overallCPU = sdProductsSum / totalNumberOfSamples
    return str(overallCPU)

def getStoredMemory(instanceType, serviceType):
    sdResultList = getMemoryValues(instanceType, serviceType)
    noResultList = getNoOfPerformanceSamples(instanceType, serviceType)
    sdProductsList = []
    for i in range(0, len(sdResultList)):
        sdProductsList.append(sdResultList[i]*noResultList[i])
    totalNumberOfSamples = 0
    sdProductsSum = 0
    for ele in range(0, len(noResultList)):
        totalNumberOfSamples = totalNumberOfSamples + noResultList[ele]
        sdProductsSum = sdProductsSum + sdProductsList[ele]
    if(len(noResultList) == 0 or totalNumberOfSamples == 0):
        overallMemory = 0
    else:
        overallMemory = sdProductsSum / totalNumberOfSamples
    return str(overallMemory)

def getStandardDeviations(instanceType, serviceType):
    mycursor.execute('select stdDev from save'+str(serviceType)+' where instanceType = \''+str(instanceType)+'\';')
    sdResult = mycursor.fetchall()
    sdResultList = []
    for i in sdResult:
        sdResultList.append(str(i)[2:-3])
    sdResultList = [float(ele) for ele in sdResultList]
    return sdResultList

def getOverallStandardDeviation(instanceType, serviceType):
    sdResultList = getStandardDeviations(instanceType, serviceType)
    noResultList = getNoOfSamples(instanceType, serviceType)
    sdProductsList = []
    for i in range(0, len(sdResultList)):
        sdProductsList.append(sdResultList[i]*noResultList[i])
    totalNumberOfSamples = 0
    sdProductsSum = 0
    for ele in range(0, len(noResultList)):
        totalNumberOfSamples = totalNumberOfSamples + noResultList[ele]
        sdProductsSum = sdProductsSum + sdProductsList[ele]
    if(len(noResultList) == 0):
        overallStandardDeviation = 0
    else:
        overallStandardDeviation = sdProductsSum / totalNumberOfSamples
    return str(overallStandardDeviation)

def getConnect(instanceType, serviceType):
    mycursor.execute('select Connect from '+str(serviceType)+'logs where instanceType = \''+str(instanceType)+'\';')
    result = mycursor.fetchall()
    resultList = []
    for i in result:
        resultList.append(str(i)[2:-3])
    resultList = [float(ele) for ele in resultList]
    if(len(resultList)==0):
        avg = 0
    else:
        avg = sum(resultList)/len(resultList)
    return str(avg)

def getCPU(instanceType, serviceType):
    mycursor.execute('select cpu from '+str(serviceType)+'performance where instanceType = \''+str(instanceType)+'\';')
    result = mycursor.fetchall()
    resultList = []
    for i in result:
        resultList.append(str(i)[2:-3])
    resultList = [float(ele) for ele in resultList]
    if(len(resultList)==0):
        avg = 0
    else:
        avg = sum(resultList)/len(resultList)
    return str(avg)

def getMemory(instanceType, serviceType):
    mycursor.execute('select memory from '+str(serviceType)+'performance where instanceType = \''+str(instanceType)+'\';')
    result = mycursor.fetchall()
    resultList = []
    for i in result:
        resultList.append(str(i)[2:-3])
    resultList = [float(ele) for ele in resultList]
    if(len(resultList)==0):
        avg = 0
    else:
        avg = sum(resultList)/len(resultList)
    return str(avg)

def isServiceTypeNotLoaded(serviceType):
    mycursor.execute('select * from derivedValues where serviceType=\''+str(serviceType)+'\';')
    result = mycursor.fetchall()
    if result == []:
        return True
    else:
        return False

def isInstanceTypeNotLoaded(instanceType):
    mycursor.execute('select * from derivedValues where instanceType=\''+str(instanceType)+'\';')
    result = mycursor.fetchall()
    if result == []:
        return True
    else:
        return False

def insertDerivedValues(elapsed, latency, connect, cpu, memory, standardDeviation, errorRate, throughput, sessionID, endpointID, instanceType, serviceType, timestamp):
    mycursor.execute('insert into derivedValues values(\''+str(elapsed)+'\', \''+str(latency)+'\', \''+str(connect)+'\', \''+str(cpu)+'\', \''+str(memory)+'\', \''+str(standardDeviation)+'\', \''+str(errorRate)+'\', \''+str(throughput)+'\', \''+str(serviceType)+'\', \''
    +str(instanceType)+'\', \''+str(timestamp)+'\', \''+str(sessionID)+'\', \''+str(endpointID)+'\');')
    db.commit()

def updateExistingDerivedValues(elapsed, latency, connect, cpu, memory, standardDeviation, errorRate, throughput, sessionID, endpointID, instanceType, serviceType, timestamp):
    mycursor.execute('update derivedValues set elapsed = \''+str(elapsed)+'\', Latency = \''+str(latency)+'\', Connect = \''+
    str(connect)+'\', cpu = \''+str(cpu)+'\', memory = \''+str(memory)+'\', stdDev = \''+str(standardDeviation)+'\', errorRate = \''+str(errorRate)+'\', Throughput = \''+str(throughput)+
    '\', lastUpdated = \''+str(timestamp)+'\', sessionID = \''+str(sessionID)+'\', endpointID = \''+str(endpointID)+
    '\'where instanceType = \''+str(instanceType)+'\' and serviceType = \''+str(serviceType)+'\';')
    db.commit()

def updateDerivedValues(elapsed, latency, connect, cpu, memory, standardDeviation, errorRate, throughput, sessionID, endpointID, instanceType, serviceType, timestamp):
    serviceTypeFlag = 0
    instanceTypeFlag = 0
    if(isServiceTypeNotLoaded(serviceType)):
        serviceTypeFlag = 1
    if(isInstanceTypeNotLoaded(instanceType)):
        instanceTypeFlag = 1
    if(serviceTypeFlag or instanceTypeFlag):
        insertDerivedValues(elapsed, latency, connect, cpu, memory, standardDeviation, errorRate, throughput, sessionID, endpointID, instanceType, serviceType, timestamp)
    else:
        updateExistingDerivedValues(elapsed, latency, connect, cpu, memory, standardDeviation, errorRate, throughput, sessionID, endpointID, instanceType, serviceType, timestamp)

def updateDerivedCalculationLogs(endpointID, sessionID, serviceType, instanceType, timestamp):
    mycursor.execute('insert into derivedCalculationLogs values(\''+str(endpointID)+'\', \''+str(sessionID)+'\', \''+str(serviceType)+'\', \''+str(instanceType)+'\', \''+str(timestamp)+'\');')
    db.commit()

def getNameFromEndpointID(endpointID):
    mycursor.execute('select user from endpointData where endpointID=\''+str(endpointID)+'\';')
    result = mycursor.fetchall()
    result = str(result)[3:-4]
    return result

def getLatestID():
    mycursor.execute('select endpointID from endpointData where endpointID = (select max(endpointid) from endpointData)')
    result = mycursor.fetchall()
    if(result == []):
        return 2
    else:
        result = str(result)[3]
        return int(result)+1

def getLatestCount(tableName):
    mycursor.execute('select count(*) from '+str(tableName))
    result = mycursor.fetchall()
    result = str(result)[2:-3]
    if(result == '0'):
        return 0
    else:
        return int(result)+1

def updateEndpointData(id, name):
    mycursor.execute('insert into endpointData values (\''+str(id)+'\', \''+str(name)+'\');')
    db.commit()

def updateEndpointAccess(id, password):
    mycursor.execute('insert into endpointAccess values (\''+str(id)+'\', \''+str(password)+'\');')
    db.commit()

def initEndpointLogs(id):
    mycursor.execute('insert into endpointLogs values (\''+str(id)+'\', files = \'\');')
    db.commit()

def createEndpoint(name, password):
    id = getLatestID()
    updateEndpointData(id, name)
    updateEndpointAccess(id, password)
    initEndpointLogs(id)
    return id

def getRetrievedValue(fieldName, serviceType, instanceType):
    mycursor.execute('select '+str(fieldName)+' from derivedValues where serviceType=\''+str(serviceType)+'\' and instanceType = \''+str(instanceType)+'\';')
    result = mycursor.fetchall()
    result = str(result)[3:-4]
    end_time = time.time()
    return result


def insertPRequest(pNo, timestamp, filters, priorities, serviceType, instanceType):
    mycursor.execute('insert into processingRequests values (\''+str(pNo)+'\', \''+str(filters)+'\', \''+str(priorities)+'\', \''+
    str(serviceType)+'\', \''+str(instanceType)+'\', \''+str(timestamp)+'\');')
    db.commit()


def getRelativeValue(serviceType, firstParam, secondParam, fieldName):
    reversableValues = ['elapsed', 'stdDev', 'Latency', 'errorRate', 'Connect', 'cpu', 'memory', 'CPU']
    firstVal = getRetrievedValue(fieldName, serviceType, firstParam)
    secondVal = getRetrievedValue(fieldName, serviceType, secondParam)
    result = float(firstVal) / float(secondVal)
    if(fieldName in reversableValues):
        result = 1/result
    return result

def getRelativeRank(firstParam, secondParam, listOfFilters, priorities):
    firstParamIndex = listOfFilters.index(firstParam)
    firstValue = priorities[firstParamIndex]
    firstValue = 1 / float(firstValue)
    secondParamIndex = listOfFilters.index(secondParam)
    secondValue = priorities[secondParamIndex]
    secondValue = 1 / float(secondValue)
    relativeRank = firstValue / secondValue
    return relativeRank

def ahpCode(serviceType, listOfInstanceTypes, listOfFilters, priorities):
    start_time = time.time()
    comb = combinations(listOfInstanceTypes, 2)
    instancesDict = {}
    dictionaryList = []
    for j in listOfFilters:
        instancesDict.clear()
        comb1 = combinations(listOfInstanceTypes, 2)
        for i in list(comb1):
            instancesDict[i] = getRelativeValue(serviceType, str(i[0]), str(i[1]), str(j))
        dictionaryList.append(instancesDict.copy())
    comb2 = combinations(listOfFilters, 2)
    criteriaDict = {}
    for i in list(comb2):
        criteriaDict[i] = getRelativeRank(str(i[0]), str(i[1]), listOfFilters, priorities)
    end_time = time.time()
    print("processing for ahp code done in:")
    print("--- %s seconds ---" % (end_time - start_time))
    result = ahp.ahpProcessing(dictionaryList, criteriaDict, listOfFilters, listOfInstanceTypes)
    return result

def getFilters(pno):
    mycursor.execute('select filters from processingRequests where pno=\''+str(pno)+'\';')
    result = mycursor.fetchall()
    result = str(result)[3:-4]
    return result

def getServiceType(pno):
    mycursor.execute('select serviceType from processingRequests where pno=\''+str(pno)+'\';')
    result = mycursor.fetchall()
    result = str(result)[3:-4]
    return result

def getPriorities(pno):
    mycursor.execute('select priorities from processingRequests where pno=\''+str(pno)+'\';')
    result = mycursor.fetchall()
    result = str(result)[3:-4]
    return result

def getInstanceType(pno):


    mycursor.execute('select instanceType from processingRequests where pno=\''+str(pno)+'\';')
    result = mycursor.fetchall()
    result = str(result)[3:-4]
    return result

def updateTaskStatus(pno):
    mycursor.execute('update taskStatus set status = \'Complete\' where pno = \''+str(pno)+'\';')
    db.commit()

def insertAHPResult(result, pno, timestamp):
    weights = result
    resultStr = ''
    weights = str(weights)
    resultStr = resultStr + weights
    mycursor.execute('insert into ahpResults values (\''+str(pno)+'\', \''+resultStr+'\', \''+str(timestamp)+'\');')
    db.commit()

def updateResults(result, pNo, timestamp):
    updateTaskStatus(pNo)
    if(not isAS3Request(pNo)):
        insertAHPResult(result, pNo, timestamp)

def checkProcessingStatus(pNo):
    mycursor.execute('select status from taskStatus where pno=\''+str(pNo)+'\';')
    result = mycursor.fetchall()
    result = str(result)[3:-4]
    if result == 'Complete':
        return 1
    else:
        return 0

def checkIfProcessingIsDone(pNo):
    mycursor.execute('select status from taskStatus where pno=\''+str(pNo)+'\';')
    result = mycursor.fetchall()
    result = str(result)[3:-4]
    if result == 'Pending':
        return 1
    else:
        return 0

def isAS3Request(pNo):
    mycursor.execute('select serviceType from processingRequests where pno=\''+str(pNo)+'\';')
    result = mycursor.fetchall()
    result = str(result)[3:-4]
    if result == 's3':
        return 1
    else:
        return 0

def saveEC2(index, sessionID, endpointID, instanceType, serviceType, elapsed, latency, connect, stdDev, errorRate, throughput, summarySize, timestamp, cpu, memory, performanceSize):
    mycursor.execute('insert into saveec2 values(\''+str(index)+'\', \''+str(elapsed)+'\', \''+str(latency)+'\', \''+str(connect)+'\', \''+str(summarySize)+'\', \''+str(stdDev)+'\', \''+str(errorRate)+'\', \''+str(throughput)+'\', \''
    +str(performanceSize)+'\', \''+str(cpu)+'\', \''+str(memory)+'\', \''+str(instanceType)+'\', \''+str(endpointID)+'\', \''+str(sessionID)+'\', \''+str(timestamp)+'\');')
    db.commit()

def saveRDS(index, sessionID, endpointID, instanceType, serviceType, elapsed, latency, connect, stdDev, errorRate, throughput, summarySize, timestamp, cpu, memory, performanceSize):
    mycursor.execute('insert into saverds values(\''+str(index)+'\', \''+str(elapsed)+'\', \''+str(latency)+'\', \''+str(connect)+'\', \''+str(summarySize)+'\', \''+str(stdDev)+'\', \''+str(errorRate)+'\', \''+str(throughput)+'\', \''
    +str(performanceSize)+'\', \''+str(cpu)+'\', \''+str(memory)+'\', \''+str(instanceType)+'\', \''+str(endpointID)+'\', \''+str(sessionID)+'\', \''+str(timestamp)+'\');')
    db.commit()

def saveS3(index, sessionID, endpointID, instanceType, serviceType, elapsed, latency, connect, stdDev, errorRate, throughput, summarySize, timestamp, cpu, memory, performanceSize):
    mycursor.execute('insert into saves3 values(\''+str(index)+'\', \''+str(elapsed)+'\', \''+str(latency)+'\', \''+str(connect)+'\', \''+str(summarySize)+'\', \''+str(stdDev)+'\', \''+str(errorRate)+'\', \''+str(throughput)+'\', \''
    +str(performanceSize)+'\', \''+str(cpu)+'\', \''+str(memory)+'\', \''+str(instanceType)+'\', \''+str(endpointID)+'\', \''+str(sessionID)+'\', \''+str(timestamp)+'\');')
    db.commit()

def getElapsedForML(instanceType, serviceType):
    sdResultList = getElapsedValues(instanceType, serviceType)
    noResultList = getNoOfSamples(instanceType, serviceType)
    sdProductsList = []
    for i in range(0, len(sdResultList)):
        for j in range(1, int(noResultList[i])):
            sdProductsList.append(sdResultList[i])
    return sdProductsList

def getLatencyForML(instanceType, serviceType):
    sdResultList = getLatencyValues(instanceType, serviceType)
    noResultList = getNoOfSamples(instanceType, serviceType)
    sdProductsList = []
    for i in range(0, len(sdResultList)):
        for j in range(1, int(noResultList[i])):
            sdProductsList.append(sdResultList[i])
    return sdProductsList

def getConnectForML(instanceType, serviceType):
    sdResultList = getConnectValues(instanceType, serviceType)
    noResultList = getNoOfSamples(instanceType, serviceType)
    sdProductsList = []
    for i in range(0, len(sdResultList)):
        for j in range(1, int(noResultList[i])):
            sdProductsList.append(sdResultList[i])
    return sdProductsList

def getStandardDeviationForML(instanceType, serviceType):
    sdResultList = getStandardDeviations(instanceType, serviceType)
    noResultList = getNoOfSamples(instanceType, serviceType)
    sdProductsList = []
    for i in range(0, len(sdResultList)):
        for j in range(1, int(noResultList[i])):
            sdProductsList.append(sdResultList[i])
    return sdProductsList

def getErrorRateForML(instanceType, serviceType):
    erResultList = getErrorRates(instanceType, serviceType)
    noResultList = getNoOfSamples(instanceType, serviceType)
    erProductsList = []
    for i in range(0, len(erResultList)):
        for j in range(1, int(noResultList[i])):
            erProductsList.append(erResultList[i])
    return erProductsList

def getThroughputForML(instanceType, serviceType):
    tpResultList = getThroughputs(instanceType, serviceType)
    noResultList = getNoOfSamples(instanceType, serviceType)
    tpProductsList = []
    for i in range(0, len(tpResultList)):
        for j in range(1, int(noResultList[i])):
            tpProductsList.append(tpResultList[i])
    return tpProductsList

def getResultFromAHP(processingNumber):
    mycursor.execute('select results from ahpResults where pno=\''+str(processingNumber)+'\';')
    result = mycursor.fetchall()
    result = str(result)[3:-4]
    print(result)
    return result

from flask import Flask, render_template, jsonify, request
from flaskext.mysql import MySQL
from flask_cors import CORS, cross_origin
import random
import string
import datetime
import json
import ahp
import os
import time
from threading import Thread
from uwsgi_tasks import task, TaskExecutor
import threading
import databaseCommands as dbCommands
import mlCode as mlp

app = Flask(__name__)
CORS(app, support_credentials=True)
app.debug = True

def updateFilesInDB(endpointID, filesString):
    dbCommands.updateFiles(endpointID, filesString)

def logAPICall(name):
    timestamp = datetime.datetime.now()
    dbCommands.logAPICall(name, str(timestamp))

def generatePNumber():
    randomNo = 'p'
    randomNoChars = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(9)])
    randomNo = randomNo + randomNoChars
    print(randomNo)
    return randomNo

def generateSNumber():
    randomNo = 's'
    randomNoChars = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(9)])
    randomNo = randomNo + randomNoChars
    print(randomNo)
    return randomNo

def getValFromDb(text):
    #this function will use the entered text and search for statically
    #stored content in a table
    #if it matches a certain string, it will return it
    #else, it will say not found
    statement = "select content from staticContent where name = \'" + text + "\';"
    result = dbCommands.dbSelect(statement)
    if(result == []):
        return "not found"
    else:
        return result

def retrieveValuesFromDB():
    return dbCommands.retrieveValues()

def startProcessing(filters, serviceType, instanceType, priorities):
    filtersList = filters.split(",")
    instancesList = instanceType.split(",")
    prioritiesList = priorities.split(",")
    result = dbCommands.ahpCode(serviceType, instancesList, filtersList, prioritiesList)
    return result

def bgTask(pNo):
    print('Started thread:')
    val = getResultsFromProcessingNumber(pNo)

def processFilters(timestamp, filters, priorities, serviceType, instanceTypes):
    #it uses the filters as input and generates ahp and ml-based calculations
    errorMessage = ""
    filtersList = filters.split(",")
    prioritiesList = priorities.split(",")
    if (filters == ""):
        errorMessage+="Filters is missing."
    if(timestamp == ""):
        errorMessage+=" Timestamp is missing."
    if(serviceType == ""):
        errorMessage+=" ServiceType is missing."
    if(instanceTypes == ""):
        errorMessage+=" InstanceTypes is missing."
    if(priorities == ""):
        errorMessage+=" Priorities is missing."
    if(not len(filtersList) == len(prioritiesList)):
        errorMessage+=" Filters and Priorities length do not match."
    if errorMessage != "":
        return ("failure", errorMessage)
    else:
        pNo = generatePNumber()
        while(dbCommands.isDuplicatePNumber(pNo)):
            pNo = generatePNumber()
        dbCommands.insertPNumber(pNo)
        dbCommands.insertPRequest(str(pNo), timestamp, filters, priorities, serviceType, instanceTypes)
        return ("success", str(pNo))

def updateResult(result, pNo):
    timestamp = datetime.datetime.now()
    dbCommands.updateResults(result, pNo, str(timestamp))

def checkStatus(pNo):
    if(dbCommands.checkProcessingStatus(pNo)):
        return 1
    else:
        return 0

def checkIfProcessingIsDone(pNo):
    if(dbCommands.checkIfProcessingIsDone(pNo)):
        return 1
    else:
        return 0

def isAS3Request(pNo):
    if(dbCommands.isAS3Request(pNo)):
        return 1
    else:
        return 0

def getResultsFromPNo(text):
    if(not dbCommands.isDuplicatePNumber(text)):
        return (0, "Invalid PNo.")
    elif(checkIfProcessingIsDone(text)):
        return (0, "Processing for this pNo is still pending... Try again")
    else:
        result = dbCommands.getResultFromAHP(text)
        return result

def getResultsFromProcessingNumber(text):
    if(not dbCommands.isDuplicatePNumber(text)):
        return (0, "Invalid PNo.")
    elif(checkStatus(text)):
        return (0, "Processing for this pNo is complete!")
    else:
        filters = dbCommands.getFilters(text)
        serviceType = dbCommands.getServiceType(text)
        priorities = dbCommands.getPriorities(text)
        if(isAS3Request(text)):
            result = mlp.runML(serviceType, 'na', priorities, filters)
            updateResult(result, text)
            return result
        else:
            instanceType = dbCommands.getInstanceType(text)
            result = startProcessing(filters, serviceType, instanceType, priorities)
            updateResult(result, text)
            return result

def getLatestTimestamp(endpointID):
    filesString = dbCommands.getFiles(endpointID)
    return filesString

def initiateLogging(endpointID):
    sNo = generateSNumber()
    while(dbCommands.isDuplicateSNumber(sNo)):
        sNo = generateSNumber()
    dbCommands.insertSNumber(sNo, endpointID)
    return str(sNo)

def updateSessionInfo(sessionID):
    dbCommands.updateSession(sessionID)

def saveToEC2Summary(index, valuesList, sessionID, endpointID, instanceType, logsSummary, timestamp):
    label = valuesList[0]
    numberOfSamples = valuesList[1]
    average = valuesList[2]
    minVal = valuesList[3]
    maxVal = valuesList[4]
    stdDev = valuesList[5]
    errorRate = valuesList[6]
    throughput = valuesList[7]
    receivedKBPS = valuesList[8]
    sentKBPS = valuesList[9]
    avgBytes = valuesList[10]
    dbCommands.insertEC2Summary(index, label, numberOfSamples, average, minVal, maxVal, stdDev, errorRate, throughput, receivedKBPS, sentKBPS, avgBytes, endpointID, sessionID, instanceType, timestamp)

def saveSummaryInEC2(index, sessionID, endpointID, instanceType, logsSummary, timestamp):
    summary_dict = json.loads(logsSummary)
    valuesList = []
    print(summary_dict.values())
    for i in summary_dict.values():
        valuesList.append(i)
    print(valuesList)
    saveToEC2Summary(index, valuesList, sessionID, endpointID, instanceType, logsSummary, timestamp)

def saveSummaryDataInEC2(index, sessionID, endpointID, instanceType, logsSummary, timestamp):
    summary_dict = json.loads(logsSummary)
    valuesList = []


def saveToEC2Logs(index, valuesList, instanceType, sessionID, endpointID, timestamp):
    elapsed = valuesList[0]
    responseCode = valuesList[1]
    responseMessage = valuesList[2]
    success = valuesList[3]
    latency = valuesList[4]
    connect = valuesList[5]
    dbCommands.insertEC2Logs(index, elapsed, responseCode, responseMessage, success, latency, connect, instanceType, endpointID, sessionID, timestamp)

def saveToEC2Performance(index, valuesList, instanceType, sessionID, endpointID, timestamp):
    cpu = valuesList[0]
    memory = valuesList[1]
    dbCommands.insertEC2Performance(index, cpu, memory, instanceType, endpointID, sessionID, timestamp)

def saveLogsInEC2(sessionID, endpointID, instanceType, logs, timestamp):
    logs_dict = json.loads(logs)
    print(len(logs_dict))
    print("Logs Dict['elapsed']:")
    print(len(logs_dict.values()))
    index = dbCommands.getLatestCount('ec2logs')
    for j in range(1, len(logs_dict['elapsed'])):
        valuesList = []
        for i in logs_dict.values():
            valuesList.append(i.get(str(j)))
        saveToEC2Logs(index, valuesList, instanceType, sessionID, endpointID, timestamp)
        index = index + 1

def savePerformanceInEC2(sessionID, endpointID, instanceType, logsPerformance, timestamp):
    logs_dict = json.loads(logsPerformance)
    print(len(logs_dict))
    print("LogsPerformance Dict['CPU']:")
    print(len(logs_dict.values()))
    index = dbCommands.getLatestCount('ec2performance')
    for j in range(1, len(logs_dict['CPU'])):
        valuesList = []
        for i in logs_dict.values():
            valuesList.append(i.get(str(j)))
        saveToEC2Performance(index, valuesList, instanceType, sessionID, endpointID, timestamp)
        index = index + 1

def saveSummary(sessionID, endpointID, instanceType, serviceType, logsSummary, timestamp):
    if(serviceType=='ec2'):
        index = dbCommands.getLatestCount('ec2summary')
        saveSummaryInEC2(index, sessionID, endpointID, instanceType, logsSummary, timestamp)
        return 1
    if(endpointID == "hello"):
        return 0
    else:
        return 0

def saveSummaryData(sessionID, endpointID, instanceType, serviceType, logsSummary, timestamp):
    if(serviceType=='ec2'):
        saveSummaryDataInEC2(index, sessionID, endpointID, instanceType, logsSummary, timestamp)
        return 1
    if(endpointID == "hello"):
        return 0
    else:
        return 0

def saveLogs(sessionID, endpointID, instanceType, serviceType, logs, timestamp):
    if(serviceType=='ec2'):
        saveLogsInEC2(sessionID, endpointID, instanceType, logs, timestamp)
        return 1
    if(endpointID == "hello"):
        return 0
    else:
        return 0

def savePerformance(sessionID, endpointID, instanceType, serviceType, logsPerformance, timestamp):
    if(serviceType=='ec2'):
        savePerformanceInEC2(sessionID, endpointID, instanceType, logsPerformance, timestamp)
        return 1
    if(endpointID == "hello"):
        return 0
    else:
        return 0

def checkPassword(endpointID, password):
    if(dbCommands.checkPassword(endpointID, password)):
        return 1
    else:
        return 0

def logLogin(endpointID, timestamp):
    dbCommands.logLogin(endpointID, timestamp)

def attemptLogin(endpointID, password, timestamp):
    if(checkPassword(endpointID, password)):
        logLogin(endpointID, timestamp)
        return "success"
    else:
        return "failure"

def updateDerivedValues(sessionID, endpointID, instanceType, serviceType, timestamp):
    elapsed = dbCommands.getElapsed(instanceType, serviceType)
    latency = dbCommands.getLatency(instanceType, serviceType)
    connect = dbCommands.getConnect(instanceType, serviceType)
    cpu = dbCommands.getCPU(instanceType, serviceType)
    memory = dbCommands.getMemory(instanceType, serviceType)
    standardDeviation = dbCommands.getOverallStandardDeviation(instanceType, serviceType)
    errorRate = dbCommands.getOverallErrorRate(instanceType, serviceType)
    throughput = dbCommands.getOverallThroughput(instanceType, serviceType)
    cpu = dbCommands.getCPU(instanceType, serviceType)
    memory = dbCommands.getMemory(instanceType, serviceType)
    dbCommands.updateDerivedValues(elapsed, latency, connect, cpu, memory, standardDeviation, errorRate, throughput, sessionID, endpointID, instanceType, serviceType, timestamp)
    dbCommands.updateDerivedCalculationLogs(endpointID, sessionID, serviceType, instanceType, timestamp)

def getNameFromEndpointID(endpointID):
    name = dbCommands.getNameFromEndpointID(endpointID)
    return name

def createEndpoint(name, password):
    endpointID = dbCommands.createEndpoint(name, password)
    return str(endpointID)

def updateDerValues(sessionID, endpointID, instanceType, serviceType, timestamp):
    elapsed = dbCommands.getStoredElapsed(instanceType, serviceType)
    latency = dbCommands.getStoredLatency(instanceType, serviceType)
    connect = dbCommands.getStoredConnect(instanceType, serviceType)
    cpu = dbCommands.getStoredCPU(instanceType, serviceType)
    memory = dbCommands.getStoredMemory(instanceType, serviceType)
    standardDeviation = dbCommands.getOverallStandardDeviation(instanceType, serviceType)
    errorRate = dbCommands.getOverallErrorRate(instanceType, serviceType)
    throughput = dbCommands.getOverallThroughput(instanceType, serviceType)
    dbCommands.updateDerivedValues(elapsed, latency, connect, cpu, memory, standardDeviation, errorRate, throughput, sessionID, endpointID, instanceType, serviceType, timestamp)
    dbCommands.updateDerivedCalculationLogs(endpointID, sessionID, serviceType, instanceType, timestamp)

def saveEC2(index, sessionID, endpointID, instanceType, serviceType, elapsed, latency, connect, stdDev, errorRate, throughput, summarySize, timestamp, cpu, memory, performanceSize):
    dbCommands.saveEC2(index, sessionID, endpointID, instanceType, serviceType, elapsed, latency, connect, stdDev, errorRate, throughput, summarySize, timestamp, cpu, memory, performanceSize)

def saveRDS(index, sessionID, endpointID, instanceType, serviceType, elapsed, latency, connect, stdDev, errorRate, throughput, summarySize, timestamp, cpu, memory, performanceSize):
    dbCommands.saveRDS(index, sessionID, endpointID, instanceType, serviceType, elapsed, latency, connect, stdDev, errorRate, throughput, summarySize, timestamp, cpu, memory, performanceSize)

def saveS3(index, sessionID, endpointID, instanceType, serviceType, elapsed, latency, connect, stdDev, errorRate, throughput, summarySize, timestamp, cpu, memory, performanceSize):
    dbCommands.saveS3(index, sessionID, endpointID, instanceType, serviceType, elapsed, latency, connect, stdDev, errorRate, throughput, summarySize, timestamp, cpu, memory, performanceSize)

def saveLogData(sessionID, endpointID, instanceType, serviceType, elapsed, latency, connect, stdDev, errorRate, throughput, summarySize, timestamp, isPerformanceIncluded, cpu, memory, performanceSize):
    if(serviceType == 'ec2'):
        index = dbCommands.getLatestCount('saveec2')
        if(isPerformanceIncluded == '1'):
            saveEC2(index, sessionID, endpointID, instanceType, serviceType, elapsed, latency, connect, stdDev, errorRate, throughput, summarySize, timestamp, cpu, memory, performanceSize)
        else:
            saveEC2(index, sessionID, endpointID, instanceType, serviceType, elapsed, latency, connect, stdDev, errorRate, throughput, summarySize, timestamp, 0, 0, 0)
        return 1
    elif(serviceType == 'rds'):
        #do rds
        index = dbCommands.getLatestCount('saverds')
        saveRDS(index, sessionID, endpointID, instanceType, serviceType, elapsed, latency, connect, stdDev, errorRate, throughput, summarySize, timestamp, 0, 0, 0)
        return 1
    elif(serviceType == 's3'):
        #do s3
        index = dbCommands.getLatestCount('saves3')
        saveS3(index, sessionID, endpointID, instanceType, serviceType, elapsed, latency, connect, stdDev, errorRate, throughput, summarySize, timestamp, 0, 0, 0)
        return 1
    else:
        return 0

@app.route('/', methods = ['GET'])
def hello():
    return "Hello! Welcome to the server of Cloud Service Optimizer!"

@app.route('/test-route/', methods = ['POST'])
def test_method():
    param1 = request.args.get("p1")
    param2 = request.args.get("p2")
    print(param1)
    print(param2)
    value = jsonify({
    "status": "success",
    "params": str(param1) + " and " + str(param2)
    })
    return value

@app.route('/front-end/get-content/', methods=['GET', 'OPTIONS'])
def front_end_get_content():

    logAPICall('f/get-content')
    val = ""
    text = ""
    text = request.args.get("string")
    val = getValFromDb(text)
    if(val=="not found"):
        value = jsonify({
        "status": "failure",
        "message": ""
        })
        value.headers.add('Access-Control-Allow-Origin', '*')
        value.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return value
    else:
        value = jsonify({
        "status": "success",
        "message": val
        })
        value.headers.add('Access-Control-Allow-Origin', '*')
        value.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return value


@app.route('/front-end/post-process-filters/', methods=['POST'])
def front_end_post_process_filters():
    logAPICall('f/get-process-filters')
    request_data = request.get_json()
    serviceType = request_data['serviceType']
    timestamp = request_data['timestamp']
    filters = request_data['filters']
    priorities = request_data['priorities']
    instanceType = request_data['instanceType']
    val = ()
    val = processFilters(timestamp, filters, priorities, serviceType, instanceType)
    value = jsonify({
    "status": val[0],
    "message": val[1]
    })
    value.headers.add('Access-Control-Allow-Origin', '*')
    value.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return value

@app.route('/front-end/get-results/', methods=['GET', 'OPTIONS'])
def front_end_get_results():
    val = ""
    text = ""
    text = request.args.get("processingNumber")
    val = getResultsFromProcessingNumber(text)
    if(val[0]==0):
        value = jsonify({
        "status": "failure",
        "data": val[1],
        "processingNumber": text
        })
        value.headers.add('Access-Control-Allow-Origin', '*')
        value.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return value
    else:
        val1 = json.loads(val)
        value = jsonify({
        "status": "success",
        "payload": val1,
        "processingNumber": text
        })
        value.headers.add('Access-Control-Allow-Origin', '*')
        value.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return value

@app.route('/endpoints/get-files/', methods=['POST'])
def endpoints_get_latest_timestamp():
    logAPICall('e/get-files')
    request_data = request.get_json()
    endpointID = request_data['endpointID']
    val = getLatestTimestamp(endpointID)
    return jsonify({
    "status": "success",
    "message": val,
    "endpointID": endpointID
    })

@app.route('/endpoints/update-files/', methods=['POST'])
def endpoints_update_files():
    logAPICall('e/update_files')
    request_data = request.get_json()
    endpointID = request_data['endpointID']
    sessionID = request_data['sessionID']
    filesString = request_data['filesString']
    print(filesString)
    updateFilesInDB(endpointID, filesString)
    updateSessionInfo(sessionID)
    return jsonify({
    "status": "success",
    "message": "Files list updated.",
    "endpointID": endpointID,
    "filesString": filesString
    })

@app.route('/endpoints/initiate-logging/', methods=['GET'])
def endpoints_initiate_logging():
    logAPICall('e/initiate-logging')
    val = ""
    endpointID = ""
    endpointID = request.args.get("endpointID")
    val = initiateLogging(endpointID)
    return jsonify({
    "status": "success",
    "message": val
    })


@app.route('/endpoints/post-logs/', methods=['POST'])
def endpoints_post_summary():
    logAPICall('e/post-logs')
    request_data = request.get_json()
    sessionID = request_data['sessionID']
    endpointID = request_data['endpointID']
    instanceType = request_data['instanceType']
    serviceType = request_data['serviceType']
    logsSummary = request_data['logsSummary']
    logs = request_data['logs']
    timestamp = request_data['timestamp']
    isPerformanceIncluded = request_data['isPerformanceIncluded']
    logsPerformance = request_data['logsPerformance']
    val = saveSummary(sessionID, endpointID, instanceType, serviceType, logsSummary, timestamp)
    val2 = saveLogs(sessionID, endpointID, instanceType, serviceType, logs, timestamp)
    val3 = 1
    if(isPerformanceIncluded == '1'):
        val3 = savePerformance(sessionID, endpointID, instanceType, serviceType, logsPerformance, timestamp)
    if(val and val2 and val3):
        print("In update derived values")
        updateDerivedValues(sessionID, endpointID, instanceType, serviceType, timestamp)
    if(not val or not val2 or not val3):
        return jsonify({
        "status": "failure",
        "message": val,
        "sessionID": sessionID,
        "endpointID": endpointID,
        "serviceType": serviceType,
        "instanceType": instanceType
        })
    else:
        return jsonify({
        "status": "success",
        "message": val,
        "sessionID": sessionID,
        "endpointID": endpointID,
        "serviceType": serviceType,
        "instanceType": instanceType
        })

@app.route('/endpoints/post-log-data/', methods=['POST'])
def endpoints_post_log_data():
    logAPICall('e/post-log-data')
    request_data = request.get_json()
    sessionID = request_data['sessionID']
    endpointID = request_data['endpointID']
    instanceType = request_data['instanceType']
    serviceType = request_data['serviceType']
    elapsed = request_data['elapsed']
    latency = request_data['latency']
    connect = request_data['connect']
    stdDev = request_data['stdDev']
    errorRate = request_data['errorRate']
    throughput = request_data['throughput']
    summarySize = request_data['summarySize']
    timestamp = request_data['timestamp']
    isPerformanceIncluded = request_data['isPerformanceIncluded']
    cpu = request_data['cpu']
    memory = request_data['memory']
    performanceSize = request_data['performanceSize']
    val = saveLogData(sessionID, endpointID, instanceType, serviceType, elapsed, latency, connect, stdDev, errorRate, throughput, summarySize, timestamp, isPerformanceIncluded, cpu, memory, performanceSize)
    if(val):
        print("In update derived values")
        updateDerValues(sessionID, endpointID, instanceType, serviceType, timestamp)
    if(not val):
        return jsonify({
        "status": "failure",
        "message": val,
        "sessionID": sessionID,
        "endpointID": endpointID,
        "serviceType": serviceType,
        "instanceType": instanceType
        })
    else:
        return jsonify({
        "status": "success",
        "message": val,
        "sessionID": sessionID,
        "endpointID": endpointID,
        "serviceType": serviceType,
        "instanceType": instanceType
        })

@app.route('/endpoints/endpoint-login/', methods=['POST'])
def endpoints_endpoint_login():
    logAPICall('e/endpoint_login')
    request_data = request.get_json()
    endpointID = request_data['endpointID']
    password = request_data['password']
    timestamp = request_data['timestamp']
    result = attemptLogin(endpointID, password, timestamp)
    if(result == "success"):
        name = getNameFromEndpointID(endpointID)
        return jsonify({
        "status": "success",
        "message": name,
        "endpointID": endpointID
        })
    else:
        return jsonify({
        "status": "failure",
        "message": "Invalid credentials.",
        "endpointID": endpointID
        })

@app.route('/endpoints/create-endpoint/', methods=['POST'])
def endpoints_create_endpoint():
    logAPICall('e/create-endpoint')
    request_data = request.get_json()
    name = request_data['name']
    password = request_data['password']
    result = createEndpoint(name, password)
    return jsonify({
    "status": "success",
    "message": result,
    "name": name
    })

if __name__ == '__main__':
    app.run()

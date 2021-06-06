#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import csv
import pandas as pd
import json
import os
import requests
import datetime
import time
fileName = 'data/Log_11052021.csv'
path = './../bigLogsDir/'
endpointID = 2
separator = '/'
url = 'http://cloud-service-optimizer-dev.herokuapp.com/'

def attemptLogin(eID, pwd):
    headersPost = {'Content-type': 'application/json'}
    timestamp = datetime.datetime.now()
    postData = { "endpointID": str(eID), "password": str(pwd), "timestamp": str(timestamp)}
    postData = json.dumps(postData)
    responseFile = requests.post(url+'endpoints/endpoint-login/', data = postData, headers = headersPost)
    responseFile = json.loads(responseFile.text)
    if(responseFile['status'] == 'success'):
        return (1, responseFile['message'])
    else:
        return (0, responseFile['message'])

def attemptSignup(name, password):
    headersPost = {'Content-type': 'application/json'}
    postData = { "name": str(name), "password": str(password)}
    postData = json.dumps(postData)
    responseFile = requests.post(url+'endpoints/create-endpoint/', data = postData, headers = headersPost)
    responseFile = json.loads(responseFile.text)
    if(responseFile['status'] == 'success'):
        return (1, responseFile['message'], responseFile['name'])
    else:
        return (0, responseFile['message'], responseFile['name'])

loginFailure = 1

while(loginFailure):
    inputFailure = 1
    while(inputFailure):
        loginOrSignup = input('Press 1 for logging in. Press 0 for creating/registering an endpoint:\n')
        if(not loginOrSignup == '1' and not loginOrSignup =='0'):
            print("Wrong input. Please try again.")
        else:
            inputFailure = 0
    if(loginOrSignup == '1'):
        eID = input("Enter endpoint ID:\n")
        pwd = input("Enter password:\n")
        print("Checking login credentials...")
        loginResult = attemptLogin(eID, pwd)
        if(loginResult[0]):
            print("Successfully logged in to "+str(loginResult[1])+"!\n")
            pathFailure = 1
            while(pathFailure):
                separatorCheckFailure = 1
                while(separatorCheckFailure):
                    separatorCheck = input('If Windows, press 1. If non-Windows, press 0.')
                    if(separatorCheck == '0' or separatorCheck == '1'):
                        separatorCheckFailure = 0
                    else:
                        print('Invalid entry. Please try again.')
                if(separatorCheck == '1'):
                    separator = '\\' + '\\'
                else:
                    separator = '/'
                enteredPath = input('Enter the path where the logs are stored:')
                separatorValid = '/'
                if(separatorCheck == '1'):
                    separatorValid = '\\'  
                if(not enteredPath[-1] == separatorValid):
                    enteredPath = enteredPath + separator
                if(os.path.isdir(enteredPath)):
                    pathFailure = 0
                else:
                    print('The entered directory does not exist. Please try again.')
            loginFailure = 0
        else:
            print("Invalid credentials. Try again.")
    else:
        name = input('Please enter your name:\n')
        passwordsDoNotMatch = 1
        while(passwordsDoNotMatch):
            password = input('Please create your password:\n')
            confirmPassword = input('Please confirm your password:\n')
            if(password == confirmPassword):
                passwordsDoNotMatch = 0
            else:
                print("Passwords do not match. Try again.")
        signupResult = attemptSignup(name, password)
        if(signupResult[0]):
            print("Successfully signed up user "+str(signupResult[2]))
            print("Your endpoint ID to log in is: "+str(signupResult[1]))
        print("Login with created credentials:")
        eID = input("Enter endpoint ID:\n")
        pwd = input("Enter password:\n")
        print("Checking login credentials...")
        loginResult = attemptLogin(eID, pwd)
        if(loginResult[0]):
            print("Successfully logged in to "+str(loginResult[1])+"!\n")
            pathFailure = 1
            while(pathFailure):
                separatorCheckFailure = 1
                while(separatorCheckFailure):
                    separatorCheck = input('If Windows, press 1. If non-Windows, press 0.')
                    if(separatorCheck == '0' or separatorCheck == '1'):
                        separatorCheckFailure = 0
                    else:
                        print('Invalid entry. Please try again.')
                if(separatorCheck == '1'):
                    separator = '\\' + '\\'
                else:
                    separator = '/'
                enteredPath = input('Enter the path where the logs are stored:')
                separatorValid = '/'
                if(separatorCheck == '1'):
                    separatorValid = '\\'
                if(not enteredPath[-1] == separatorValid):
                    enteredPath = enteredPath + separator
                if(os.path.isdir(enteredPath)):
                    pathFailure = 0
                else:
                    print('The entered directory does not exist. Please try again.') 
            loginFailure = 0
        else:
            print("Invalid credentials. Try again.")
endpointID = eID
path = enteredPath

def getFilesInServer(endpointID):
    headersPost = {'Content-type': 'application/json'}
    postData = { "endpointID": str(endpointID)}
    postData = json.dumps(postData)
    responseFile = requests.post(url+'endpoints/get-files/', data = postData, headers = headersPost)
    responseFile = json.loads(responseFile.text)
    if(responseFile['status'] == 'success'):
        strFiles = str(responseFile['message'])
        strFiles = strFiles[3:]
        strFiles = strFiles[:-3]
        strFiles = strFiles[:]
        return strFiles
    else:
        return ''

def initiateLogging(endpointID):
    ploads = {'endpointID': str(endpointID)}
    responseFile = requests.get(url+'endpoints/initiate-logging', params = ploads)
    responseFile = json.loads(responseFile.text)
    if(responseFile['status'] == "success"):
        return responseFile['message']

filesInServer = getFilesInServer(endpointID)
sessionID = initiateLogging(endpointID)
print("Your login session ID is:"+str(sessionID))

def uploadLogFile(isPerformanceIncluded, performanceJSON, logsJSON, summaryJSON, sessionID, endpointID, serviceType, instanceType):
    headersPost = {'Content-type': 'application/json'}
    timestamp = datetime.datetime.now()
    postData = {}
    if(isPerformanceIncluded):
        postData = { "sessionID": sessionID, "endpointID": endpointID, "serviceType": serviceType, "instanceType": instanceType, "elapsed": str(logsJSON[0]), "latency": str(logsJSON[1]), "connect": str(logsJSON[2]), "stdDev": str(summaryJSON[0]), "errorRate": str(summaryJSON[1]), "throughput": str(summaryJSON[2]), "summarySize": str(summaryJSON[3]), "timestamp": str(timestamp), "isPerformanceIncluded": '1', "cpu": str(performanceJSON[0]), "memory": str(performanceJSON[1]), "performanceSize": str(performanceJSON[2])}
    else:
        postData = { "sessionID": sessionID, "endpointID": endpointID, "serviceType": serviceType, "instanceType": instanceType, "elapsed": str(logsJSON[0]), "latency": str(logsJSON[1]), "connect": str(logsJSON[2]), "stdDev": str(summaryJSON[0]), "errorRate": str(summaryJSON[1]), "throughput": str(summaryJSON[2]), "summarySize": str(summaryJSON[3]), "timestamp": str(timestamp), "isPerformanceIncluded": '0', "cpu": '', "memory": '', "performanceSize": ''}
    postData = json.dumps(postData)
    start_time = time.time()
    response = requests.post(url+'endpoints/post-log-data/', data = postData, headers=headersPost)
    end_time = time.time()
    print("Upload done in:")
    print("--- %s seconds ---" % (end_time - start_time))

def getElapsed(df):
    return df.mean()
    
def getLatency(df):
    return df.mean()

def getConnect(df):
    return df.mean()

def readLogFile(filePath):
    df = pd.read_csv(filePath, usecols = ['elapsed', 'responseCode', 'responseMessage', 'success', 'Latency', 'Connect'])
    df = df[1:]
    elapsed = getElapsed(df["elapsed"])
    latency = getLatency(df["Latency"])
    connect = getConnect(df["Connect"])
    return(elapsed, latency, connect)
    json_str = df.to_json()
    return json_str
    
def readSummaryFile(filePath):
    df = pd.read_csv(filePath, usecols = ['Label', '# Samples', 'Average', 'Min', 'Max', 'Std. Dev.', 'Error %', 'Throughput', 'Received KB/sec', 'Sent KB/sec', 'Avg. Bytes'])
    df = df.iloc[0]
    sizeOfFile = df['# Samples']
    stdDev = df['Std. Dev.']
    errorRate = df['Error %']
    throughput = df['Throughput']
    return (stdDev, errorRate, throughput, sizeOfFile)
    json_str = df.to_json()
    return json_str

def readPerformanceFile(filePath):
    df = pd.read_csv(filePath, usecols = ['CPU', 'Memory'])
    df = df[1:]
    sizeOfFile = len(df.index)
    cpu = df["CPU"].mean()
    memory = df["Memory"].mean()
    return (cpu, memory, sizeOfFile)
    
def updateFilesListInServer(filesList, endpointID, sessionID):
    headersPost = {'Content-type': 'application/json'}
    postData = { "sessionID": sessionID, "endpointID": endpointID, "filesString": filesList}
    postData = json.dumps(postData)
    response = requests.post(url+'endpoints/update-files/', data = postData, headers=headersPost)

    
filesList = filesInServer 

flag = 0 
print('Going through files...')
for serviceType in os.listdir(path):
    if os.path.isdir(path+serviceType) and (serviceType == 'ec2' or serviceType == 'rds'):
        subpath = path+serviceType
        for instanceType in os.listdir(subpath):
            if os.path.isdir(subpath + separator + instanceType):
                suppath = subpath + separator + instanceType
                for filename in os.listdir(suppath):
                    if os.path.isfile(suppath+separator+filename) and filename.endswith('_l.csv'):
                        filePath = suppath+separator+filename
                        summaryFile = filename[:-5] + 's.csv'
                        performanceFile = filename[:-5] + 'p.csv'
                        summaryPath = suppath + separator + summaryFile
                        performancePath = suppath + separator + performanceFile
                        if filesList.find(filePath) == -1:
                            print("Currently uploading file:")
                            print(filePath)
                            logsJSON = readLogFile(filePath)
                            summaryJSON = readSummaryFile(summaryPath)
                            if(os.path.exists(performancePath)):
                                performanceJSON = readPerformanceFile(performancePath)
                                uploadLogFile(1, performanceJSON, logsJSON, summaryJSON, sessionID, endpointID, serviceType, instanceType)
                            else:
                                uploadLogFile(0, '', logsJSON, summaryJSON, sessionID, endpointID, serviceType, instanceType)
                            print('File uploaded successfully!')
                            filesList = filesList + filePath + ', '
                            flag = 1
    elif(os.path.isdir(path+serviceType) and (serviceType == 's3')):
        subpath = path+serviceType
        for filename in os.listdir(subpath):
            if os.path.isfile(subpath+separator+filename) and filename.endswith('_l.csv'):
                filePath = subpath+separator+filename
                summaryFile = filename[:-5] + 's.csv'
                summaryPath = subpath + separator + summaryFile
                if filesList.find(filePath) == -1:
                    print("Currently uploading s3 file:")
                    print(filePath)
                    logsJSON = readLogFile(filePath)
                    summaryJSON = readSummaryFile(summaryPath)
                    uploadLogFile(0, '', logsJSON, summaryJSON, sessionID, endpointID, serviceType, 'na')
                    print('File uploaded successfully!')
                    filesList = filesList + filePath + ', '
                    flag = 1
                    print('Read the s3 file')
if(flag):
    filesList = filesList[:-2]
    print('Uploaded files list:'+filesList)
else:
    print("No new files to be uploaded.")
updateFilesListInServer(filesList, endpointID, sessionID)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from CompareImpl import Compare
import json
import strings
import time

def ahpProcessing(comparisonsList, criterionList, listOfFilters, listOfInstanceTypes):
    start_time = time.time()
    ahpList = []
    for i in range(0, len(comparisonsList)):
        contentArea = Compare(listOfFilters[i], comparisonsList[i], precision=3, random_index='saaty')
        ahpList.append(contentArea)
    end_time = time.time()
    print("first for loop done in:")
    print("--- %s seconds ---" % (end_time - start_time))
    localWeights = []
    localWeightsDict = {}
    j = 0
    subFilterTextDict = {}
    finalDict = {}
    subDisplayNameTextDict = {}
    criterionWeights = []
    criterionWeightsDict = {}
    filterTextDict = {}
    displayNameTextDict = {}
    criteria = Compare('Ranks', criterionList, precision = 3, random_index='saaty')
    criteria.add_children(ahpList)
    criterionWeights.append(criteria.target_weights)
    criterionWeightsDict["data"] = criteria.target_weights
    filterTextDict["filterCompare"] = strings.getFilterText(criteria.target_weights, "Overall")
    displayNameTextDict["displayName"] = "Overall"
    localWeightsRes = str(localWeightsDict)[:-1]
    criterionWeightsRes = str(criterionWeightsDict)[1:-1]
    filterTextRes = str(filterTextDict)[1:-1]
    displayNameRes = str(displayNameTextDict)[1:-1]
    finalData = filterTextRes + ', ' + criterionWeightsRes + ', ' + displayNameRes
    finalDict["overall"] = {finalData[:]}
    start_time=time.time()
    for i in ahpList:
        localWeightsDict["data"] = i.local_weights
        subFilterTextDict["filterCompare"] = strings.getFilterText(i.local_weights, strings.getDisplayName(listOfFilters[j]))
        subDisplayNameTextDict["displayName"] = strings.getDisplayName(listOfFilters[j])
        localWeightsRes = str(localWeightsDict)[1:-1]
        subFilterTextRes = str(subFilterTextDict)[1:-1]
        subDisplayNameRes = str(subDisplayNameTextDict)[1:-1]
        finalSubData = subFilterTextRes + ', ' + localWeightsRes + ', ' + subDisplayNameRes
        finalDict[listOfFilters[j]] = {finalSubData[:]}
        j = j + 1
    end_time = time.time()
    print("second for loop done in:")
    print("--- %s seconds ---" % (end_time - start_time))
    finalDict = str(finalDict)
    finalDict = finalDict.replace('"', '')
    finalDict = finalDict.replace("'", '"')
    return finalDict

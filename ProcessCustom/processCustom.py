'''
This function will take -- in order --
baselineFile: a pickle of the baseline acDict (from pickleCustomOutputs)
comparisonFile: a pickle of the acDict to compare against
outputFileName: name of output csv file to create
'''

''' This gets the function arguments '''
import sys
import os.path

# print 'Number of arguments:', len(sys.argv), 'arguments.'
# print 'Argument List:', str(sys.argv)
#
# if len(sys.argv) != 3:
#     print "   Error: need exactly two arguments after file name"
#     print "          baselineFileName comparisonFolder"
#     sys.exit()
#
# # Unpack inputs
# baselineFile    = sys.argv[1]
# comparisonFolder = sys.argv[2]
#
# # Check that inputs exist
# if not os.path.isfile(baselineFile):
#     print "   Error: {0} does not exist".format(baselineFile)
#     sys.exit()
# elif not os.path.isdir(comparisonFolder):
#     print "   Error: {0} does not exist".format(comparisonFolder)
#     sys.exit()
#
''' Now start the actual processing work '''
from customFunctions import *
import numpy as np
import pickle
import glob

#
# comparisonPickleVec = glob.glob1(comparisonFolder, "*.pkl")

# baselineFile = "/Users/tcolvin1/Desktop/LevelOneOutputsTrans/2018Files/000.pkl"
# comparisonFolder = "/Users/tcolvin1/Desktop/LevelOneOutputsTrans/2018Files/"
# fileNames = ["001.pkl"]
# comparisonPickleVec = ["{0}{1}".format(comparisonFolder, obj) for obj in fileNames]


baselineFile = "/Users/tcolvin1/Desktop/LevelOneOutputsTrans/BaselineFiles/222.pkl"
comparisonFolder = "/Users/tcolvin1/Desktop/LevelOneOutputsTrans/BaselineFiles"
fileNames = ["223.pkl"]
comparisonPickleVec = ["{0}{1}".format(comparisonFolder, obj) for obj in fileNames]





[aircraftDictBaseline, trash] = pickle.load( open( baselineFile, "rb" ) )


#### Debug, scope some stuff here
reroutedAcList = []
deltaTime       = []
deltaDistance   = []
deltaFuel       = []
reroutedAcList_Base = []
totalFuel = []

for comparisonFile in comparisonPickleVec:
    outputFileName = "{0}.csv".format(comparisonFile.split('.')[0])

    # Read in the raw output from FACET
    [aircraftDictComparison, aircraftFilterDict]    = pickle.load( open( comparisonFile, "rb" ) )
    aircraftFilterSet                               = sorted(set(aircraftFilterDict.keys()))

    # aircraftDictBaseline['N100NR_223']  # Rerouted
    # aircraftDictComparison['N100NR_223']  # Rerouted
    #
    # aircraftDictBaseline['N100NR_25']   # Not rerouted
    # aircraftDictComparison['N100NR_25']   # Not rerouted

    # Determine which AC are rerouted
    reroutedAcList = []
    for curAC in sorted(aircraftDictComparison.keys()):
        if CURR_AVOIDANCE_RTE in aircraftDictComparison[curAC]['isRerouted']:
            reroutedAcList.append(curAC)

    # reroutedAcList = sorted(aircraftDictComparison.keys())
    print len(reroutedAcList)

    deltaTime       = []
    deltaDistance   = []
    deltaFuel       = []
    # hackOffset      = -1   #Needed to convert from comparison to baseline.

    reroutedAcList_Base = []
    totalFuel = []

    for key in reroutedAcList:

        try:
            print "Trying {0}".format(key)
            baseline    = aircraftDictBaseline[key]
            reroutedAcList_Base.append(key)
        except:
            # IDs are off.  In general not a consistent offset.  Find the closest ID.
            sign, id = key.split("_")

            possibleIDs = []
            for baseKey in aircraftDictBaseline.keys():
                if sign == baseKey.split("_")[0]:
                    print "  ERROR {0}".format(baseKey)
                    possibleIDs.append(int(baseKey.split("_")[1]))
            possibleIDs = np.array(possibleIDs)
            closestIX = np.argmin(abs(possibleIDs - int(id)))

            baseKey = "{0}_{1}".format(sign,possibleIDs[closestIX])
            print "  FIXED {0}".format(baseKey)
            baseline    = aircraftDictBaseline[baseKey]
            reroutedAcList_Base.append(baseKey)



        comparison  = aircraftDictComparison[key]

        deltaTime.append(comparison['flightTime'] - baseline['flightTime'])
        deltaDistance.append(comparison['flightDistance'] - baseline['flightDistance'])
        deltaFuel.append(comparison['fuelBurn'] - baseline['fuelBurn'])

        totalFuel.append(baseline['fuelBurn'])

    aggregateDeltaTime      = sum(deltaTime)
    aggregateDeltaDistance  = sum(deltaDistance)
    aggregateDeltaFuel      = sum(deltaFuel)

    minutesInFilter = [(np.diff(aircraftFilterDict[curKey])[0]/60 + 1) for curKey in aircraftFilterSet ]
    aggMinutesInFilter = sum(minutesInFilter)

    print "From {0}".format(comparisonFile)
    print 'number rerouted          = {0}'.format(len(reroutedAcList))
    print 'aggregateDeltaTime       = {0} minutes'.format(aggregateDeltaTime)
    print 'aggregateDeltaDistance   = {0} naut miles'.format(aggregateDeltaDistance)
    print 'aggregateDeltaFuel       = {0} lbs'.format(aggregateDeltaFuel)
    print "reroutedAcList           = {0}".format(reroutedAcList)
    print 'number filtered          = {0}'.format(len(aircraftFilterSet))
    print "aircraftFilterSet        = {0}".format(aircraftFilterSet)
    print "\n\n\n"

    outputKeys = ['rerouted',
                  'DeltaTime',
                  'DeltaDist',
                  'DeltaFuel',
                  'numFilter',
                  'sumFilterMinutes']

    outputVals = [len(reroutedAcList),
                  aggregateDeltaTime,
                  aggregateDeltaDistance,
                  aggregateDeltaFuel,
                  len(aircraftFilterSet),
                  aggMinutesInFilter]


    outFile = open(outputFileName,'w')
    outFile.write('#' + ','.join(outputKeys) + '\n')
    outFile.write(','.join([str(obj) for obj in outputVals]) + '\n\n')

    outFile.write("#rerouted\n")
    outFile.write(','.join(reroutedAcList) + '\n\n')

    outFile.write("#filtered, {0}\n".format(len(aircraftFilterSet)))
    outFile.write(','.join(aircraftFilterSet) + '\n')
    outFile.write(','.join([str(obj) for obj in minutesInFilter]) + '\n')
    outFile.close()

#### Debuggin
# zip(reroutedAcList_Base, reroutedAcList, deltaDistance, deltaFuel)

km2miles = 0.62
fuelDensity	= 6.75  # lbs/gal
nmi2miles = 1.15
kg2lbs = 2.2
gal2liter = 3.785

numRerouted = len(reroutedAcList)

for ix in range(numRerouted):
    d = deltaDistance[ix]
    f = deltaFuel[ix]
    if abs(d) > 1e-6:
        print "{0:10}{1:8.2f}[l/km]{2:8.2f}[lbs]{3:8.2f}[nmi]{4:8.2f}".format(reroutedAcList[ix].split('_')[0], (f/fuelDensity*gal2liter)/(d*nmi2miles/km2miles), f, d, deltaTime[ix])
        # print "{0:10}{1:8.2f}[l/km]{2:8.2f}[lbs]{3:8.2f}[nmi]{4:8.2f}".format(reroutedAcList[ix].split('_')[0], (f/fuelDensity*gal2liter)/(d*nmi2miles/km2miles), f, d, deltaTime[ix])
        # print "{0:10}{1:8.2f}[lbs/nmi]{2:8.2f}[lbs]{3:8.2f}[nmi]{4:8.2f}".format(reroutedAcList[ix].split('_')[0], f/d, f, d, deltaTime[ix])
    else:
        print "{0}, no distance change, {1} [lbs], {2} [mins]".format(reroutedAcList[ix].split('_')[0], deltaFuel[ix], deltaTime[ix])


print "Total Fuel efficiency on rerouted legs = {0}".format((sum(deltaFuel)/fuelDensity*gal2liter)/(sum(deltaDistance)*nmi2miles/km2miles))
sum(deltaDistance) / sum(deltaFuel)

#### Try to GE plot
toPlotDict_Base = readCustomFacetFile_LatLon("/Users/tcolvin1/Desktop/LevelOneOutputs/000_Custom_Nothing.cst", reroutedAcList_Base)
toPlotDict_Comp = readCustomFacetFile_LatLon("/Users/tcolvin1/Desktop/LevelOneOutputs/001_Custom_2018Low.cst", reroutedAcList)

ft2m = 0.3048

fileNameGE = 'testFlightTracks.kml'

flatArray       = []  #lat lon alt vx vy vz lat lon alt vx vy vz lat lon ...
numTimeSteps    = []
callSigns       = []

filterAircraft = []
# filterAircraft = reroutedAcList
# for curSign in sorted(aircraftDictComparison.keys()):

numRerouted = len(reroutedAcList)

# for curSign in sorted(reroutedAcList):
for CSix in range(numRerouted):
    curSign_C = reroutedAcList[CSix]
    curSign_B = reroutedAcList_Base[CSix]
    curSign = curSign_B.split('_')[0]
    # curSign = flightRecord[0]
    # dataList = flightRecord[1]
    dataC     = toPlotDict_Comp[curSign_C]
    dataB    = toPlotDict_Base[curSign_B]

    noFilter = (len(filterAircraft) == 0)

    # if curSign == 'AWI377_LNK':
    if noFilter or (curSign in filterAircraft):

        subFlatArray = []
        # for entry in dataListBaseline['latLonFL']:
        for entry in zip(dataB['lat'], dataB['lon'], dataB['FL']):
            # Don't care about velocity information here, so just use zeros
            # entry[2] = entry[2]*100  #The units are wrong anyways, should be meters, not feet
            # subFlatArray.extend(entry)

            subFlatArray.append(entry[0])
            subFlatArray.append(entry[1])
            subFlatArray.append(entry[2] * 100 * ft2m)
            subFlatArray.extend([0,0,0])

        flatArray.extend(subFlatArray)
        numTimeSteps.extend([len(dataB['lat'])])
        callSigns.append(curSign + "_B")

        subFlatArray = []
        # for entry in dataC['latLonFL']:
        for entry in zip(dataC['lat'], dataC['lon'], dataC['FL']):

            # Don't care about velocity information here, so just use zeros
            # entry[2] = entry[2]*100  #The units are wrong anyways, should be meters, not feet
            # subFlatArray.extend(entry)

            subFlatArray.append(entry[0])
            subFlatArray.append(entry[1])
            subFlatArray.append(entry[2] * 100 * ft2m)
            subFlatArray.extend([0,0,0])

        flatArray.extend(subFlatArray)
        numTimeSteps.extend([len(dataC['lat'])])
        callSigns.append(curSign + "_R")

# import sys
# Points to the python scripts needed from Francisco
# friscoFiles = "../GoogleEarth/"

sys.path.append("../GoogleEarth/")
import GoogleEarth as GE

# data2GE.convertTJC(fileNameGE, flatArray, numTimeSteps, numRuns = len(numTimeSteps), cutoffNAS = False, maxTimeSteps = 1e10)
GE.convertTJCAircraft(fileNameGE, flatArray, numTimeSteps, callSigns, numElementsPerLine = 6)



#### Debug on N65WW
curSign_C = "N65WW_27860"
curSign_B = "N65WW_27859"

toPlotDict_Base[curSign_B]
toPlotDict_Comp[curSign_C]
curTimeSteps = len(toPlotDict_Base[curSign_B]['grndSpd'])
# for () zip(toPlotDict_Base[curSign_B]['grndSpd'], toPlotDict_Comp[curSign_C]['grndSpd'])



# curKey = 'AAL1366_20194'
# aircraftDictComparison[curKey]
# aircraftDictBaseline[curKey]
#
# zip(reroutedAcList, [(aircraftDictComparison[curKey]['fuelBurn'],aircraftDictComparison[curKey]['acType'])  for curKey in reroutedAcList])
# zip(reroutedAcList_Base, [aircraftDictBaseline[curKey]['fuelBurn'] for curKey in reroutedAcList_Base])
#
#
# totalNASFuel = []
# totalNASTime = []
# totalNASDist = []
# for (curKey, curAC) in aircraftDictBaseline.iteritems():
#     totalNASFuel.append(curAC['fuelBurn'])
#     totalNASTime.append(curAC['flightTime'] - int(curAC['firstTime']))
#     totalNASDist.append(curAC['flightDistance'])
#
#     if curAC['fuelBurn'] == 5.02:
#         print curKey
#
#
# import matplotlib.pyplot as plt
# (n, bins, patches)  = plt.hist(totalNASFuel, bins=100, range=[0,100000])
# plt.show()
#
# curKey = 'DAL1500_15763'
# curAC = aircraftDictBaseline[curKey]
# curAC['flightTime'] - int(curAC['firstTime'])























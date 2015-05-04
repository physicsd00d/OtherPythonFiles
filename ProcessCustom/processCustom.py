'''
This function will take -- in order --
baselineFile: a pickle of the baseline acDict (from pickleCustomOutputs)
comparisonFile: a pickle of the acDict to compare against
outputFileName: name of output csv file to create
'''

''' This gets the function arguments '''
import sys
import os.path

print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)

if len(sys.argv) != 4:
    print "   Error: need exactly three arguments after file name"
    print "          fileToFilterOn fileToPrune outputFile"
    sys.exit()

# Unpack inputs
baselineFile    = sys.argv[1]
comparisonFile  = sys.argv[2]
outputFileName  = sys.argv[3]

# Check that inputs exist
if not os.path.isfile(baselineFile):
    print "   Error: {0} does not exist".format(baselineFile)
    sys.exit()
elif not os.path.isfile(comparisonFile):
    print "   Error: {0} does not exist".format(comparisonFile)
    sys.exit()

''' Now start the actual processing work '''
from customFunctions import *
import numpy as np
import pickle

# Read in the raw output from FACET
[aircraftDictBaseline, trash]                   = pickle.load( open( baselineFile, "rb" ) )
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

for key in reroutedAcList:

    try:
        print "Trying {0}".format(key)
        baseline    = aircraftDictBaseline[key]
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


    comparison  = aircraftDictComparison[key]

    deltaTime.append(comparison['flightTime'] - baseline['flightTime'])
    deltaDistance.append(comparison['flightDistance'] - baseline['flightDistance'])
    deltaFuel.append(comparison['fuelBurn'] - baseline['fuelBurn'])

aggregateDeltaTime      = sum(deltaTime)
aggregateDeltaDistance  = sum(deltaDistance)
aggregateDeltaFuel      = sum(deltaFuel)

minutesInFilter = [(np.diff(aircraftFilterDict[curKey])[0]/60 + 1) for curKey in aircraftFilterSet ]
aggMinutesInFilter = sum(minutesInFilter)

print 'number rerouted          = {0}'.format(len(reroutedAcList))
print 'aggregateDeltaTime       = {0} minutes'.format(aggregateDeltaTime)
print 'aggregateDeltaDistance   = {0} naut miles'.format(aggregateDeltaDistance)
print 'aggregateDeltaFuel       = {0} lbs'.format(aggregateDeltaFuel)
print "reroutedAcList           = {0}".format(reroutedAcList)
print 'number filtered          = {0}'.format(len(aircraftFilterSet))
print "aircraftFilterSet        = {0}".format(aircraftFilterSet)

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

outFile.write("#filtered\n")
outFile.write(','.join(aircraftFilterSet) + '\n')
outFile.write(','.join([str(obj) for obj in minutesInFilter]) + '\n')
outFile.close()

























import os
import sys
import numpy as np

UNCHECKED_AVOIDANCE_RTE = 1
NO_AVOIDANCE_RTE        = 2
CURR_AVOIDANCE_RTE      = 3

# //curr_ac->avoidance_status
# //enum {
# //    UNCHECKED_AVOIDANCE_RTE = 1,
# //    NO_AVOIDANCE_RTE        = 2,
# //    CURR_AVOIDANCE_RTE      = 3,
# //    NO_AVOIDANCE_CELLS      = 4,
# //    CHECKED_AVOIDANCE_CELLS = 5,
# //    NEW_AVOIDANCE_CELLS     = 6,
# //    CLEARED_AVOIDANCE_RTE   = 7
# //};

def readCustomFacetFile(facetFileName):

    aircraftDict = dict()
    sectorDict = dict()

    # These are the names of the variables within the output file
    keyVals = []
    numKeys = -1

    inFile = open(facetFileName, 'r')

    for line in inFile:
        curLine = []

        curValues = line.split()

        # Skip empty lines
        if len(line) == 0:
            continue

        # Skip comments
        if line[0] == '#':
            continue

        # The @ line contains the key names for the values
        if line[0] == '@':
            keyVals = line[1:].split()
            numKeys = len(keyVals)
            print keyVals
            continue

        # This must be an error
        if len(curValues) != numKeys:
            print 'ERROR!!!!'
            raise RuntimeError

        # Anything else had better be data
        # put it into a dictionary
        curLine = dict(zip(keyVals, curValues))

        # Things we want to save:
        #   * Total Flight Time
        #   * Total Flight Distance

        # Combine callsign and intID into a single (unique) key
        callSignKey = '{0}_{1}'.format(curLine['acID'], curLine['intID'])

        # If this is the first time we've seen this aircraft, initialize its dictionary entry
        if not aircraftDict.has_key(callSignKey):
            aircraftDict[callSignKey] = {'flightTime'   : -1,   'flightDistance'    : -1,
                                         'fuelBurn'     : -1,   'isRerouted'        : set()}

        # Pull down the dictionary of the current aircraft (this might be pointer to dictionary?)
        curAC = aircraftDict[callSignKey]

        # By virtue of seeing this aircraft again, that means that surely time and distance are updated

        #
        # Update Time of flight
        #
        curTime = int(curLine['time'])
        if (curTime > curAC['flightTime']):
            curAC['flightTime'] = curTime
        else:
            print 'UNEXPECTED time BEHAVIOUR!!!'
            raise RuntimeError

        #
        # Update distance traveled
        #
        curDist = float(curLine['dist'])
        if (curDist > curAC['flightDistance']):
            curAC['flightDistance'] = curDist
        else:
            print 'UNEXPECTED dist BEHAVIOUR!!!'
            raise RuntimeError

        #
        # Update fuel burned
        #   * I'm noticing some AC with zero fuel burn.  It might be that there is no BADA model for this type of AC.
        #     If that's the case, then perhaps don't update if fuel brn is zero (which will leave it at -1 in the record)
        #
        curFuel = float(curLine['fuelBrn'])
        if curFuel == 0.:
            None
        elif (curFuel > curAC['fuelBurn']):
            curAC['fuelBurn'] = curFuel
        else:
            print 'UNEXPECTED fuelBrn BEHAVIOUR!!!'
            raise RuntimeError

        #
        # Update isRerouted flags
        #
        curFlag = int(curLine['isRerouted'])
        curAC['isRerouted'].add(curFlag)

        # If this is the first time we've seen this sector, initialize its dictionary entry
        sectorKey = curLine['sector']
        if not sectorDict.has_key(sectorKey):
            sectorDict[sectorKey] = {'timeList' : [], 'ACList' : []}

        # Pull down the current sector
        curSector = sectorDict[sectorKey]

        if curTime in curSector['timeList']:
            # We have already seen this time before!  Find the index that this time represents
            curIX = len(curSector['timeList'])-1    #Assuming times never decrease
            curSector['ACList'][curIX].append(callSignKey)
        else:
            # We haven't yet seen this time, so the lists are empty
            curSector['timeList'].append(curTime)
            curIX = len(curSector['timeList'])-1
            # print 'timeList = {0}'.format(curSector['timeList'])
            # print 'curIX = {0}'.format(curIX)
            curSector['ACList'].append([callSignKey])

    return aircraftDict, sectorDict




def readFilter(filterName):

    aircraftDict = set()
    inFile = open(filterName, 'r')

    for line in inFile:

        curValues = line.split()

        # Skip empty lines
        if len(line) == 0:
            continue

        # Skip everything that's not a TRACK
        if curValues[0] != 'TRACK':
            continue

        id, callsign = curValues[1:3]

        acKey = "{0}_{1}".format(callsign, id)

        if acKey not in aircraftDict:
            aircraftDict.add(acKey)

    return aircraftDict



resultsFolder   = 'Results/'


# '''
# Script
# '''
# if __name__ == "__main__":
resultsFolder   = '/Users/tcolvin1/Desktop/LevelOneOutputs/'
customFacetFileBaseline     = '000_Custom_Nothing.cst'
customFacetFileComparison   = '001_Custom_2018Low.cst'
customFacetFilter           = '001_Filter_2018Low.flt'

sys.exit()

# Read in the raw output from FACET
aircraftDictBaseline,   sectorDictBaseline      = readCustomFacetFile(resultsFolder + customFacetFileBaseline)
aircraftDictComparison, sectorDictComparison    = readCustomFacetFile(resultsFolder + customFacetFileComparison)
aircraftFilterSet                               = readFilter(resultsFolder + customFacetFilter)

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

print 'number rerouted          = {0}'.format(len(reroutedAcList))
print 'aggregateDeltaTime       = {0} minutes'.format(aggregateDeltaTime)
print 'aggregateDeltaDistance   = {0} naut miles'.format(aggregateDeltaDistance)
print 'aggregateDeltaFuel       = {0} lbs'.format(aggregateDeltaFuel)
print "reroutedAcList           = {0}".format(reroutedAcList)
print 'number filtered          = {0}'.format(len(aircraftFilterSet))
print "aircraftFilterSet        = {0}".format(aircraftFilterSet)


#### Debugging.  Why is rerouted dist/fuel ratio so terrible?  What is mpg of overall flight?
km2miles = 0.62
fuelDensity	= 6.75  # lbs/gal
nmi2miles = 1.15
kg2lbs = 2.2
gal2liter = 3.785

testSignC = "AAL1016_27228"
testSignB = "AAL1016_27227"
print aircraftDictComparison[testSignC]['flightDistance']   # Claims to be nmi (that checks out via GE)
print aircraftDictComparison[testSignC]['fuelBurn']  # Claims to be lbs (that checks out via fuel efficiency calc)
dist = aircraftDictComparison[testSignC]['flightDistance']
fuel = aircraftDictComparison[testSignC]['fuelBurn']
distKm = dist * nmi2miles / km2miles
fuelLiter = (fuel / fuelDensity) * gal2liter
print "{0} [l/km]".format(fuelLiter /distKm )
print "{0} [lbs/nmi]".format(fuel /dist )

compDist = dist
compFuel = fuel
compDistKm = distKm
compFuelLiter = fuelLiter


# TRACK AAL1016 MD83 000 000 1 1 0 NONE NONE 330
#     FP_ROUTE KTUS..TUS..BURRO..VAINE..MESCA..CIE..ALIBY..HOWRD..LINZY..INK..PHILS..TQA..MEDLY..SITNA..GEENI..CADES..SICUM..JEN..FEVER..ISABL..LUCCK..YAMEL..DFW..KDFW


print aircraftDictBaseline[testSignB]['flightDistance']
print aircraftDictBaseline[testSignB]['fuelBurn']
dist = aircraftDictBaseline[testSignB]['flightDistance']
fuel = aircraftDictBaseline[testSignB]['fuelBurn']
distKm = dist * nmi2miles / km2miles
fuelLiter = (fuel / fuelDensity) * gal2liter
print fuelLiter / (distKm )

baseDist = dist
baseFuel = fuel
baseDistKm = distKm
baseFuelLiter = fuelLiter

distDiffKm = compDistKm - baseDistKm
fuelDiffLiter = compFuelLiter - baseFuelLiter
print fuelDiffLiter/distDiffKm
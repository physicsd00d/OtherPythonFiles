import os
import sys
import numpy as np

from datetime import timedelta
from datetime import datetime
refDate = datetime(1970,1,1,0,0,0)      #FACET refDate is refDate = datetime(1970,1,1,0,0,0)

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

def convertDegreesToDegMinSec(val):
    Deg = int(np.floor(val))
    Min = int((val - Deg)*60.)
    Sec = int((val - Deg - Min/60.)*3600.)
    return [Deg, Min, Sec]

def convertDegMinSecStringToDegrees(val):
    if ('.' in val) or ('-' in val):
        print '# This cannot accomodate decimals in the seconds or negative signs.'
        raise RuntimeError

    Seconds      = float(val[-2:])
    Minutes      = float(val[-4:-2])
    if len(val) == 6:
        Degrees  = float(val[:2])
    elif len(val) == 7:
        Degrees  = float(val[:3])
    else:
        print "BAD LONGITUDE FORMAT: {0}".format(val)
        raise RuntimeError

    return Degrees + Minutes/60. + Seconds/3600.

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
            aircraftDict[callSignKey] = {'flightTime'   : -1e9,   'flightDistance'    : -1,
                                         'fuelBurn'     : -1,   'isRerouted'        : set(),
                                         'latLonFL'     : [],   'timeVec' : []}

        # Pull down the dictionary of the current aircraft (this might be pointer to dictionary?)
        curAC = aircraftDict[callSignKey]

        # By virtue of seeing this aircraft again, that means that surely time and distance are updated

        #
        # Update Time of flight
        #
        curTime = int(curLine['time'])
        if (curTime >= curAC['flightTime']):
            curAC['flightTime'] = curTime
        else:
            print 'UNEXPECTED time BEHAVIOUR!!!'
            raise RuntimeError

        #
        # Update distance traveled
        #
        curDist = float(curLine['dist'])
        if (curDist >= curAC['flightDistance']):
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

        #
        # Record the track info
        #
        curAC['latLonFL'].append([float(curLine['lat']), float(curLine['lon']), float(curLine['alt'])])
        curAC['timeVec'].append(int(curLine['time']))

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

'''
This function REQUIRES that the timestep be exactly one minute and that that times start on the minute
'''
def readTRXIntoDictByTimeFromStart(inFileName):
    print 'readTRXIntoDictByTimeFromStart for ' + str(inFileName)

    TRXKeys = ['Callsign', 'AcType', 'LatN-HMS', 'LonW-HMS', 'GrndSpdKnots', 'FlightLevel', 'Center', 'Sector', 'FiledLevel']

    # Best idea for keys is callsign_departureAirport
    TRX_Storage = dict()

    startDatetimeMidnight = -1
    try:
        inputFile = open(inFileName, 'r')

        # This will hold the information as we run through the lines until it's time to save it to the dictionary
        curTime = -1
        trackDatetime = -1
        curFPLine = ''
        curTrackLine = ''
        # shouldPrint = False

        for line in inputFile:
            key = line.split()

            if len(key) > 0:
                if key[0] == 'TRACK_TIME':
                    # Indicates progress
                    curTime = int(key[1])
                    trackDatetime = refDate + timedelta(seconds=curTime)
                    if startDatetimeMidnight == -1:
                        startDatetimeMidnight = trackDatetime.replace(hour=0,minute=0,second=0)


                elif key[0] == 'TRACK':
                    # if filterCallsigns:
                    #     shouldPrint = (key[1] in callsigns)    #Sets it true
                    #
                    # if filterSectorNames:
                    #     shouldPrint = shouldPrint or (key[8] in set(sectorNames))   # Another chance to be true
                    #
                    # # modifiedSign = key[1] + '_' + suffixList[fileCounter]
                    # if (key[1] == 'EJM626'):
                    #     print 'DEBUG {0}, shouldPrint {1}'.format(key[1], shouldPrint)
                    curTrackLine = line

                elif key[0] == 'FP_ROUTE':
                    curFPLine = line

                    # Assemble the key callSign_depAiport
                    # Pull out the things we care about from the TRACK line
                    trackKeys       = curTrackLine.split()
                    curAcDict = dict(zip(TRXKeys, trackKeys[1:]))
                    curAcDict['FlightPlan'] = curFPLine.split()[1]

                    # Store by minutes since operation start
                    minutesSinceMidnight = int((trackDatetime - startDatetimeMidnight).total_seconds()/60.)

                    # Create this time record if necessary
                    if not TRX_Storage.has_key(minutesSinceMidnight):
                        TRX_Storage[minutesSinceMidnight] = dict()

                    # Store the info
                    TRX_Storage[minutesSinceMidnight][curAcDict['Callsign']] = curAcDict

                elif key[0][0] == '#':
                    # print 'COMMENT'
                    None

                else:
                    print "pruneTRXFromList: NewLine! This should not have been hit!"
                    print key
                    print line

    except:
        print "pruneTRXFromList: FAILURE in reading the file"
        printOkay = 0
        raise

    return TRX_Storage




'''
Script
'''
# resultsFolder   = 'ResultsForOct31/'
resultsFolder   = 'ResultsForNov13/'
# customFacetFileBaseline     = 'LevelOne_CustomOutput_NoSUAs'
customFacetFileComparison   = 'LevelOne_CustomOutput_FalconCapeTraditional'
customAirTopFileComparison  = 'LevelOne_FromAirtop'
customFacetFileBaseline = customAirTopFileComparison

# customFacetFileComparison   = 'LevelOne_CustomOutput_FalconCapeEnvelope'
launchDate = datetime(2013, 3, 1, 0, 0, 0)      #FACET refDate is refDate = datetime(1970,1,1,0,0,0)


# Read in the raw output from FACET
aircraftDictBaseline,   sectorDictBaseline      = readCustomFacetFile(resultsFolder + customFacetFileBaseline)
aircraftDictComparison, sectorDictComparison    = readCustomFacetFile(resultsFolder + customFacetFileComparison)

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
for key in reroutedAcList:
    baseline    = aircraftDictBaseline[key]
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


TRXFacetFileInput       = 'TRX_TFMSFalcon'
# TRXFacetFileBaseline    = 'TRX_LevelOneOutput_NoSUAs'
# TRXFacetFileComparison  = 'TRX_LevelOneOutput_FalconCapeTraditional'

# TRXDict_Baseline = readTRXIntoDictByTimeFromStart(resultsFolder + TRXFacetFileBaseline)
TRXDict_Input = readTRXIntoDictByTimeFromStart(resultsFolder + TRXFacetFileInput)




fileNameGE = 'testFlightTracks.kml'

flatArray       = []  #lat lon alt vx vy vz lat lon alt vx vy vz lat lon ...
numTimeSteps    = []
callSigns       = []

filterAircraft = []
# filterAircraft = reroutedAcList
# for curSign in sorted(aircraftDictComparison.keys()):
for curSign in sorted(reroutedAcList):
    # curSign = flightRecord[0]
    # dataList = flightRecord[1]
    dataListCompare     = aircraftDictComparison[curSign]
    dataListBaseline    = aircraftDictBaseline[curSign]

    noFilter = (len(filterAircraft) == 0)

    # if curSign == 'AWI377_LNK':
    if noFilter or (curSign in filterAircraft):

        subFlatArray = []
        for entry in dataListBaseline['latLonFL']:
            # Don't care about velocity information here, so just use zeros
            entry[2] = entry[2]*100
            subFlatArray.extend(entry)
            subFlatArray.extend([0,0,0])

        flatArray.extend(subFlatArray)
        numTimeSteps.extend([len(dataListBaseline['latLonFL'])])
        callSigns.append(curSign + "_B")

        subFlatArray = []
        for entry in dataListCompare['latLonFL']:
            # Don't care about velocity information here, so just use zeros
            entry[2] = entry[2]*100
            subFlatArray.extend(entry)
            subFlatArray.extend([0,0,0])

        flatArray.extend(subFlatArray)
        numTimeSteps.extend([len(dataListCompare['latLonFL'])])
        callSigns.append(curSign + "_R")

import sys
# Points to the python scripts needed from Francisco
friscoFiles = '../../../Prop3Dof/FriscoDebris/pythonFiles/'
sys.path.append(friscoFiles)

import data2GE

# data2GE.convertTJC(fileNameGE, flatArray, numTimeSteps, numRuns = len(numTimeSteps), cutoffNAS = False, maxTimeSteps = 1e10)
data2GE.convertTJCAircraft(fileNameGE, flatArray, numTimeSteps, callSigns, numElementsPerLine = 6)

'''
Let's open up the pickle that the TRX file was made from
'''
import pickle
TFMSPickle = pickle.load(open(resultsFolder + 'TFMSFalcon.pkl','rb'))
basicAcRecord = TFMSPickle['basicAcRecord']

# Currently, the keys are unique TFMS IDs, swap em out by prepending the callsign
tfmsIDVec = basicAcRecord.keys()
for tfmsID in tfmsIDVec:
    callSign = basicAcRecord[tfmsID]['callSign']
    basicAcRecord['{0}_{1}'.format(callSign,tfmsID)] = basicAcRecord.pop(tfmsID)

'''
Now let's make a csv file since that's probably easiest for them
'''

comma = ","
colon = ":"
csvFields = ['#CallSign', '#FacetID', '#Distance'   , '#Duration'   , '#DepTime', '#FirstTrackTime'     , '#LastTrackTime'      , '#NominalFlightPlan'  , '#AvoidanceFlightPlan']
csvUnits  = ['#string'  , '#int'    , '#nautMiles'  , '#minutes'    , '#string' , '#MinutesFromMidnight', '#MinutesFromMidnight', '#string'             , '#LatLonPairsForNow']
reroutedFlightsCSVFile = 'rerouted.csv'
output = open(reroutedFlightsCSVFile, 'w')
output.write(comma.join(csvFields) + '\n')
output.write(comma.join(csvUnits) + '\n')

for callSignKey in sorted(reroutedAcList):
    curLine = []
    curAC   = aircraftDictComparison[callSignKey]
    callSign, facetID = callSignKey.split('_')
    firstTime = curAC['timeVec'][0]
    NominalFlightPlan = ""
    depDatetime = ""

    # Have to parse out the avoidancePlan for now
    avoidancePlan = curAC['latLonFL']   # This is a list of length-three lists lat lon FL
    avoidancePlan = ['{0}:{1}:{2}'.format(subList[0], subList[1], subList[2]) for subList in avoidancePlan]
    avoidancePlan = ' x '.join(avoidancePlan)

    # Find the input file entry that corresponds to this flight this leg
    for (curSign, curDict) in basicAcRecord.iteritems():
        if callSign in curSign:
            depDatetime = curDict['depDatetime']
            if int((depDatetime-launchDate).total_seconds()/60.) == firstTime:
                # This is the flight we want, grab the flight plan
                NominalFlightPlan = curDict['flightPlan']
                print "HIT {0} vs {1}".format(callSignKey, curSign)
                break
            else:
                print "Missed {0} vs {1}".format(callSignKey, curSign)

    curLine = [callSign,
               facetID,
               str(curAC['flightDistance']),
               str(curAC['flightTime']),
               str(depDatetime),
               str(curAC['timeVec'][0]),
               str(curAC['timeVec'][-1]),
               NominalFlightPlan,
               avoidancePlan
            ]
    output.write(comma.join(curLine) + '\n')

output.close()


























'''
Graveyad
'''
sys.exit()

LevelZeroSectorMaxOccupancyGraphs       = 'LevelZeroSectorMaxOccupancyGraphs/'
LevelZeroCenterMaxOccupancyGraphs       = 'LevelZeroCenterMaxOccupancyGraphs/'
# Make sure that the directory for holding the graph files exists
folderPath = os.path.abspath(LevelZeroSectorMaxOccupancyGraphs)
if not os.path.exists(folderPath):
    os.makedirs(folderPath)

folderPath = os.path.abspath(LevelZeroCenterMaxOccupancyGraphs)
if not os.path.exists(folderPath):
    os.makedirs(folderPath)
del folderPath      # Just to be safe!

# Read in the raw output from FACET
aircraftDict, sectorDict = readCustomFacetFile(resultsFolder + customFacetFile)

# This whole thing will fail miserably if this isn't true
# If this changes, then will have to move away from using range() as well
deltaT = 1

# Also the time is assumed to start at midnight.
# Aircraft are counted at the precise time of the timestep, it's not a bin.

minTime     = 9e9
maxTime     = -1
maxCount    = -1

maxMaxOccupancy = -1

for curSector in sectorDict.iteritems():
    # iteritems will give me a tuple (dictKey, valueOfDict)
    #   Since i'm using a dict of dicts, valueOfDict will be a dictionary with the information i care about
    #   dictKey will be the name of the sector

    # # Count the number of aircraft present at each timestep
    # curSector[1]['AcCount'] = np.array([len(sublist) for sublist in curSector[1]['ACList']])

    # Make time lists into vectors for easy manipulation.
    curSector[1]['timeList'] = np.array(curSector[1]['timeList'])

    '''
    # Bin into 15-minute intervals that start on the hour
    [0-14,15-29,30-44,45-59]
    '''

    # Find the timeSteps since midnight (as an array)
    timeStepsSinceMidnight = (np.floor(curSector[1]['timeList']/15.)).astype(int)

    # What are the timesteps present?   TODO: Could take care of gaps right here
    # Do I have any promise that these will be in order???
    binnedTimeList  = np.unique(timeStepsSinceMidnight)

    # Total occupancy is number of unique flights in the sector within an interval
    totalOccupancy  = np.zeros_like(binnedTimeList)

    # Max occupancy is the maximum number of simultaneously present flights at any time within the the 15-minute interval
    maxOccupancy    = np.zeros_like(binnedTimeList)

    AcPresentList = []

    # Loop over them
    for IX in range(len(binnedTimeList)):
        curBinnedTimeStep = binnedTimeList[IX]

        # This is an ARRAY of indices indicating which values of ACList belong to this timestep
        curBinnedIX = np.where(timeStepsSinceMidnight == curBinnedTimeStep)[0]

        # This runs through every IX which is included in this timeStep, and runs through every AC within those lists
        #   It puts them all together into a single large list with many duplicate entries
        #   But then turns the list into a set, which keeps only the unique elements
        curAcPresent            = set([thisAc for thisListIX in curBinnedIX for thisAc in curSector[1]['ACList'][thisListIX]])
        totalOccupancy[IX]      = len(curAcPresent)

        # This runs through every IX which is included in this timeStep, gets the list of aircraft present at that IX
        #   and takes its length.  The result will be a list that indicates the number of simultaneously present AC
        #   at every IX that falls within the current (15-minute) timestep.
        numSimultaneousList     = [len(curSector[1]['ACList'][thisListIX]) for thisListIX in curBinnedIX]
        maxOccupancy[IX]        = np.max(numSimultaneousList)

        AcPresentList.append(curAcPresent)


    # Gather some statistics (if we wind up binning times together, this will have to get kicked to after that happens)
    curMinTime      = np.min(binnedTimeList)
    curMaxTime      = np.max(binnedTimeList)

    if curMinTime < minTime:
        minTime = curMinTime

    if curMaxTime > maxTime:
        maxTime = curMaxTime

    if max(maxOccupancy) > maxMaxOccupancy:
        maxMaxOccupancy = max(maxOccupancy)

    # Save the information
    curSector[1]['totalOccupancy']  = totalOccupancy
    curSector[1]['maxOccupancy']    = maxOccupancy
    curSector[1]['binnedTimeList']  = binnedTimeList
    curSector[1]['AcPresentList']   = AcPresentList

    # To reduce confusion, I'm going to delete the elements of the dictionary that are no longer needed
    del curSector[1]['ACList']
    del curSector[1]['timeList']
    # TODO: Oh crap, i need to keep these in order to collect the center-wide maxOccupancy statistics

    # Are there any gaps in the time vectors?
    if sum(np.diff(binnedTimeList) != deltaT):
        # Above expression assumes the timestep is 1 (minute)
        print 'THERE IS A TIME GAP!!!'
        print binnedTimeList
        raise RuntimeError

    # if curSector[0] == 'ZBW85':
    #     print timeStepsSinceMidnight
    #     raise RuntimeError


'''
Now that we've gathered the data by sector, aggregate it into centers
'''


# Initialize the center dictionary
centerDict = dict()

# Find the centers that are present by parsing out the sectors
knownCenters = set([curSector[:3] for curSector in sectorDict.keys()])

# Get the sectors and sort so that we can slice through them
fullSectorList = sorted(sectorDict.keys())

# Now run through each of the centers
for curCenter in knownCenters:
    # Initialize the stuff
    timeList            = []
    maxOccupancyList    = []
    centerDict[curCenter] = dict()

    binnedTimeList  = np.array(range(minTime, maxTime+1))
    maxOccupancy    = np.zeros_like(binnedTimeList)
    totalOccupancy  = np.zeros_like(binnedTimeList)

    # Initialize this list of sets
    AcPresentList       = [set()]*len(binnedTimeList)

    # Run through the sectors and look for members.
    # This is NOT how i wanted to do it, but i couldn't figure out how to do it better
    for curSectorTuple in sectorDict.iteritems():
        if curCenter in curSectorTuple[0]:
            # Being here means that the sector in focus is within the center
            # Make a record of which AC are present

            # By subtracting the minTime, the binnedTimeList becomes a list of time indices for the center binnedTimeList
            curTimeIXList = curSectorTuple[1]['binnedTimeList'] - minTime

            # Run through each current time index and union together the AC names
            for thisIX, thisAcList in zip(curTimeIXList, curSectorTuple[1]['AcPresentList']):
                AcPresentList[thisIX] = AcPresentList[thisIX].union(thisAcList)

    # Now that we have a list of sets, where each set contains the unique names of the AC that were present
    #   we can simply take the lengths of the sets to get the totalOccupancy
    centerDict[curCenter]['totalOccupancy'] = np.array([len(thisSet) for thisSet in AcPresentList])
    centerDict[curCenter]['binnedTimeList'] = binnedTimeList











    # if curCenter == 'ZFW':
    #     raise RuntimeError



'''
Make Sector Plots
'''
# Imports
import matplotlib
# matplotlib.use('Agg')  # Allows plot generation on server without X-windows
import matplotlib.pyplot as plt

fig1 = plt.figure()
for curSector in sorted(sectorDict.keys()):
    curOutputFileName = "{0}_{1}".format(curSector, 'maxOccupancy')

    '''
    Want to set the bounds of the bar box to be consistent for all sectors
    Need to find:
    * The first and last times overall
    * The maximum number of AC at a timestep over all sectors
    '''

    # for plotting purposes
    maxOccupancy    = sectorDict[curSector]['maxOccupancy']
    binnedTimeList  = sectorDict[curSector]['binnedTimeList']
    plt.bar(binnedTimeList, maxOccupancy, alpha=0.75)
    plt.axis([minTime, maxTime+1, 0, maxMaxOccupancy+2])

    plt.title(curOutputFileName)
    plt.xlabel('15-Minute Tsteps Since Midnight')
    plt.ylabel('Count')

    plt.savefig(LevelZeroSectorMaxOccupancyGraphs + curOutputFileName)
    plt.clf()


'''
Make Center Plots
'''

LevelZeroCenterMaxOccupancyGraphs

'''
You know, really, i think this is the one time that a spreadsheet is the best way to go.
MAKE A CSV FILE!!!
'''












# the histogram of the data
# n, bins, patches = plt.hist(x, 50, normed=1, facecolor='green', alpha=0.75)


# plt.xlabel('Smarts')
# plt.ylabel('Probability')
# plt.title(r'$\mathrm{Histogram\ of\ IQ:}\ \mu=100,\ \sigma=15$')
# # plt.axis([40, 160, 0, 0.03])
# plt.grid(True)
#
# plt.show()

















    # # Are there any gaps in the time vectors?
    # if sum(np.diff(curSector[1]['timeList']) != deltaT):
    #     # Above expression assumes the timestep is 1 (minute)
    #     # print 'THERE IS A TIME GAP!!!'
    #     # print curSector[1]['timeList']
    #
    #     # Get the diff vector
    #     curDiff = np.diff(curSector[1]['timeList'])
    #
    #     # Find the locations of the discrepencies
    #     gapIXs = np.where(curDiff != deltaT)[0]
    #
    #     # Go through them in reverse order (so that you don't mess up the gapIX's)
    #     for curGapIX in np.flipud(gapIXs):
    #         numMissing      = curDiff[curGapIX];
    #         lastGoodTime    = curSector[1]['timeList'][curGapIX]
    #         missingTimes    = np.array(range(lastGoodTime + deltaT, lastGoodTime + numMissing))
    #         missingCounts   = np.zeros_like(missingTimes)
    #         # print missingTimes
    #
    #         # Insert them
    #         curSector[1]['timeList']    = np.insert(curSector[1]['timeList'], curGapIX+1, missingTimes)
    #         curSector[1]['AcCount']     = np.insert(curSector[1]['AcCount'], curGapIX+1, missingCounts)
    #
    #     # print curSector[1]['timeList']
    #     # print curSector[1]['AcCount']
    #     # print "\n\n"
    #
    # '''
    # DEBUG CHECK
    # '''
    # # Are there any gaps in the time vectors?
    # if sum(np.diff(curSector[1]['timeList']) != deltaT):
    #     # Above expression assumes the timestep is 1 (minute)
    #     print 'FATAL!!!'
    #     print curSector[1]['timeList']
    #     raise RuntimeError






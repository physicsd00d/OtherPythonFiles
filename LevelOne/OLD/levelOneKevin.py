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





'''
Script
'''
resultsFolder   = 'Results/'
customFacetFileBaseline     = 'Kevin_Custom_Nothing'
customFacetFileComparison   = 'Kevin_Custom_2018Low'
customFacetFilter           = 'Kevin_Filter_2018Low'

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




'''
customFacetFileBaseline     = 'Kevin_Custom_Nothing'
customFacetFileComparison   = 'Kevin_Custom_2018Low'
customFacetFilter           = 'Kevin_Filter_2018Low'
number rerouted          = 93
aggregateDeltaTime       = 127 minutes
aggregateDeltaDistance   = 896.099 naut miles
aggregateDeltaFuel       = 1455.934 lbs
reroutedAcList           = ['AAL1016_27228', 'AAL1285_29154', 'AAL1413_13800', 'AAL1491_24503', 'AAL1520_22956', 'AAL1740_12528', 'AAL1848_24323', 'AAL1887_12864', 'AAL205_8503', 'AAL2167_16511', 'AAL2416_12374', 'AAL2453_28086', 'AAL468_29162', 'AAL903_15268', 'ACA997_10466', 'ASH2836_26540', 'ASQ4616_27593', 'AWE1422_12363', 'AWE158_15917', 'AWE163_24310', 'AWE255_5804', 'AWE302_15293', 'AWE44_15921', 'AWE564_26717', 'AWE57_15923', 'AWE644_29186', 'AWE687_15683', 'AWE81_16031', 'CGAPT_11680', 'DAL1655_9759', 'DAL2013_9764', 'DAL2054_13031', 'DAL837_10487', 'DAL857_6510', 'DAL8949_29232', 'DCM2532_13140', 'EJA290_14651', 'EJA668_17357', 'JBU181_6899', 'JBU585_16963', 'LAK789_15452', 'N12U_26929', 'N18GX_10150', 'N1903G_28525', 'N2121_23911', 'N312NC_22299', 'N378SF_27003', 'N404HR_16267', 'N411AJ_14762', 'N4500X_22347', 'N506KS_13335', 'N65WW_27860', 'N66BS_28697', 'N88QC_11941', 'N92RX_16415', 'N972BR_24792', 'N996AG_28785', 'SKW306M_21300', 'SKW364P_21728', 'SKW4497_26811', 'SKW5610_28211', 'STAVE01_13511', 'SWA1622_28340', 'SWA1814_22093', 'SWA1944_9621', 'SWA1950_4221', 'SWA198_13061', 'SWA210_12102', 'SWA263_28036', 'SWA2870_27305', 'SWA2937_9623', 'SWA347_13620', 'SWA409_9627', 'SWA410_9628', 'SWA481_9632', 'SWA517_7741', 'SWA592_14251', 'SWA712_15799', 'TN715WS_13515', 'TONE39_29475', 'UAL1224_27515', 'UAL1547_28168', 'UAL1589_27768', 'UAL1612_15012', 'UAL1627_27731', 'UAL1695_26788', 'UAL1707_28358', 'UAL284_27413', 'UAL436_28169', 'UAL589_24389', 'UAL594_24907', 'UAL950_13765', 'ZAPER51_12018']
number filtered          = 41
aircraftFilterSet        = set(['N828SK_16391', 'N8841C_28238', 'N399SC_10215', 'N605MJ_30211', 'N787DR_30254', 'AAL1209_12369', 'N554SD_30196', 'CJC4930_27582', 'EJA952_26886', 'TONE92_25676', 'N800JC_17628', 'SWA177_14242', 'TOM126_1168', 'EJA668_17357', 'AAL113_1172', 'ROVE13_30312', 'DBANN_11691', 'AAL173_1553', 'SWA254_26774', 'JBU585_16963', 'N429DM_30960', 'VIR75K_1760', 'N625RL_27059', 'N289HB_22287', 'N2478D_25386', 'EGF2944_28122', 'N519EJ_29788', 'SWA2266_11590', 'XSR290_16486', 'RPA1334_16817', 'SWA209_17651', 'SKW6472_12940', 'N7JW_11918', 'N323RF_29609', 'VRD312_14017', 'BAW207_1954', 'ASQ6170_17543', 'TOM796_1289', 'TN715WS_13515', 'ARG1303_9877', 'UAL1218_24430'])










Kevin_Custom_2025Med
number rerouted          = 1
aggregateDeltaTime       = 0 minutes
aggregateDeltaDistance   = -1.54 naut miles
aggregateDeltaFuel       = -6.97 lbs
['AMX686_13564']


Kevin_Custom_2025High
number rerouted          = 1
aggregateDeltaTime       = 0 minutes
aggregateDeltaDistance   = 0.99 naut miles
aggregateDeltaFuel       = 1.11 lbs
'''


















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








'''
Codes that tell us what the reroute status of the aircraft is
'''
UNCHECKED_AVOIDANCE_RTE = 1
NO_AVOIDANCE_RTE        = 2
CURR_AVOIDANCE_RTE      = 3

'''
Read in my custom FACET output file
'''
def readCustomFacetFile(facetFileName):
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


'''
I don't remember if this is custom to me or not, but whatever, need to read them in.  In this context,
the filter records the aircraft that are found inside the active hazard areas.  If the rerouting algorithm
is acting perfectly, then this file should be empty.  Unfortunately, FACET doesn't seem to know what to do
with aircraft that are scheduled to take-off or land inside an active hazard area...this filter captures
those aircraft so we can handle them in post-processing.
'''
def readFilter(filterName):

    aircraftDict = dict()
    curTime = 0
    inFile = open(filterName, 'r')


    for line in inFile:

        curValues = line.split()

        # Skip empty lines
        if len(line) == 0:
            continue

        # Get the time and then skip ahead
        if curValues[0] == 'TRACK_TIME':
            curTime = int(curValues[1])
            continue

        # Skip everything else that's not a TRACK
        if curValues[0] != 'TRACK':
            continue

        id, callsign = curValues[1:3]

        acKey = "{0}_{1}".format(callsign, id)

        # Keep track of the first and last track times the aircraft was caught in the filter
        if acKey not in aircraftDict:
            aircraftDict[acKey] = [curTime, curTime]
        else:
            aircraftDict[acKey][1] = curTime

    return aircraftDict



# '''
# I don't remember if this is custom to me or not, but whatever, need to read them in.  In this context,
# the filter records the aircraft that are found inside the active hazard areas.  If the rerouting algorithm
# is acting perfectly, then this file should be empty.  Unfortunately, FACET doesn't seem to know what to do
# with aircraft that are scheduled to take-off or land inside an active hazard area...this filter captures
# those aircraft so we can handle them in post-processing.
# '''
# def readFilter(filterName):
#
#     aircraftDict = set()
#     inFile = open(filterName, 'r')
#
#     for line in inFile:
#
#         curValues = line.split()
#
#         # Skip empty lines
#         if len(line) == 0:
#             continue
#
#         # Skip everything that's not a TRACK
#         if curValues[0] != 'TRACK':
#             continue
#
#         id, callsign = curValues[1:3]
#
#         acKey = "{0}_{1}".format(callsign, id)
#
#         if acKey not in aircraftDict:
#             aircraftDict.add(acKey)
#
#     return aircraftDict
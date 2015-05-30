'''
==== This file parses and AirTOp flight plan file (.csv) and turns it into a TRX ===
* Up front you'll find the function defs
* The latter half of the file is a script that uses the functions

Author: Thomas J Colvin
'''
import re
import sys
import numpy as np
from datetime import timedelta
from datetime import datetime

todayYear = 2013
todayMonth = 3
todayDay = 1

launchDateMidnight = datetime(todayYear, todayMonth, todayDay, 0, 0, 0)

# These are the only parameters you need to change for this script to run
# flightPlanFolder = 'AirTOp_Data_Calibration_Model_SpaceX_Launch March 01, 2013/AirTOp_FltPlans_&_Routing_Data/'
flightPlanFolder = 'ResultsForNov13/'
reroutedAircraftFile = 'AIRSPACE.PLANNED_RE_ROUTING.FLIGHTS_RE_ROUTED_AUTOMATICALLY_Nov062014.csv'
endedEndedFile = 'FLIGHT_ENDED_ENDED.csv'
flightPlanCsv = 'FlightPlan.csv'
simulatedTrajectoriesFile = 'SimulatedTrajectories.gfdr'
timeOffset = timedelta(hours=5)

UNCHECKED_AVOIDANCE_RTE = 1
NO_AVOIDANCE_RTE        = 2
CURR_AVOIDANCE_RTE      = 3

kg2lbs = 2.20462
km2nm = 0.539957



def convertTwoElementStringToDate(inStr, char = ' '):
    '''
    :param inStr: a two-element string specifying date, first element is date offset, second is time
    :param char: sometimes they're space-separated and sometimes comma separated.  Default is space
    :return: departureTime + timeOffset
    '''
    # TimeStr = inStr.split()[1]
    # TimeOffset = inStr.split()[0]

    TimeOffset, TimeStr = inStr.split(char)

    # Sometimes TimeOffset has leading zeros.  Convert to int to be safe
    TimeOffset = int(TimeOffset)

    departureTime = datetime.strptime(TimeStr, '%H:%M:%S')  #set the time
    departureTime = departureTime.replace(year=todayYear, month=todayMonth, day=todayDay) #set the date

    if TimeOffset == 1:
        departureTime = departureTime - timedelta(days=1)
    elif TimeOffset == 3:
        departureTime = departureTime + timedelta(days=1)

    return departureTime + timeOffset


def convertNxWxStringToLatLon(inStr):
    LatLon = re.split('N|W',inStr)
    # First element is empty
    return LatLon[1], LatLon[2]



def convertFlightPlan2CustomOutput(inFileName, reroutedList = []):
    # Open the file and get the dict keys
    dictKeys = []
    inputFile = open(inFileName, 'r')

    numInactive = 0
    numActiveWithoutProfile = 0
    numAircraftTotal = 0

    for line in inputFile:
        key = line.split()
        if (key[0] == '#Active'):
            dictKeys = key
            dictKeys[0] = 'Active'  #Manually remove the '#'
            break

        '''Maybe there's a way to set the current date in the comments?'''

    trackTimeRecord = dict()
    uniqueID = -1
    for line in inputFile:
        key = line.split(';')

        # Ignore comments
        if (key[0][0] == '#'):
            continue

        uniqueID = uniqueID + 1
        curAcDict = dict(zip(dictKeys, key))

        # if curAcDict['Aircraft'] == 'AAL1797':
        # if curAcDict['Aircraft'] == 'AAL1815':
        # if curAcDict['Aircraft'] == 'JBU223':
        #     break

        if curAcDict['Aircraft'] == 'AAL648':
            return curAcDict


        # flightPlan = dict()

        # minDepartureTime = datetime.strptime('23:59:59', '%H:%M:%S')


        # # Assemble the dictionary at this non-comment line
        # for ix in range(numKeys):
        #     flightPlan[dictKeys[ix]] = key[ix]
        numAircraftTotal = numAircraftTotal +1


        # Now that the dictionary is populated, gather statistics or whatever
        # Only worry about active aircraft at the moment, because inactive don't have flight profiles
        if (curAcDict['Active'] == 'false'):
            numInactive = numInactive + 1
            continue

        # It appears that even some aircraft lack flight profiles.  Skip those as well
        if (curAcDict['AirspaceProfile'] == ''):
            numActiveWithoutProfile = numActiveWithoutProfile +1
            continue

        # if (flightPlan['FlightStatus'] == 'Terminated'):
        #     print '{0} was TERMINATED'.format(flightPlan['Callsign'])

        if (curAcDict['FlightStatus'] != 'Terminated'):
            print '{0} was {1}'.format(curAcDict['Callsign'], curAcDict['FlightStatus'])

        # Figure out the proper departure time (not worrying about the specific date YET)
        departureTime   = convertTwoElementStringToDate(curAcDict['DepartureTime'])
        # arrivalTime     = convertTwoElementStringToDate(curAcDict['ArrivalTime'])

        # if (departureTime < minDepartureTime):
        #     minDepartureTime = departureTime

        # Parse waypoints for FACET
        wayPoints = curAcDict['WaypointList'].split(',')
        curPlan = wayPoints[0]
        for ix in range(1,len(wayPoints)):
            if wayPoints[ix] is not '':
                curPlan = curPlan + '..' + wayPoints[ix]

        # Prepend / append departure / arrival airports
        Airports = curAcDict['Routing'].split('-')
        curPlan = '{0}..{1}..{2}'.format(Airports[0], curPlan, Airports[1])

        # AirspaceProfile is the thing that needs to be specified in the TRX file
        curProfile = curAcDict['AirspaceProfile']

        # When entering a new center, the slice will be 28 elements long
        #   When staying inside your current center, slice will be 14 elements long
        elementList = np.array(curProfile.split(','))
        elementList = elementList.reshape((len(elementList)/14,14))

        # if curAcDict['Aircraft'] == 'JBU223':
        #     return elementList
        #     break

        acID            = curAcDict['Aircraft']
        acType          = "Unset"
        totalDistance   = curAcDict['TotalDistance'].split('NM')[0]

        # If acID is known to be rerouted, elif acID is definitely known to be not rerouted, else -1
        isRerouted = -1
        if acID in reroutedList:
            isRerouted = CURR_AVOIDANCE_RTE
        elif len(reroutedList) > 0:
            isRerouted = NO_AVOIDANCE_RTE


        counter = 0
        for curElement in elementList:
            curSector = curElement[0]
            # print str(counter) + str(curElement)
            # counter = counter +1

            # This appears to be the only change that concerns me, the sectors are now padded with an extra 0
            if len(curSector) == 6:
                # This means we're looking at an actual sector, not a center.  GOOD!
                # This is good because there are two different types of entries, sector and center
                # The sector entries have the latlon values of the flown aircraft for the given timestep
                # There are two latlon pairs per sector entry, the first and last coords within that sector
                '''If you read the above, you'll notice that means we lose the very last latlon coord in the list'''

                entryTime = convertTwoElementStringToDate(curElement[2])
                minutesSinceMidnight = int(round((entryTime - launchDateMidnight).total_seconds()/60.))

                lat, lon = convertNxWxStringToLatLon(curElement[4])
                altitude = curElement[5].split('ft')[0]
                flightLevel = int(round(float(altitude)/100.))    # There will be some rounding error here
                grndSpd = -1
                vertSpd = -1
                curCenter = curSector[:3]
                heading = '0'
                aircraft = 'B52'
                fuelBrn = curElement[6].split('kg')[0]
                dist = totalDistance

                outputStr = "{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}\t{10}\t{11}\t{12}\t{13}\n".format(
                    minutesSinceMidnight,
                    uniqueID,
                    acID,
                    acType,
                    lat,
                    lon,
                    flightLevel,
                    grndSpd,
                    vertSpd,
                    curCenter,
                    curSector,
                    fuelBrn,
                    dist,
                    isRerouted
                )

                # infoString1 = 'TRACK ' + curAcDict['Callsign'] + ' ' + aircraft + ' ' + Lat + ' ' + \
                #             Lon + ' ' + '1' + ' ' + str(flightLevel) + ' ' + heading + ' ' + curCenter + \
                #             ' ' + curSector
                # infoString2 = '    FP_ROUTE ' + curPlan

                # curDict = {'CallSign': curAcDict['Callsign'],
                #    'Aircraft': curAcDict['Aircraft'],
                #    'infoString2': infoString2,
                #    'infoString1': infoString1}

                # curDict = dict(min)

                # Add the key to the dictionary or append to existing key
                if minutesSinceMidnight not in trackTimeRecord:
                    trackTimeRecord[minutesSinceMidnight] = []
                    trackTimeRecord[minutesSinceMidnight].append(outputStr)
                else:
                    trackTimeRecord[minutesSinceMidnight].append(outputStr)
            #
            # elif len(curSector) != 3:
            #     # print 'curSector = {0}'.format(curSector)
            #     1


    # sortedKeys = sorted(trackTimeRecord.keys())
    # for curTime in sortedKeys:
    #     curDict = trackTimeRecord[curTime]
    #     TRACK_TIME = int((curTime-refDate).total_seconds())
    #     outFile.write('TRACK_TIME ' + str(TRACK_TIME) + '\n')
    #
    #     for flight in curDict:
    #         outFile.write(flight['infoString1'] + '\n')
    #         outFile.write(flight['infoString2'] + '\n\n')
    #
    #     # outFile.write('TRACK ' + flightPlan['Callsign'] + ' ' + flightPlan['Aircraft']
    #     #               + ' ' + 'Lat    Lon    \n'  )
    #     #
    #     # outFile.write('    FLIGHTPLAN\n\n')

    print 'numInactive              = {0}'.format(numInactive)
    print 'numActiveWithoutProfile  = {0}'.format(numActiveWithoutProfile)
    print 'numAircraftTotal         = {0}'.format(numAircraftTotal)

    return trackTimeRecord



def findReroutedAircraft(filename):
    inputFile = open(filename, 'r')
    reroutedList = []
    for line in inputFile:
        keys = line.split(";")
        if (len(keys) > 0) and keys[0] == "Total":
            # First key is word, next key is number of AC, followed by csv of ACids
            acHere = keys[2].split(", ")
            reroutedList.extend(acHere)

    return reroutedList


def readEndedEnded(filename):
    inputFile = open(filename, 'r')

    dictKeys = []
    # First get the diciontary keys
    for line in inputFile:
        element = line.split()
        if element[0] == '#ID':
            dictKeys = element[1:]
            break


    # Now load the data
    storageDict = dict()
    for line in inputFile:
        element = line.split(';')

        if element[0] == 'OPCE#1':
            tempDict = dict(zip(dictKeys, element[1:]))

            acID            = tempDict['Aircraft']
            dist_nm         = float(tempDict['TotalDistanceFlown'].split('m')[0]) * km2nm/1000.
            duration        = tempDict['TotalFlightDuration']
            fuelBurn_lbs    = float(tempDict['TotalFuelBurned'].split('kg')[0]) * kg2lbs
            storageDict[acID] = dict(dist_nm=dist_nm, duration=duration, fuelBurn_lbs=fuelBurn_lbs)

    return storageDict



def convertSimulatedTrajectories2CustomOutput(inFileName, reroutedList = [], endedEndedDict = []):
    '''
    Format for a single AC at a single timestep looks like this
    01,19:01:00 tvalt   SWA1614 B737    1   0   EN_ROUTE    0   0
    01,19:01:00 tvhdg   SWA1614 B737    1   0   EN_ROUTE    0   272.7432
    01,19:01:00 latvlong    SWA1614 B737    1   0   EN_ROUTE    -80.152747  26.072583
    01,19:01:00 tvgs    SWA1614 B737    1   0   EN_ROUTE    0   153.5
    '''

    # Open the file and get the dict keys
    inputFile = open(inFileName, 'r')

    curAltFt    = 'ERROR'
    curLonDegE  = 'ERROR'
    curLatDegN  = 'ERROR'

    uniqueID = 0    # Not used here

    trackTimeRecord = dict()
    for line in inputFile:
        # Skip comments (I manually added the comments myself!)
        if line[0] == '#':
            continue

        elem = line.split()

        curKey = elem[1]
        if curKey == 'tvalt':
            curAltFt = elem[-1]
        elif curKey == 'tvhdg':
            None    # Get heading eventually if we care
        elif curKey == 'latvlong':
            curLonDegE = elem[-2]
            curLatDegN = elem[-1]
        elif curKey == 'tvgs':
            None    # Get groundspeed eventually if we care

            acID            = elem[2]
            acType          = elem[3]
            # By virtue of making it here, it's time to store this track
            entryTime = convertTwoElementStringToDate(elem[0],',')
            minutesSinceMidnight = int(round((entryTime - launchDateMidnight).total_seconds()/60.))

            # If acID is known to be rerouted, elif acID is definitely known to be not rerouted, else -1
            isRerouted = -1
            if acID in reroutedList:
                isRerouted = CURR_AVOIDANCE_RTE
            elif len(reroutedList) > 0:
                isRerouted = NO_AVOIDANCE_RTE

            # If we know the final values for some metrics, just put them in there for all times
            #             storageDict[acID] = dict(dist_nm=dist_nm, duration=duration, fuelBurn_lbs=fuelBurn_lbs)

            fuelBrn = '-1'
            dist = '-1'
            if acID in endedEndedDict:
                curDict = endedEndedDict[acID]
                fuelBrn     = curDict['fuelBurn_lbs']
                dist        = curDict['dist_nm']
            elif len(endedEndedDict) > 0:
                print "ERROR: {0} was not found in endedEndedDict.  Exiting so you can investigate...".format(acID)

            lat = curLatDegN
            lon = curLonDegE
            flightLevel = int(round(float(curAltFt)/100.))    # There will be some rounding error here
            grndSpd = -1
            vertSpd = -1
            curCenter = 'Unset'
            curSector = 'Unset'
            heading = '0'

            outputStr = "{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}\t{10}\t{11}\t{12}\t{13}\n".format(
                minutesSinceMidnight,
                uniqueID,
                acID,
                acType,
                lat,
                lon,
                flightLevel,
                grndSpd,
                vertSpd,
                curCenter,
                curSector,
                fuelBrn,
                dist,
                isRerouted
            )

            # Add the key to the dictionary or append to existing key
            if minutesSinceMidnight not in trackTimeRecord:
                trackTimeRecord[minutesSinceMidnight] = []
                trackTimeRecord[minutesSinceMidnight].append(outputStr)
            else:
                trackTimeRecord[minutesSinceMidnight].append(outputStr)

            # Reset the persistent values
            curAltFt    = 'ERROR'
            curLonDegE  = 'ERROR'
            curLatDegN  = 'ERROR'

        else:
            print "Error: You should not have made it here.  Exiting..."
            sys.exit()

    # numInactive = 0
    # numActiveWithoutProfile = 0
    # numAircraftTotal = 0
    return trackTimeRecord




'''
Script
'''

#
# endedEndedDict = readEndedEnded(flightPlanFolder + endedEndedFile)
# reroutedList = findReroutedAircraft(flightPlanFolder + reroutedAircraftFile)
#
# trackTimeRecord = convertSimulatedTrajectories2CustomOutput("/Volumes/Storage/Sandbox/" + simulatedTrajectoriesFile,
#                                                             reroutedList, endedEndedDict)
#
#
# customOutputFile = "LevelOne_FromAirtop"
# # trackTimeRecord = convertFlightPlan2CustomOutput(flightPlanFolder + flightPlanCsv, reroutedList)
#
# output = open(customOutputFile, 'w')
#
# # Take care of the preamble
# preamble1 = "#TJC Generated Output from Airtop\n"
# preamble2 = "@time   intID   acID    type    lat     lon     alt     grndSpd vertSpd center  sector  fuelBrn dist    isRerouted\n"
# preamble3 = "#min    _____   ____    ____    deg     deg     FL      knots   knots   ______  ______  lbs.    n.m.    ____\n"
#
# output.write(preamble1)
# output.write(preamble2)
# output.write(preamble3)
#
# for curTime in sorted(trackTimeRecord.keys()):
#     curRecord = trackTimeRecord[curTime]
#     for curLine in curRecord:
#         output.write(curLine)
# output.close()
# #
# #
# # # SWA1890
# # # 3382.43kg
# # # 1810360m


curACDict = convertFlightPlan2CustomOutput(flightPlanFolder + flightPlanCsv)



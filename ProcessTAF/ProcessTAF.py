'''
==== This file parses a Terminal Area Forecase file (.csv) and turns it into a TRX ===
* Up front you'll find the function defs
* The latter half of the file is a script that uses the functions

Author: Thomas J Colvin
'''
import sys
from datetime import datetime
from datetime import timedelta
import numpy as np
import re


# These are the only parameters you need to change for this script to run
flightPlanFolder = 'Forecast_AirTraffic_2018_2025/'


# flightPlanCsv = 'abridgedFlightPlan.csv'
flightPlanCsv = 'OUT_constrained_schedules_20120504_2018.csv'
midnight = datetime(2012, 5, 4, 0, 1, 0)


outputFolder = 'OutputFiles/'
# outputFolder = '/Volumes/Storage/OldDocuments/Research/FACE2/Sandbox/'



# TrxName = 'TRX_Falcon9_March_1_2013_Airtop'
TrxName = 'TRX_TAF_PlannedTest'




# =========== Function Definitions ==============


# Some global variables
# todaysDate = datetime(2013,3,1)         # BE SURE TO SET THIS!!!
refDate = datetime(1970,1,1,0,0,0)      #FACET refDate is refDate = datetime(1970,1,1,0,0,0)


def CSVtoTRX(inFileName, outFileName):

    numInactive = 0
    numActiveWithoutProfile = 0
    numAircraftTotal = 0

    # date_object = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')

    # Open the file and get the dict keys
    try:
        outFile = open(outFileName,'w')
        
        inputFile = open(inFileName, 'r')
    
        for line in inputFile:
            key = re.split(',|\n', line)    #Using re to catch the \n
            # key = line.split(',')

            if (key[0] == '#ID_NUM'):
                dictKeys = key[:-1] #keep all but last one which is known to be empty due to '\n'
                dictKeys[0] = 'ID_NUM'  #Manually remove the '#'
                break
    except:
        print 'file(s) failed to open'
        
    print dictKeys
    numKeys = len(dictKeys)


    trackTimeRecord = dict()
                
    try:
        
        # minDepartureTime = datetime.strptime('23:59:59', '%H:%M:%S')

        
        for line in inputFile:
            # For every line, make a flightPlan dictionary


            # if numAircraftTotal > 100:
            #     print '\n\nFor debugging purposes, we are breaking right here'
            #     break

            flightPlan = dict()

            key = line.split(',')

            
            # Ignore comments
            if (key[0][0] == '#'):
                print 'COMMENT'
                continue

            # Assemble the dictionary at this non-comment line
            for ix in range(numKeys):
                flightPlan[dictKeys[ix]] = key[ix]
            numAircraftTotal = numAircraftTotal +1

            if flightPlan['FLIGHT_PLAN_TYPE'] == 'VFR':
                # Skip VFR for now, only do IFR
                continue

            print flightPlan['ACID']
            # ### DEBUGGING
            # if(flightPlan['ACID'] != 'DAL269'):
            #     # return curDict
            #     continue
            # ### DEBUGGING
            # if(flightPlan['ACID'] == 'DAL269'):
            #     return flightPlan


            # Figure out the proper departure time (not worrying about the specific date YET)
            departureTime   = convertTwoElementStringToDate(flightPlan['OUT_TIME'])
            arrivalTime     = convertTwoElementStringToDate(flightPlan['IN_TIME'])

#             if (departureTime < minDepartureTime):
#                 minDepartureTime = departureTime
#
            # Parse waypoints for FACET
            # wayPoints = flightPlan['WAYPOINTS'].split(' ')
            wayPoints = re.split(' |\n', flightPlan['WAYPOINTS'])
            curPlan = wayPoints[0]
            for ix in range(1,len(wayPoints)):
                if wayPoints[ix] is not '':
                    curPlan = curPlan + '..' + wayPoints[ix]

            # Prepend / append departure / arrival airports
            departureAirportICAO    = flightPlan['DEPT_ICAO_CODE']
            arrivalAirportICAO      = flightPlan['ARR_ICAO_CODE']
            curPlan = '{0}..{1}..{2}'.format(departureAirportICAO, curPlan, arrivalAirportICAO)

            entryTime           = departureTime
            callSign            = flightPlan['ACID']
            aircraft            = flightPlan['ETMS_AIRCRAFT_TYPE']
            # Lat, Lon            = convertDecimalStringToDegMinSecString([flightPlan['DEPT_LAT'], flightPlan['DEPT_LON']])
            Lat, Lon            = "000", "000"  # Must be exactly three zeros for a planned flight
            filedFlightLevel    = str(int(float(flightPlan['FILED_ALTITUDE'])))
            # filedAirSpeed       = str(int(float(flightPlan['FILED_AIRSPEED'])))
            heading     = '0'     # Unknown
            curSector   = "NONE"    # Unknown
            curCenter   = "NONE"    # Can't be blank!

            groundSpd   = "1"       # The true speed will get set by the aircraft performance model.  DON'T SET IT TO ZERO!!!
            trackFL     = "1"       # Similarly, don't set this to zero either otherwise the flight will get killed.


            infoString1 = 'TRACK ' + callSign + ' ' + aircraft + ' ' + Lat + ' ' + \
                        Lon + ' ' + groundSpd + ' ' + trackFL + ' ' + heading + ' ' + curCenter + \
                        ' ' + curSector + ' ' + filedFlightLevel
            infoString2 = '    FP_ROUTE ' + curPlan

            curDict = {'CallSign': callSign,
               'Aircraft': aircraft,
               'infoString2': infoString2,
               'infoString1': infoString1}


            # Add the key to the dictionary or append to existing key
            if entryTime not in trackTimeRecord:
                trackTimeRecord[entryTime] = []
                trackTimeRecord[entryTime].append(curDict)
            else:
                trackTimeRecord[entryTime].append(curDict)


        sortedKeys = sorted(trackTimeRecord.keys())
        for curTime in sortedKeys:
            if curTime <= midnight:
                # Ignore tracks that happen before the date of interest
                continue

            curDict = trackTimeRecord[curTime]
            TRACK_TIME = int((curTime-refDate).total_seconds())
            outFile.write('TRACK_TIME ' + str(TRACK_TIME) + '\n')

            for flight in curDict:
                outFile.write(flight['infoString1'] + '\n')
                outFile.write(flight['infoString2'] + '\n\n')






    except:
        print "Unexpected error:", sys.exc_info()
        import traceback
        traceback.print_tb(sys.exc_traceback)
        print line
#
# # Now write everything to file
# #        try:
# #            outFile = open(outFileName,'w')
# #            for ix in range(len(timeStorage)):
# #                outFile.write(timeStorage[ix])
# #                for ac in range(len(aircraftAtTimeStorage[ix])):
# #                    outFile.write(line1AtTimeStorage[ix][ac])
# #                    outFile.write(line2AtTimeStorage[ix][ac])
# #                    outFile.write('\n')
#
#
#     print 'numInactive = ' + str(numInactive)
#     print 'numActiveWithoutProfile = ' + str(numActiveWithoutProfile)
#     print 'numAircraftTotal = ' + str(numAircraftTotal)
#
#     # return trackTimeRecord
#     return flightPlan


def convertTwoElementStringToDate(inStr):
    # Split the two elements
    DateStr = inStr.split()[0]
    TimeStr = inStr.split()[1]

    # Parse out the date
    todayYear   = int(DateStr[0:4])
    todayMonth  = int(DateStr[4:6])
    todayDay    = int(DateStr[6:8])

    # Build up the datetime object
    departureTime = datetime.strptime(TimeStr, '%H:%M:%S')  #set the time
    departureTime = departureTime.replace(year=todayYear, month=todayMonth, day=todayDay) #set the date

    return departureTime

def convertDecimalStringToDegMinSecString(LatLonStr):
    curLat, curLon = LatLonStr

    if float(curLat) < 0:
        print "ERROR: CANNOT HAVE NEGATIVE LATITIUDE\n"
        sys.exit()
    elif float(curLon) > 0:
        print "ERROR: CANNOT HAVE POSITIVE LONGITUDE\n"
        sys.exit()

    # Do the Latitude first
    val             = abs(float(curLat))
    degreesInt      = int(np.floor(val))
    minutesFloat    = (val - degreesInt)*60
    minutesInt      = int(np.floor(minutesFloat))
    secondsInt      = int(np.floor((minutesFloat - minutesInt)*60.))
    LatDDMMSS       = '{0}{1}{2}N'.format(degreesInt, minutesInt, secondsInt)

    # Do the Longitude first
    val             = abs(float(curLon))
    degreesInt      = int(np.floor(val))
    minutesFloat    = (val - degreesInt)*60
    minutesInt      = int(np.floor(minutesFloat))
    secondsInt      = int(np.floor((minutesFloat - minutesInt)*60.))
    LonDDMMSS       = '{0}{1}{2}W'.format(degreesInt, minutesInt, secondsInt)

    return [LatDDMMSS, LonDDMMSS]






# =========== Run the script ==============
flightDict = CSVtoTRX(flightPlanFolder + flightPlanCsv, outputFolder + TrxName)




    #
    # Callsign    = curFlight['callSign']
    # ACtype      = curFlight['acType']
    # # curCenter   = curFlight['depCenter']
    # filedFL     = curFlight['filedFL'][curIX]        # Taking very first FL for now
    #
    # curPlan = 'ERROR'
    # if useField10:
    #     curPlan = curFlight['flightPlan'][curIX]    # Taking very first flight plan for now
    # else:
    #     curPlan = curFlight['allFixes'][curIX]    # Taking very first flight plan for now
    #
    #
    #
    # # (trackTime, lat, lon, groundSpd, trackFL) = curFlight['trackVec']
    # heading     = '0'     # Unknown
    # curSector   = "NONE"    # Unknown
    # curCenter   = "NONE"    # Can't be blank!
    #
    # #'''Dont use track time because that's not what tech center uses!!!'''
    # # trackTime = curFlight['depDatetime']      # Tech center uses first time
    # # trackTime = max(curFlight['depDatetime'])   # Best to use the true take-off time though
    #
    # # # Update lat lon to be in HMS format
    # # lat = convertDegreesToDegMinSec(lat)
    # # lon = convertDegreesToDegMinSec(abs(lon))   # Facet assumes positive = west
    # #
    # # latStr = '{0:02}{1:02}{2:02}'.format(lat[0], lat[1], lat[2])
    # # lonStr = '{0:02}{1:02}{2:02}'.format(lon[0], lon[1], lon[2])
    #
    # # I hacked FACET, so if you want to set a flight to be scheduled for takeoff, then do this
    # latStr      = "000"     # Must be exactly three zeros!
    # lonStr      = "000"
    # groundSpd   = "1"       # The true speed will get set by the aircraft performance model.  DON'T SET IT TO ZERO!!!
    # trackFL     = "1"       # Similarly, don't set this to zero either otherwise the flight will get killed.
    #
    # infoString1 = 'TRACK ' + Callsign + ' ' + ACtype + ' ' + latStr + ' ' + \
    #         lonStr + ' ' + groundSpd + ' ' + trackFL + ' ' + heading + ' ' + curCenter + \
    #         ' ' + curSector + ' ' + filedFL
    # infoString2 = '    FP_ROUTE ' + curPlan
    #
    # # Package it up
    # curDict = {'CallSign': Callsign,
    #    'Aircraft': ACtype,
    #    'infoString2': infoString2,
    #    'infoString1': infoString1}
    #
    # # Save it
    # if trackTime not in trackTimeRecord:
    #     trackTimeRecord[trackTime] = []
    # trackTimeRecord[trackTime].append(curDict)

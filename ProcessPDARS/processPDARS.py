'''
==== This file parses PDARS data (.csv) and turns it into a TRX ===
* Up front you'll find the function defs
* The latter half of the file is a script that uses the functions

Record Type 2


Author: Thomas J Colvin
'''

# These are the only parameters you need to change for this script to run
# flightPlanFolder = 'AirTOp_Data_Calibration_Model_SpaceX_Launch March 01, 2013/AirTOp_FltPlans_&_Routing_Data/'
dataFolder = 'InputsFiles/'
dataFile = 'IFF_ZMA_03012013.csv'

outputFolder = 'OutputFiles/'
# outputFolder = '/Volumes/Storage/OldDocuments/Research/FACE2/Sandbox/'

TrxName = 'TRX_PDARS'
todayYear = 2013
todayMonth = 3
todayDay = 1



# =========== Function Definitions ==============
import sys
from datetime import datetime
from datetime import timedelta
import numpy as np
import re

# Some global variables
todaysDate = datetime(2013,3,1)         # BE SURE TO SET THIS!!!
refDate = datetime(1970,1,1,0,0,0)      #FACET refDate is refDate = datetime(1970,1,1,0,0,0)


def PDARStoTRX(inFileName, outFileName):

    numInactive = 0
    numActiveWithoutProfile = 0
    numAircraftTotal = 0

    # date_object = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')

    # Open the file and get the dict keys
    try:
        # outFile = open(outFileName,'w')

        inputFile = open(inFileName, 'r')

        # There appears to be 6 different types of data lines (0-5)
        # We only care about 2, 3, and 4

        for line in inputFile:
            key = line.split(',')

            if (key[0] == '2'):
                dictKeys = key
                dictKeys[0] = 'Active'  #Manually remove the '#'
                break
    except:
        print 'file(s) failed to open'

    print dictKeys
    numKeys = len(dictKeys)

    trackTimeRecord = dict()



# =========== Run the script ==============
# flightPlan = PDARStoTRX(dataFolder + dataFile, outputFolder + TrxName)

offsetSeconds = int((todaysDate-refDate).total_seconds())
# TRACK_TIME = int((curTime-refDate).total_seconds())

'''
#
# SWA2427
#
'''
# FIRST INSTANCE OF SWA2427 in ZMA file
print 'FIRST INSTANCE OF SWA2427 in ZMA file'
curTimeSecFILED = 1362136521    #Also from PDARS
curTimeSecPDARS = 1362140137    #First track point
curTimeSecAirTp = 1362099124    #First track point
curTimeSecFACET = 1362140151    #First track point

curDeltaFILED = timedelta(seconds=(curTimeSecFILED - offsetSeconds))
curDeltaPDARS = timedelta(seconds=(curTimeSecPDARS - offsetSeconds))
curDeltaAirTp = timedelta(seconds=(curTimeSecAirTp - offsetSeconds))
curDeltaFACET = timedelta(seconds=(curTimeSecFACET - offsetSeconds))

print 'FILED {0}'.format(todaysDate + curDeltaFILED)
print 'PDARS {0}'.format(todaysDate + curDeltaPDARS)
print 'AirTp {0}'.format(todaysDate + curDeltaAirTp)
print 'FACET {0}'.format(todaysDate + curDeltaFACET)

# SECOND INSTANCE in ZMA file
print '\nSECOND INSTANCE in ZMA file'
curTimeSecPDARS = 1362140713    #First track point AND filed
curDeltaPDARS = timedelta(seconds=(curTimeSecPDARS - offsetSeconds))
print 'PDARS {0}'.format(todaysDate + curDeltaPDARS)

# Only INSTANCE in ZJX file
print '\nOnly INSTANCE in ZJX file'
curTimeSecFILED = 1362120260    #Filed
curTimeSecPDARS = 1362139941    #First track point
curDeltaFILED = timedelta(seconds=(curTimeSecFILED - offsetSeconds))
curDeltaPDARS = timedelta(seconds=(curTimeSecPDARS - offsetSeconds))
print 'FILED {0}'.format(todaysDate + curDeltaFILED)
print 'PDARS {0}'.format(todaysDate + curDeltaPDARS)

# Only INSTANCE in MERGED file
print '\nOnly INSTANCE in MERGED file'
curTimeSecFILED = 1362120260    #Filed
curTimeSecPDARS = 1362139941    #First track point
curDeltaFILED = timedelta(seconds=(curTimeSecFILED - offsetSeconds))
curDeltaPDARS = timedelta(seconds=(curTimeSecPDARS - offsetSeconds))
print 'FILED {0}'.format(todaysDate + curDeltaFILED)
print 'PDARS {0}'.format(todaysDate + curDeltaPDARS)




'''
#
# UPS352
#
'''
# FIRST INSTANCE OF UPS352 in ZMA file
print '\n\nFIRST INSTANCE OF UPS352 in ZMA file'
curTimeSecFILED = 1362103769    #Also from PDARS
curTimeSecPDARS = 1362112705    #First track point
curTimeSecAirTp = 1362082672    #First track point
curTimeSecFACET = 1362112975    #First track point

# curTimeLastPDAR = 1362141109    #Last track point (ACTUALLY 33274) ETA 1418
curTimeLastPDAR = 1362114337    #Last track point (ACTUALLY 33274) ETA 1418
# 1362145093  # Last 33274 track


curDeltaFILED = timedelta(seconds=(curTimeSecFILED - offsetSeconds))
curDeltaPDARS = timedelta(seconds=(curTimeSecPDARS - offsetSeconds))
curDeltaAirTp = timedelta(seconds=(curTimeSecAirTp - offsetSeconds))
curDeltaFACET = timedelta(seconds=(curTimeSecFACET - offsetSeconds))
curDeltaLastPDAR = timedelta(seconds=(curTimeLastPDAR - offsetSeconds))

print 'FILED {0}'.format(todaysDate + curDeltaFILED)
print 'PDARS {0}'.format(todaysDate + curDeltaPDARS)
print 'AirTp {0}'.format(todaysDate + curDeltaAirTp)
print 'FACET {0}'.format(todaysDate + curDeltaFACET)
print 'LASTP {0}'.format(todaysDate + curDeltaLastPDAR)

# # SECOND INSTANCE in ZMA file
# print '\nSECOND INSTANCE in ZMA file'
# curTimeSecPDARS = 1362140713    #First track point AND filed
# curDeltaPDARS = timedelta(seconds=(curTimeSecPDARS - offsetSeconds))
# print 'PDARS {0}'.format(todaysDate + curDeltaPDARS)
#
# # Only INSTANCE in ZJX file
# print '\nOnly INSTANCE in ZJX file'
# curTimeSecFILED = 1362120260    #Filed
# curTimeSecPDARS = 1362139941    #First track point
# curDeltaFILED = timedelta(seconds=(curTimeSecFILED - offsetSeconds))
# curDeltaPDARS = timedelta(seconds=(curTimeSecPDARS - offsetSeconds))
# print 'FILED {0}'.format(todaysDate + curDeltaFILED)
# print 'PDARS {0}'.format(todaysDate + curDeltaPDARS)
#
# # Only INSTANCE in MERGED file
# print '\nOnly INSTANCE in MERGED file'
# curTimeSecFILED = 1362120260    #Filed
# curTimeSecPDARS = 1362139941    #First track point
# curDeltaFILED = timedelta(seconds=(curTimeSecFILED - offsetSeconds))
# curDeltaPDARS = timedelta(seconds=(curTimeSecPDARS - offsetSeconds))
# print 'FILED {0}'.format(todaysDate + curDeltaFILED)
# print 'PDARS {0}'.format(todaysDate + curDeltaPDARS)




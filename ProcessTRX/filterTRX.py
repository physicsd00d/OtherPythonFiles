#!/usr/bin/python

import sys
import os.path

print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)

if len(sys.argv) != 4:
    print "   Error: need exactly three arguments after file name"
    print "          fileToFilterOn fileToPrune outputFile"
    sys.exit()

# Unpack inputs
fileToFilterOn  = sys.argv[1]
fileToPrune     = sys.argv[2]
outputFile      = sys.argv[3]

# Check that inputs exist
if not os.path.isfile(fileToFilterOn):
    print "   Error: {0} does not exist".format(fileToFilterOn)
    sys.exit()
elif not os.path.isfile(fileToPrune):
    print "   Error: {0} does not exist".format(fileToPrune)
    sys.exit()


from TRX_functions import readTRXIntoDictByCallsign
from TRX_functions import pruneTRXFromList

# fileToFilterOn  = 'TRX_Files/CapeShapeFilteredAC02'
# fileToPrune     = 'TRX_Files/TRX_20050824_FastForward_OnTheMinute'
# outputFile      = 'TRX_20050824_FastForward_OnTheMinute_Filtered'

# fileToFilterOn  = 'Kevin2018/ColoradoAircraftFilter'
# fileToPrune     = 'Kevin2018/TRX_TAF_PlannedTestFull'
# outputFile      = 'TempTRX'

# Just load the entire TRX, since it's been filtered, it should be relatively small
TRX_Storage = readTRXIntoDictByCallsign(fileToFilterOn)

# All the keys are the flights you want.  The dep airport is appended to each for (quasi) uniqueness; remove that
# First just whittle it down to only the flights you want
sortedKeys      = sorted(TRX_Storage.keys())
flightsToKeep   = [curFlight.split('_')[0] for curFlight in sortedKeys]
filterDepAirports   = False
filterTimes         = False
bigFilterKeys       = []
filterDict = {'callsigns' : flightsToKeep, 'sectorNames' : [], 'filterDepAirports' : filterDepAirports,
              'filterTimes' : filterTimes, 'bigFilterKeys' : bigFilterKeys}
pruneTRXFromList(fileToPrune, filterDict, outputFile)


sys.exit()


'''
# Now that you've eliminated all the extra flights, make sure things are clean by
#   * Pruning based on departure airport
#   * Only keeping the first track time (same as removing updates)
'''

fileToPrune     = 'TempTRX'
outputFile      = 'TRX_TAF_PlannedTestFull_Colorado'
TRX_Storage = readTRXIntoDictByCallsign(fileToPrune)

sortedKeys      = sorted(TRX_Storage.keys())
flightsToKeep   = [curFlight.split('_')[0] for curFlight in sortedKeys]
depAirports     = [curFlight.split('_')[1] for curFlight in sortedKeys]
firstTimes      = [TRX_Storage[curFlight][0][0] for curFlight in sortedKeys]

filterDepAirports   = True
filterTimes         = True
bigFilterKeys = ['{0}_{1}_{2}'.format(callsign, dep, time) for (callsign, dep, time) in zip(flightsToKeep, depAirports, firstTimes)]

### Now filter the main TRX using flightsToKeep
# First package the info up so we can jam it into an existing function
filterDict = {'callsigns' : flightsToKeep, 'sectorNames' : [], 'filterDepAirports' : filterDepAirports,
              'filterTimes' : filterTimes, 'bigFilterKeys' : bigFilterKeys}
pruneTRXFromList(fileToPrune, filterDict, outputFile)

# key = pruneTRXFromList(fileToPrune, filterDict, outputFile)

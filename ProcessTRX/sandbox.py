import numpy as np
# from TRX_functions import readTRXIntoDictByCallsign
import glob

import time

class Timer(object):
    def __init__(self, verbose=False):
        self.verbose = verbose

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()
        self.secs = self.end - self.start
        self.msecs = self.secs * 1000  # millisecs
        if self.verbose:
            print 'elapsed time: %f ms' % self.msecs


# Possibly slightly faster, FILTERS ARE NOW ORGANIZED BY TIME!!!
def pruneTRXFromList_V2(inFileName, filterDict, outFileName, deltaSeconds = 0):
    # Starts by eliminating every single aircraft (shouldPrint = False), but if an AC matches a filter,
    #   then it will be allowed through.

    #print 'Pruning for ' + str(outFileName)
    # sortedKeys = sorted(filterDict.keys())
    # plainCallsigns = [curFlight.split('_')[0] for curFlight in sortedKeys]


    # Keys are TRACK_TIMES, each value will be the strings (concatenated together) that are to be printed out
    TRX_Storage = dict()

    printOkay = True
    if not printOkay:
        print "PRINTING TURNED OFF!!!\n"

    if len(outFileName) == 0:
        printOkay = False

    try:
        inputFile = open(inFileName, 'r')

        # This will hold the information as we run through the lines until it's time to save it to the dictionary
        curTime = -1
        curFPLine = ''
        curTrackLine = ''
        shouldPrint = True
        curCallSign = []    # Scope this here

        for line in inputFile:
            key = line.split()

            if len(key) > 0:
                if key[0] == 'TRACK_TIME':
                    # Indicates progress
                    curTime = str(int(key[1]) + deltaSeconds)
                    curTimeInt = int(key[1]) + deltaSeconds

                elif key[0] == 'TRACK':
                    curCallSign = key[1]

                    # shouldPrint = (curCallSign in plainCallsigns)
                    curTrackLine = line

                elif key[0] == 'FP_ROUTE':
                    curFPLine = line

                    # At this point we need to check for the departure Airport
                    # if shouldPrint:

                    # Reset
                    shouldPrint = filterDict.has_key(curTimeInt)
                    if shouldPrint:
                        subFilter = filterDict.get(curTimeInt)
                        depAirport = key[1].split('.')[0]
                        sign_dep = "{0}_{1}".format(curCallSign, depAirport)
                        if sign_dep not in subFilter:
                            shouldPrint = False


#                     subFilter = filterDict.get(curTimeInt, False)
#                     if subFilter:
#                         depAirport = key[1].split('.')[0]
#                         sign_dep = "{0}_{1}".format(curCallSign, depAirport)
#                         if sign_dep not in subFilter:
#                             shouldPrint = False


                    # if sign_dep not in sortedKeys:
                    #     shouldPrint = False
                    # elif curTimeInt not in filterDict[sign_dep]:
                    #     shouldPrint = False


                    # At this point, we will be done with the specific aircraft that we're looking at so save it if it's good
                    if shouldPrint:
                        # Create this time record if necessary
                        if not TRX_Storage.has_key(curTime):
                            TRX_Storage[curTime] = ''

                        # Add it to the queue for printing
                        TRX_Storage[curTime] = TRX_Storage[curTime] + curTrackLine
                        TRX_Storage[curTime] = TRX_Storage[curTime] + curFPLine + '\n'

                elif key[0][0] == '#':
                    # print 'COMMENT'
                    1

                else:
                    print "pruneTRXFromList: NewLine! This should not have been hit!"
                    print key

        inputFile.close() # It's likely that the output file will be the same file, so make sure to close this first.

    except:
        print "pruneTRXFromList: FAILURE in reading the file"
        printOkay = 0
        raise


    if printOkay:
        # # Now write everything to file
        # try:
        outFile = open(outFileName,'w')

        for key in sorted(TRX_Storage.iterkeys()):
            if len(TRX_Storage[key]) > 0:
                outFile.write('TRACK_TIME ' + key + '\n')
                outFile.write(TRX_Storage[key])

        outFile.close()
        # except:
        #     print "FAIL
    return TRX_Storage


###
# Pull out all of the callsign_dep combos from a TRX filter file and the associated times
###
def readTRXIntoDictByCallsign(inFileName):
#     callSign_set = set()
    TRX_Storage = dict()
    try:
        inputFile = open(inFileName, 'r')

        # This will hold the information as we run through the lines until it's time to save it to the dictionary
        curTime = -1
        curFPLine = ''
        curTrackLine = ''
        # shouldPrint = False

        for line in inputFile:
            key = line.split()

            if len(key) > 0:
                if key[0] == 'TRACK_TIME':
                    # Indicates progress
                    curTime = int(key[1])

                elif key[0] == 'TRACK':
                    curTrackLine = line
                    callSign = key[1]

                elif key[0] == 'FP_ROUTE':
                    curFPLine = line

                    # Pull departure airport out of flight plan
                    depAirport  = curFPLine.split()[1].split('.')[0]
                    ACkey = '{0}_{1}'.format(callSign, depAirport)
#                     callSign_set.add(ACkey)

                    # Create this time record if necessary
                    if not TRX_Storage.has_key(ACkey):
                        TRX_Storage[ACkey] = []

                    # Store the info
                    TRX_Storage[ACkey].append(curTime)

                elif key[0][0] == '#':
                    # print 'COMMENT'
                    1

                else:
                    print "pruneTRXFromList: NewLine! This should not have been hit!"
                    print key
                    print line

    except:
        print "pruneTRXFromList: FAILURE in reading the file"
        printOkay = 0
        raise

    return TRX_Storage




###
# Pull out all of the callsign_dep combos from a TRX filter file and the associated times
###
def readTRXIntoDictByCallsign_APPEND(inFileName, TRX_Storage):
#     callSign_set = set()
#     TRX_Storage = dict()
    try:
        inputFile = open(inFileName, 'r')

        # This will hold the information as we run through the lines until it's time to save it to the dictionary
        curTime = -1
        curFPLine = ''
        curTrackLine = ''
        # shouldPrint = False

        for line in inputFile:
            key = line.split()

            if len(key) > 0:
                if key[0] == 'TRACK_TIME':
                    # Indicates progress
                    curTime = int(key[1])

                elif key[0] == 'TRACK':
                    curTrackLine = line
                    callSign = key[1]

                elif key[0] == 'FP_ROUTE':
                    curFPLine = line

                    # Pull departure airport out of flight plan
                    depAirport  = curFPLine.split()[1].split('.')[0]
                    ACkey = '{0}_{1}'.format(callSign, depAirport)
#                     callSign_set.add(ACkey)

                    # Create this time record if necessary
                    if not TRX_Storage.has_key(ACkey):
                        TRX_Storage[ACkey] = []

                    # Store the info
                    TRX_Storage[ACkey].append(curTime)

                elif key[0][0] == '#':
                    # print 'COMMENT'
                    1

                else:
                    print "pruneTRXFromList: NewLine! This should not have been hit!"
                    print key
                    print line

    except:
        print "pruneTRXFromList: FAILURE in reading the file"
        printOkay = 0
        raise

    return TRX_Storage


# def FindTimes(inFileName, curKey)

def stitchTogether(filterPath, rawPath, outFolder, inputFilters):
    Filter_Storage = dict() #debug scoping
    TRX_Storage = dict() #debug scoping
    CombinedStorage = dict()
    # callsignSet = []
    for curFilter in inputFilters:
        filterBaseName = curFilter.split('.')[0]
        fileToFilterOn = filterPath + curFilter
        print "Working on {0}".format(filterBaseName)

        # Just load the entire TRX, since it's been filtered, it should be relatively small
        Filter_Storage = readTRXIntoDictByCallsign_APPEND(fileToFilterOn, Filter_Storage)

    #     break

    for curFilter in inputFilters:
        filterBaseName = curFilter.split('.')[0]
        dateString = filterBaseName.split('_')[-1]

    #     fileToFilterOn = filterPath + curFilter
        fileToPrune = rawPath + "TRX_{0}.trx".format(dateString)
        outFileName = outFolder + filterBaseName + ".trx"   # This is good for debugging

        print "Working on {0}".format(filterBaseName)

        # Just load the entire TRX, since it's been filtered, it should be relatively small
    #     Filter_Storage = readTRXIntoDictByCallsign(fileToFilterOn)
        TRX_Storage = readTRXIntoDictByCallsign(fileToPrune)

        for curKey in Filter_Storage:
            if curKey in TRX_Storage:
                if curKey not in CombinedStorage:
                    CombinedStorage[curKey] = TRX_Storage[curKey]
                else:
                    CombinedStorage[curKey].extend(TRX_Storage[curKey])

    # Freeing the temp dicts
    Filter_Storage = dict() #debug scoping
    TRX_Storage = dict() #debug scoping


    filterDict = dict()
    for curCallSign in sorted(CombinedStorage.keys()):
        curTimes = np.array(CombinedStorage[curCallSign])
        jumpIXs = np.where(np.diff(curTimes)/60 > 180)[0]  #90 minutes
        keepIXs = [0]
        if len(jumpIXs) > 0:
            keepIXs.extend(jumpIXs + 1)

        for thisTime in curTimes[keepIXs]:
            if thisTime not in filterDict:
                filterDict[thisTime] = []
            filterDict[thisTime].append(curCallSign)

    # filterDict

    # Do the actual pruning.
    for curFilter in inputFilters:
        filterBaseName = curFilter.split('.')[0]
        dateString = filterBaseName.split('_')[-1]

    #     fileToFilterOn = filterPath + curFilter
        fileToPrune = rawPath + "TRX_{0}.trx".format(dateString)
        outFileName = outFolder + filterBaseName + ".trx"   #

        print "Pruning for {0}".format(curFilter)

        with Timer() as t:
            pruneTRXFromList_V2(fileToPrune, filterDict, outFileName)
        print "     => elasped time: %s s" % t.secs




#### The script that uses the above functions
import subprocess


# filterPath = "/Users/tcolvin1/Desktop/aiaaSpace/FilteredTRX/stitchTogether/"
filterPath = "/Users/tcolvin1/Desktop/aiaaSpace/FilteredTRX/finished/"
rawPath    = "/Users/tcolvin1/Desktop/aiaaSpace/RawTRX/"
outFolder  = "/Users/tcolvin1/Desktop/aiaaSpace/PrunedTRX/"

# inputFilters = glob.glob1(filterPath, "*.flt")
# # inputFilters = ["FrontRangeFilter_20130101.flt"]
# catName = "sdf"

allFilterFiles = glob.glob1(filterPath, "*.flt")
filterNames = set([obj.split('_')[0] for obj in allFilterFiles])
filterNames

for curName in filterNames:
    # Get the names of the filter files that apply to the curName filter, then run just those together before moving on.
    curFilterFiles = []
    for thisFile in allFilterFiles:
        if curName in thisFile:
            curFilterFiles.append(thisFile)
    curFilterFiles = sorted(curFilterFiles)
    print curFilterFiles

    stitchTogether(filterPath, rawPath, outFolder, curFilterFiles)

    # This is a little dangerous / not robust.  Should ideally call out all of the files individually from curFilterFiles
    callString = "cat {0}{1}_* > {0}TRX_{1}Stitched".format(outFolder, curName)
    subprocess.call(callString, shell=True)



#### ====
# Filter_Storage = dict() #debug scoping
# TRX_Storage = dict() #debug scoping
# CombinedStorage = dict()
# # callsignSet = []
# for curFilter in inputFilters:
#     filterBaseName = curFilter.split('.')[0]
#     dateString = filterBaseName.split('_')[-1]

#     fileToFilterOn = filterPath + curFilter
#     fileToPrune = rawPath + "TRX_{0}.trx".format(dateString)
#     outFileName = outFolder + filterBaseName + ".trx"   # This is good for debugging

#     print "Working on {0}".format(filterBaseName)

#     # Just load the entire TRX, since it's been filtered, it should be relatively small
#     Filter_Storage = readTRXIntoDictByCallsign(fileToFilterOn)
#     TRX_Storage = readTRXIntoDictByCallsign(fileToPrune)

#     for curKey in Filter_Storage:
#         if curKey not in CombinedStorage:
#             CombinedStorage[curKey] = TRX_Storage[curKey]
#         else:
#             CombinedStorage[curKey].extend(TRX_Storage[curKey])
# #     break

# # Freeing the temp dicts
# Filter_Storage = dict() #debug scoping
# TRX_Storage = dict() #debug scoping
#### ====






# sorted(Filter_Storage)

# len(TRX_Storage)
# len(Filter_Storage)
# len(CombinedStorage)

# Filter_Storage[Filter_Storage.keys()[0]]
# TRX_Storage.keys()
# len(TRX_Storage)

# curCallSign = sorted(Filter_Storage.keys())[1]
# curCallSign

# Filter_Storage[curCallSign]
# TRX_Storage[curCallSign]
# CombinedStorage[curCallSign]

# Have to be careful if last time is near midnight...might make next day double count.
# So if the last time in TRX_Storage is near midnight AND the callSign appears in the next day's Filter_Storage,
#  then make sure to connect the flight data up so to not double count.

# curTimes = np.array(CombinedStorage[curCallSign])
# jumpIXs = np.where(np.diff(curTimes)/60 > 15)[0]  #15 minutes
# jumpIXs
# keepIXs = [0]
# if len(jumpIXs) > 0:
#     keepIXs.extend(jumpIXs + 1)
# curTimes[keepIXs]


# np.diff(curTimes)/60




# 180000/(24*60)


# #### Some debugging
from datetime import timedelta as dt
from datetime import datetime
refDate = datetime(1970,1,1)

# sortedTimes = sorted(filterDict.keys())
# curKey = 1
# tix = -1
# for (tix, curKey) in enumerate(sortedTimes):
#     if (refDate + dt(seconds=int(curKey))).hour == 23:
#         break

# offset = 57
# sortedTimes[tix+offset]
# curKey = sortedTimes[tix+offset]
# curDate = refDate + dt(seconds=int(curKey))
# curDate

# filterDict[curKey]

# curSign = filterDict[curKey][0]
# CombinedStorage[curSign]
# curTimes = np.array(CombinedStorage[curSign])
# jumpIXs = np.where(np.diff(curTimes)/60 > 180)[0]  #90 minutes
# jumpIXs
# np.diff(curTimes)/60
# np.where(np.diff(curTimes)/60 == 11)

# curDate = refDate + dt(seconds=int(curTimes[0]))
# curDate


# refDate + dt(seconds=int(1356998813))
# refDate + dt(seconds=int(1357085214))


# # CombinedStorage["N221QS_KASE"]
# # curSign = "N221QS_KASE"
# curSign = "N139RN_KOGD"
# CombinedStorage[curSign]
# curTimes = np.array(CombinedStorage[curSign])
# jumpIXs = np.where(np.diff(curTimes)/60 > 180)[0]  #90 minutes
# jumpIXs
# np.diff(curTimes)/60
# np.where(np.diff(curTimes)/60 == 11)

# curDate = refDate + dt(seconds=int(curTimes[0]))
# curDate

# refDate + dt(seconds=int(1357084793))
# refDate + dt(seconds=int(1357085214))


# AAL604_KPDX, 10:53

#     # jumpIXs are the LAST times before the jump.
#     # Have to add 1 to index to get the first time of the next flight.

#     # This loop finds the first time that each unique flight is seen.  If it happens that the same flight is seen twice,
#     # (maybe it's a short jaunt and so it flies the route twice in a day, or the TRX file covers a few days) this loop
#     # also looks for time-discontinuities that would indicate these cases.  The resulting callsign, departure, times are
#     # used to prune the big file down to be, hopefully, just the first and last track update for each flight of interest
#     filterDict = dict()
#     for curCallSign in sortedKeys:
#         curTimes = np.array([obj[0] for obj in TRX_Storage[curCallSign]])
#         jumpIXs = np.where(np.diff(curTimes)/60 > 15)[0]  #15 minutes
#         print curTimes
#         print jumpIXs
#         print "\n"

#         # Three scenarios.
#         # 1.) Always take first track
#         # 2.) Take

#         keepIXs = np.unique(np.concatenate(([0], jumpIXs+1, [len(curTimes)-1])))
#         for thisTime in curTimes[keepIXs]:
#             if thisTime not in filterDict:
#                 filterDict[thisTime] = []
#             filterDict[thisTime].append(curCallSign)


#     # Do the actual pruning.
#     with Timer() as t:
#         pruneTRXFromList_V2(fileToPrune, filterDict, outFileName)
#     print "     => elasped time: %s s" % t.secs



#### Check that time-offsets for each call_dep don't change after midnight.

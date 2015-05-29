'''
Take a list of CallSigns and remove every track update that comes from an AC with that callsign
'''
import numpy as np
from TRX_functions import readTRXIntoDictByCallsign
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


# def pruneTRXFromList(inFileName, filterDict, outFileName, deltaSeconds = 0):
#     # Starts by eliminating every single aircraft (shouldPrint = False), but if an AC matches a filter,
#     #   then it will be allowed through.
#
#     print 'Pruning for ' + str(outFileName)
#     sortedKeys = sorted(filterDict.keys())
#     plainCallsigns = [curFlight.split('_')[0] for curFlight in sortedKeys]
#
#
#     # Keys are TRACK_TIMES, each value will be the strings (concatenated together) that are to be printed out
#     TRX_Storage = dict()
#
#     printOkay = True
#     if len(outFileName) == 0:
#         printOkay = False
#
#     try:
#         inputFile = open(inFileName, 'r')
#
#         # This will hold the information as we run through the lines until it's time to save it to the dictionary
#         curTime = -1
#         curFPLine = ''
#         curTrackLine = ''
#         shouldPrint = False
#         curCallSign = []    # Scope this here
#
#         for line in inputFile:
#             key = line.split()
#
#             if len(key) > 0:
#                 if key[0] == 'TRACK_TIME':
#                     # Indicates progress
#                     curTime = str(int(key[1]) + deltaSeconds)
#                     curTimeInt = int(key[1]) + deltaSeconds
#
#                 elif key[0] == 'TRACK':
#                     curCallSign = key[1]
#
#                     shouldPrint = (curCallSign in plainCallsigns)
#                     curTrackLine = line
#
#                 elif key[0] == 'FP_ROUTE':
#                     curFPLine = line
#
#                     # At this point we need to check for the departure Airport
#                     if shouldPrint:
#                         depAirport = key[1].split('.')[0]
#                         sign_dep = "{0}_{1}".format(curCallSign, depAirport)
#
#                         if sign_dep not in sortedKeys:
#                             shouldPrint = False
#                         elif curTimeInt not in filterDict[sign_dep]:
#                             shouldPrint = False
#
#
#                     # At this point, we will be done with the specific aircraf that we're looking at so save it if it's good
#                     if shouldPrint:
#                         # Create this time record if necessary
#                         if not TRX_Storage.has_key(curTime):
#                             TRX_Storage[curTime] = ''
#
#                         # Add it to the queue for printing
#                         TRX_Storage[curTime] = TRX_Storage[curTime] + curTrackLine
#                         TRX_Storage[curTime] = TRX_Storage[curTime] + curFPLine + '\n'
#
#                         # Reset
#                         shouldPrint = False
#
#                 elif key[0][0] == '#':
#                     # print 'COMMENT'
#                     1
#
#                 else:
#                     print "pruneTRXFromList: NewLine! This should not have been hit!"
#                     print key
#
#         inputFile.close() # It's likely that the output file will be the same file, so make sure to close this first.
#
#     except:
#         print "pruneTRXFromList: FAILURE in reading the file"
#         printOkay = 0
#         raise
#
#
#     if printOkay:
#         # # Now write everything to file
#         # try:
#         outFile = open(outFileName,'w')
#
#         for key in sorted(TRX_Storage.iterkeys()):
#             if len(TRX_Storage[key]) > 0:
#                 outFile.write('TRACK_TIME ' + key + '\n')
#                 outFile.write(TRX_Storage[key])
#
#         outFile.close()
#         # except:
#         #     print "FAIL
#     return TRX_Storage


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



def PruneBatch(filterPath, rawPath, outFolder):

    inputFilters = glob.glob1(filterPath, "*.flt")

    for curFilter in inputFilters:
        filterBaseName = curFilter.split('.')[0]
        dateString = filterBaseName.split('_')[-1]

        fileToFilterOn = filterPath + curFilter
        fileToPrune = rawPath + "TRX_{0}.trx".format(dateString)
        outFileName = outFolder + filterBaseName + ".trx"   # This is good for debugging

        print "Working on {0}".format(filterBaseName)

        # Just load the entire TRX, since it's been filtered, it should be relatively small
        TRX_Storage = readTRXIntoDictByCallsign(fileToFilterOn)
        sortedKeys      = sorted(TRX_Storage.keys())


        # jumpIXs are the LAST times before the jump.
        # Have to add 1 to index to get the first time of the next flight.

        # This loop finds the first time that each unique flight is seen.  If it happens that the same flight is seen twice,
        # (maybe it's a short jaunt and so it flies the route twice in a day, or the TRX file covers a few days) this loop
        # also looks for time-discontinuities that would indicate these cases.  The resulting callsign, departure, times are
        # used to prune the big file down to be, hopefully, just the first and last track update for each flight of interest
        filterDict = dict()
        for curCallSign in sortedKeys:
            curTimes = np.array([obj[0] for obj in TRX_Storage[curCallSign]])
            jumpIXs = np.where(np.diff(curTimes)/60 > 15)[0]  #15 minutes
            print curTimes
            print jumpIXs
            print "\n"

            # Three scenarios.
            # 1.) Always take first track
            # 2.) Take

            keepIXs = np.unique(np.concatenate(([0], jumpIXs+1, [len(curTimes)-1])))
            for thisTime in curTimes[keepIXs]:
                if thisTime not in filterDict:
                    filterDict[thisTime] = []
                filterDict[thisTime].append(curCallSign)


        # Do the actual pruning.
        with Timer() as t:
            pruneTRXFromList_V2(fileToPrune, filterDict, outFileName)
        print "     => elasped time: %s s" % t.secs




'''
This will read in the filter .flt that facet spit out, then output the first track updates of each flight from the
  source TRX.  Those will be written to files for later batch reading in.
'''
filterPath = "/Users/tcolvin1/Desktop/aiaaSpace/FilteredTRX/stitchTogether/"
rawPath    = "/Users/tcolvin1/Desktop/aiaaSpace/RawTRX/"
outFolder  = "/Users/tcolvin1/Desktop/aiaaSpace/PrunedTRX/"
PruneBatch(filterPath, rawPath, outFolder)





from datetime import timedelta as dt
from datetime import datetime
refDate = datetime(1970,1,1)

refDate.hour

# toCombineFolder = "/Users/tcolvin1/Desktop/aiaaSpace/PrunedTRX/done/"
# outFolder = "/Users/tcolvin1/Desktop/aiaaSpace/CombinedTRX/"
# fileNameVec = sorted(glob.glob1(toCombineFolder, "*.trx"))
# # fileNameVec = ["FrontRangeFilter_20130101.trx"]


# # FOR LOOP over file names
# TRX_Storage = dict()
# for curFileName in fileNameVec:
#     inFileName = toCombineFolder + curFileName
#     inputFile = open(inFileName, 'r')

#     # This will hold the information as we run through the lines until it's time to save it to the dictionary
#     curTime = -1
#     curFPLine = ''
#     curTrackLine = ''
#     shouldPrint = True
#     curCallSign = []    # Scope this here

#     for line in inputFile:
#         key = line.split()

#         if len(key) > 0:
#             if key[0] == 'TRACK_TIME':
#                 # Indicates progress
#                 curTime = str(int(key[1]))
#                 curTimeInt = int(key[1])

#             elif key[0] == 'TRACK':
#                 curCallSign = key[1]

#                 # shouldPrint = (curCallSign in plainCallsigns)
#                 curTrackLine = line

#             elif key[0] == 'FP_ROUTE':
#                 curFPLine = line

#                 # Pull departure airport out of flight plan
#                 depAirport  = curFPLine.split()[1].split('.')[0]
#                 ACkey = '{0}_{1}'.format(curCallSign, depAirport)

#                 # Create this time record if necessary
#                 if not TRX_Storage.has_key(ACkey):
#                     TRX_Storage[ACkey] = {'timeInt' : [], 'trackLine' : [], 'fpLine' : []}

#                 TRX_Storage[ACkey]['timeInt'].append(curTimeInt)
#                 TRX_Storage[ACkey]['trackLine'].append(curTrackLine)
#                 TRX_Storage[ACkey]['fpLine'].append(curFPLine)

#                 # # Add it to the queue for printing
#                 # TRX_Storage[curTime] = TRX_Storage[curTime] + curTrackLine
#                 # TRX_Storage[curTime] = TRX_Storage[curTime] + curFPLine + '\n'

#             elif key[0][0] == '#':
#                 # print 'COMMENT'
#                 1

#             else:
#                 print "pruneTRXFromList: NewLine! This should not have been hit!"
#                 print key

#     inputFile.close() # It's likely that the output file will be the same file, so make sure to close this first.


# TRX_Storage[TRX_Storage.keys()[0]]


# curDelta = dt(seconds=1356998873)
# curDelta
# curDate = refDate + curDelta
# curDate

# # Make sure we're not double-counting any track updates.
# printCount = 1
# for (curName, curDict) in TRX_Storage.iteritems():
#     print curName
#     print curDict['timeInt']
#     curTimes = np.array(curDict['timeInt'])
#     curDateVec = [refDate + dt(seconds=curSecs) for curSecs in curDict['timeInt']]
#     print curDateVec
# #     curTimes = np.array([obj[0] for obj in TRX_Storage[curCallSign]])
#     jumpIXs = np.where(np.diff(curTimes)/60 > 5)[0]
#     print np.diff(curTimes)/60
#     print "\n\n"

#     if printCount == 10:
#         break
#     printCount = printCount + 1
# #     keepIXs = np.unique(np.concatenate(([0], jumpIXs+1, [len(curTimes)-1])))
# #     for thisTime in curTimes[keepIXs]:
# #         if thisTime not in filterDict:
# #             filterDict[thisTime] = []
# #             filterDict[thisTime].append(curCallSign)

# # outFile = open(outFileName,'w')
# # for ix in range(len(timeStorage)):
# #     outFile.write(timeStorage[ix])
# #     for ac in range(len(aircraftAtTimeStorage[ix])):
# #         outFile.write(line1AtTimeStorage[ix][ac])
# #         outFile.write(line2AtTimeStorage[ix][ac])
# #         outFile.write('\n')



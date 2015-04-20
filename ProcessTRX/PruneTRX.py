'''
This is a bit of a garbage file for now.  Some of the remaining functions need to be moved into
TRX_functions when the need arises.
'''

import sys

'''Moved to TRX_functions.py'''
# '''
# RemoveTrackUpdates:
# Generally, a TRX file will have many track updates for a single aircraft.  This
# seems to produce some weird behavior when trying to simulate reroutes because it
# will hit a track update and mess up the reroute.  I wrote this function a long time ago
# so maybe i misunderstood the problem back then, but this function runs through a
# TRX file and pulls out the first instance of every aircraft that it sees and then
# records that collection of first-instances to a new TRX file.  This effectively strips
# away all of the track updates and forces FACET to simulate the aircraft along its
# flight plan (as it was at the time of the first track update).
# '''
# def RemoveTrackUpdates(inFileName,outFileName):
#     index = -1
#     currentAcList = []
#     allAcSeenThusFar = []
#
#     timeStorage = [];
#     aircraftAtTimeStorage = []
#     line1AtTimeStorage = []
#     line2AtTimeStorage = []
#
#     curLine1Storage = []
#     curLine2Storage = []
#
#     printOkay = 1
#
#     try:
#         inputFile = open(inFileName, 'r')
#         for line in inputFile:
#             key = line.split()
#             if len(key) > 0:
#                 if key[0] == 'TRACK_TIME':
#                     # Indicates progress
#                     print str(index)
# #                     import pdb; pdb.set_trace()  # XXX BREAKPOINT
#
#                     # store the track time line
#                     timeStorage.append(line)
#
#                     # Only append things after the first run through, i.e. when index is no longer -1, so that everything lines up
#                     if index >= 0:
#                         # store the new AC we just found
#                         aircraftAtTimeStorage.append(currentAcList)
#
#                         # Compile the list of aircraft that have already been seen
#                         allAcSeenThusFar.extend(currentAcList)
#
#                         # Store the lines to print at this timestep
#                         line1AtTimeStorage.append(curLine1Storage)
#                         line2AtTimeStorage.append(curLine2Storage)
#
#                         # Clear the cur variables
#                         currentAcList = []
#                         curLine1Storage = []
#                         curLine2Storage = []
#
#                     index += 1
#
#                 elif key[0] == 'TRACK':
#                     shouldPrint = (key[1] not in set(allAcSeenThusFar))
#                     if shouldPrint:
#                         currentAcList.append(key[1])
#                         curLine1Storage.append(line)
#
#                 elif key[0] == 'FP_ROUTE':
#                     if shouldPrint:
#                         curLine2Storage.append(line)
#
#                 elif key[0][0] == '#':
#                     print 'COMMENT'
#
#                 else:
#                     print "RemoveTrackUpdates: NewLine! This should not have been hit!"
#                     print key
#
#         # Now we're finished running through the file, have to play clean up to catch the last AC we filtered
#         # store the new AC we just found
#         aircraftAtTimeStorage.append(currentAcList)
#
#         # Compile the list of aircraft that have already been seen
#         allAcSeenThusFar.extend(currentAcList)
#
#         # Store the lines to print at this timestep
#         line1AtTimeStorage.append(curLine1Storage)
#         line2AtTimeStorage.append(curLine2Storage)
#
#
#     except:
#         print "FAILURE in reading the file"
#         printOkay = 0
#
#
#     if printOkay:
#         # Now write everything to file
#         try:
#             outFile = open(outFileName,'w')
#             for ix in range(len(timeStorage)):
#                 outFile.write(timeStorage[ix])
#                 for ac in range(len(aircraftAtTimeStorage[ix])):
#                     outFile.write(line1AtTimeStorage[ix][ac])
#                     outFile.write(line2AtTimeStorage[ix][ac])
#                     outFile.write('\n')
#
#
#             print line1AtTimeStorage[-1][-3:]
#
#         except:
#             print "FAILURE in writing the file"
#



# def pruneAbridgedTRXFromList(inFileName, vectorACIDs, outFileName):
#     index = -1
#     currentAcList = []
# #     allAcSeenThusFar = []
#
#     timeStorage = [];
#     aircraftAtTimeStorage = []
#     line1AtTimeStorage = []
#     line2AtTimeStorage = []
#
#     curLine1Storage = []
#     curLine2Storage = []
#
#     printOkay = 1
#
#     try:
#         inputFile = open(inFileName, 'r')
#         for line in inputFile:
#             key = line.split()
#             if len(key) > 0:
#                 if key[0] == 'TRACK_TIME':
#                     # Indicates progress
#                     print str(index)
#
#                     # store the track time line
#                     timeStorage.append(line)
#
#                     # Only append things after the first run through, i.e. when index is no longer -1, so that everything lines up
#                     if index >= 0:
#                         # store the new AC we just found
#                         aircraftAtTimeStorage.append(currentAcList)
#
#                         ## Compile the list of aircraft that have already been seen
#                         #allAcSeenThusFar.extend(currentAcList)
#
#                         # Store the lines to print at this timestep
#                         line1AtTimeStorage.append(curLine1Storage)
#                         line2AtTimeStorage.append(curLine2Storage)
#
#                         # Clear the cur variables
#                         currentAcList = []
#                         curLine1Storage = []
#                         curLine2Storage = []
#
#                     index += 1
#
#                 elif key[0] == 'TRACK':
#                     shouldPrint = (key[1] in set(vectorACIDs))
#                     if shouldPrint:
#                         currentAcList.append(key[1])
#                         curLine1Storage.append(line)
#
#                 elif key[0] == 'FP_ROUTE':
#                     if shouldPrint:
#                         curLine2Storage.append(line)
#
#                 else:
#                     print "NewLine! This should not have been hit!"
#
#         # Now we're finished running through the file, have to play clean up to catch the last AC we filtered
#         # store the new AC we just found
#         aircraftAtTimeStorage.append(currentAcList)
#
#         ## Compile the list of aircraft that have already been seen
#         #allAcSeenThusFar.extend(currentAcList)
#
#         # Store the lines to print at this timestep
#         line1AtTimeStorage.append(curLine1Storage)
#         line2AtTimeStorage.append(curLine2Storage)
#
#
#     except:
#         print "FAILURE in reading the file"
#         printOkay = 0
#
#
#     if printOkay:
#         # Now write everything to file
#         try:
#             outFile = open(outFileName,'w')
#             for ix in range(len(timeStorage)):
#                 outFile.write(timeStorage[ix])
#                 for ac in range(len(aircraftAtTimeStorage[ix])):
#                     outFile.write(line1AtTimeStorage[ix][ac])
#                     outFile.write(line2AtTimeStorage[ix][ac])
#                     outFile.write('\n')
#
#
#             print line1AtTimeStorage[-1][-3:]
#
#         except:
#             print "FAILURE in writing the file"





# def uniqueAffected(inFileName, abridgedTRXFile, outFileName):
#     index = -1
#     timeVec = []
#     aircraftListFull = []
#
#     # Read in the file and load up aircraftListFull with all of the ACIDs present in the file
#     try:
#         inputFile = open(inFileName,'r')
#         for line in inputFile:
#             key = line.split()
#             if len(key) > 0:
#                 if key[0] == '#':
#                     index += 1
#                     aircraftListFull.append([])     #push back an empty list
#                 elif key[0] == 'TRACK_TIME':
#                     timeVec.append(key[1])          #save the current timestep
#                 elif key[0] == 'TRACK':
#                     aircraftListFull[index].append(key[1])
#
#     except:
#         print "FAILURE in reading the file"
#
#     #Find unique aircraft
#     uniqueAcList = []
#     try:
#         for ix in range(index):
#             uniqueAcList.extend(set(aircraftListFull[ix]) - set(uniqueAcList))
#
#         print "unique = ",
#         print str((uniqueAcList)),
#
#         print "\nNumber of unique aircraft affected = " + str(len(uniqueAcList))
#
#     except:
#         print "FAILURE in processing the aircraft"
#
#     #How long was each aircraft affected?
#
#     # Find those AC's and write that to a file
#     pruneAbridgedTRXFromList(abridgedTRXFile, uniqueAcList, outFileName)

'''
Take a list of CallSigns and remove every track update that does come from an AC with that callsign
MOVED TO TRX_Functions.py
'''
# def pruneTRXFromList(inFileName, filterDict, outFileName, deltaSeconds = 0):
#     # Starts by eliminating every single aircraft (shouldPrint = False), but if an AC matches a filter,
#     #   then it will be allowed through.
#
#     print 'Pruning for ' + str(outFileName)
#     # Unpack the filters and determine if they're active or not
#     callsigns           = set(filterDict['callsigns'])
#     filterCallsigns     = len(callsigns) > 0
#
#     sectorNames         = filterDict['sectorNames']
#     filterSectorNames   = len(sectorNames) > 0
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
#
#         for line in inputFile:
#             key = line.split()
#
#             if len(key) > 0:
#                 if key[0] == 'TRACK_TIME':
#                     # Indicates progress
#                     curTime = str(int(key[1]) + deltaSeconds)
#
#                 elif key[0] == 'TRACK':
#                     if filterCallsigns:
#                         shouldPrint = (key[1] in callsigns)    #Sets it true
#
#                     if filterSectorNames:
#                         shouldPrint = shouldPrint or (key[8] in set(sectorNames))   # Another chance to be true
#
#                     # modifiedSign = key[1] + '_' + suffixList[fileCounter]
#                     if (key[1] == 'EJM626'):
#                         print 'DEBUG {0}, shouldPrint {1}'.format(key[1], shouldPrint)
#
#                     curTrackLine = line
#
#                 elif key[0] == 'FP_ROUTE':
#                     curFPLine = line
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
#     except:
#         print "pruneTRXFromList: FAILURE in reading the file"
#         printOkay = 0
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
#         # except:
#         #     print "FAIL
#     return TRX_Storage

    

'''
Have to worry about aircraft with overlapping callsigns!
'''
def CombineTRXFiles(TRX_FileList, suffixList, outFileName):
    TRX_Storage = dict()

    print TRX_FileList
    # TRX_FileList = [TRX1, TRX2]

    printOkay = True
    if len(outFileName) == 0:
        printOkay = False

    try:
        fileCounter = 0
        for TRX_File in TRX_FileList:
            inputFile = open(TRX_File, 'r')
            print TRX_File

            # This will hold the information as we run through the lines until it's time to save it to the dictionary
            curTime = -1
            curFPLine = ''
            curTrackLine = ''

            for line in inputFile:
                key = line.split()

                if len(key) > 0:
                    if key[0] == 'TRACK_TIME':
                        # Indicates progress
                        curTime = key[1]

                        # Create this time record if necessary
                        if not TRX_Storage.has_key(curTime):
                            TRX_Storage[curTime] = ''

                    elif key[0] == 'TRACK':
                        # Change the callsign (key[1]) to avoid overlaps between files
                        # key[1] = key[1] + '_' + str(fileCounter)

                        modifiedSign = key[1] + '_' + suffixList[fileCounter]
                        if (key[1] == 'EJM626'):
                            print 'DEBUG ' + modifiedSign

                        key[1] = modifiedSign

                        # Then piece the current line back together
                        curTrackLine = ' '.join(key) + '\n'


                    elif key[0] == 'FP_ROUTE':
                        curFPLine = line

                        # At this point, we will be done with the specific aircraf that we're looking at so save it
                        TRX_Storage[curTime] = TRX_Storage[curTime] + curTrackLine
                        TRX_Storage[curTime] = TRX_Storage[curTime] + curFPLine + '\n'


                    else:
                        print "CombineTRXFiles: NewLine! This should not have been hit!"
                        print key

            inputFile.close()
            fileCounter += 1
    except:
        print "CombineTRXFiles: FAILURE in reading the file"
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

        # except:
        #     print "FAIL
    return TRX_Storage



'''
Scan through a TRX file and pull out all of the callsigns
'''
def getAllCallsigns(inFileName):

    callsignStorage = dict()
    try:
        inputFile = open(inFileName, 'r')

        curTime = 0                 # Keeps track of current time
        curSign = ""                # Keeps track of current call sign

        for line in inputFile:
            key = line.split()

            if len(key) > 0:
                if key[0] == 'TRACK_TIME':
                    # Indicates progress
                    curTime = key[1]

                if key[0] == 'TRACK':
                    # AirTOp lists multiple legs like VM701#3, so split the hash off and keep the base sign
                    curSign = key[1].split('#')[0]

                if key[0] == 'FP_ROUTE':
                    depAirport = key[1].split('.')[0]

                    try:
                        if not callsignStorage.has_key(curSign):
                            # If the callsign is new, add it to the storage dictionary
                            callsignStorage[curSign] = dict(timeSec=[long(curTime)], depAirport=[depAirport])

                        elif depAirport not in set(callsignStorage[curSign]['depAirport']):
                        # elif callsignStorage[curSign][depAirport] is not depAirport:
                            # If there is a different leg of the flight, add it
                            callsignStorage[curSign]['timeSec'].append(long(curTime))
                            callsignStorage[curSign]['depAirport'].append(depAirport)
                    except:
                        print depAirport
                        raise




        inputFile.close()
    except:
        print 'ERROR: getAllCallsigns failed'
        raise

    # Return the set
    return callsignStorage

# def getAllCallsigns(inFileName):
#
#     callsignStorage = set()
#     try:
#         inputFile = open(inFileName, 'r')
#
#         curTime = 0                 # Keeps track of current time
#         for line in inputFile:
#             key = line.split()
#
#             if len(key) > 0:
#                 if key[0] == 'TRACK_TIME':
#                     # Indicates progress
#                     curTime = key[1]
#
#                 if key[0] == 'TRACK':
#                     if (key[1] not in callsignStorage):
#                         callsignStorage.add(key[1])     # If the callsign is new, add it to the list (set)
#
#         inputFile.close()
#     except:
#         print 'ERROR: getAllCallsigns failed'
#         raise
#
#     # Return the set
#     return callsignStorage

    
    
'''
This is a script to use the above functions
'''


# Get all the callsigns from FACET
# inFileNameFACET = '/Volumes/Storage/OldDocuments/Research/FACE2/FACET-1109-Darwin-10.6-x86_64/user/work/TRX_March012013_ZMA_ZJX'
inFileNameFACET = '/Users/marian/Dropbox/To_Facet/TRX_March012013_V3Offset'

FACET_dict = getAllCallsigns(inFileNameFACET)
FACET_Callsigns = set(FACET_dict.keys())

# Get all the callsigns from AirTOp
inFileNameAirTOp = '/Volumes/Storage/OldDocuments/Research/FACE2/Sandbox/TRX_Airtop_Full'
AirTOp_dict = getAllCallsigns(inFileNameAirTOp)
AirTOp_Callsigns = set(AirTOp_dict.keys())

# Find the similar and disimilar ones and convert to lists
commonCallsigns = list(FACET_Callsigns.intersection(AirTOp_Callsigns))
uniqueFACET     = list(FACET_Callsigns.difference(AirTOp_Callsigns))
uniqueAirTOp    = list(AirTOp_Callsigns.difference(FACET_Callsigns))

print 'Number of Callsigns In Common        : {0}'.format(len(commonCallsigns))
print 'Number of Callsigns Unique To FACET  : {0}'.format(len(uniqueFACET))
print 'Number of Callsigns Unique to AirTp  : {0}'.format(len(uniqueAirTOp))


# Pair them off by 100s and make combined TRX files for comparison
numInCommon     = len(commonCallsigns)
numPerOutput    = 100

curFilterCallsigns = commonCallsigns[:100]
filterDict      = dict(callsigns = curFilterCallsigns, sectorNames = [])

# Offset that we'll use on AirTOp data (on March 1st, it's EST (-5) as opposed to EDT(-4))
airtopOffsetSec = (5)*3600

# Dump the time offsets for the current common callsigns
for AC in curFilterCallsigns:
    print AC
    print 'FACET Deps {0} at {1}'.format(FACET_dict[AC]['depAirport'],FACET_dict[AC]['timeSec'])
    print 'AirTp Deps {0} at {1}'.format(AirTOp_dict[AC]['depAirport'],AirTOp_dict[AC]['timeSec'])
    # Airtop usually only has one departure airport, use that
    # numAirpts = len(AirTOp_dict[AC]['depAirport'])
    # if numAirpts == 1:
    for curAirpt in AirTOp_dict[AC]['depAirport']:
        # curAirpt = AirTOp_dict[AC]['depAirport'][0]

        # Is it in the list?
        if curAirpt in FACET_dict[AC]['depAirport']:
            # Find the location
            ixFacet = FACET_dict[AC]['depAirport'].index(curAirpt)
            ixAirTp = AirTOp_dict[AC]['depAirport'].index(curAirpt)

            offsetMin = (FACET_dict[AC]['timeSec'][ixFacet] - AirTOp_dict[AC]['timeSec'][ixAirTp] - airtopOffsetSec)/60.
            print '[{1},{2}], offset = {3} minutes'.format(AC, FACET_dict[AC]['depAirport'][ixFacet], AirTOp_dict[AC]['depAirport'][ixAirTp], offsetMin)
        else:
            print '{0}: THERE ARE NO OVERLAPPING FLIGHTS FROM HERE!!!'.format(curAirpt)

    # else:
    #     # youv'e been hardcoding to just use the first airtop depAirport
    #     print 'ERROR: Stop and think about this'
    #     sys.exit()

    print ''
    # offsetMin = (FACET_dict[AC]['timeSec'][0] - AirTOp_dict[AC]['timeSec'][0] - airtopOffsetSec)/60.
    # print '{0} [{1},{2}]offset = {3} minutes'.format(AC, FACET_dict[AC]['depAirport'][0], AirTOp_dict[AC]['depAirport'][0], offsetMin)

# Prune them into temp files
TRX1 = 'TRX_tempFACET'
facetOffsetSec = 5*60   #ASDI data is known to be off by 5 minutes...however i think i fixed it in the main TRX
pruneTRXFromList(inFileNameFACET, filterDict, TRX1, deltaSeconds = 0)

TRX2 = 'TRX_tempAirTOp'
pruneTRXFromList(inFileNameAirTOp, filterDict, TRX2, deltaSeconds = airtopOffsetSec)

suffix = ['F','A']
TRX_List = [TRX1, TRX2]

outFileName = '/Volumes/Storage/OldDocuments/Research/FACE2/Sandbox/Comparisons/TRX_Comparison_' + str(0)
CombineTRXFiles(TRX_List, suffix, outFileName)















# # vectorCallsigns = ['SWA403']  #Terminated
# # vectorCallsigns = ['UAL362']  #Active           Not present in ASDI data
# # vectorCallsigns = ['SIL3992'] #Planned              +7:46
# vectorCallsigns = ['AWE1523'] #Airborne         +5:46
# vectorSectors   = ['ZJX', 'ZMA']
# filterDict      = dict(callsigns = vectorCallsigns, sectorNames = vectorSectors)
#
# # vectorCallsigns = ['DAL110','SWA403', 'AWE1523']
#
#
# # inFileName = '../ProcessAirTOpFlightPlans/OutputFiles/TRX_Falcon9_March_1_2013'
# # inFileName = '/Volumes/Storage/OldDocuments/Research/FACE2/Sandbox/TRX_Falcon9_March_1_2013_Airtop'
# inFileName = '/Volumes/Storage/OldDocuments/Research/FACE2/Sandbox/TRX_Airtop_Full'
#
# # TRX1 = 'TRX_PrunedByList_AirTOp'
# # deltaSeconds1 = (5)*3600 + 46*60
# # TRX_Storage = pruneTRXFromList(inFileName, filterDict, TRX1, deltaSeconds1)
#
# inFileName = '/Users/marian/Dropbox/To_Facet/TRX_March012013_V3Offset'
# # inFileName = '/Users/marian/Dropbox/To_Facet/TRX_February282013'
# TRX2 = 'TRX_PrunedByList_FACET'
# deltaSeconds2 = -5*60
# TRX_Storage = pruneTRXFromList(inFileName, filterDict, TRX2, deltaSeconds2)
# # 1362188875
#
# # TRX_fileList = [TRX2]
# # # outFileName = '/Volumes/Storage/OldDocuments/Research/FACE2/Sandbox/TRX_March012013_test'
# # outFileName = 'TRX_March012013_test'
# # CombineTRXFiles(TRX_fileList, outFileName)











# # vectorCallsigns = ['SWA403']  #Terminated
# # vectorCallsigns = ['UAL362']  #Active           Not present in ADSI data
# # vectorCallsigns = ['SIL3992'] #Planned              +7:46
# vectorCallsigns = ['AWE1523'] #Airborne         +5:46
# vectorSectors   = ['ZJX', 'ZMA']
# filterDict      = dict(callsigns = vectorCallsigns, sectorNames = vectorSectors)
#
# vectorCallsigns = ['DAL110','SWA403', 'AWE1523']
# # inFileName = '../ProcessAirTOpFlightPlans/OutputFiles/TRX_Falcon9_March_1_2013'
# # inFileName = '/Volumes/Storage/OldDocuments/Research/FACE2/Sandbox/TRX_Falcon9_March_1_2013_Airtop'
# inFileName = '/Volumes/Storage/OldDocuments/Research/FACE2/Sandbox/TRX_Airtop_Full'
#
# # TRX1 = 'TRX_PrunedByList_AirTOp'
# # deltaSeconds1 = (5)*3600 + 46*60
# # TRX_Storage = pruneTRXFromList(inFileName, filterDict, TRX1, deltaSeconds1)
#
# inFileName = '/Users/marian/Dropbox/To_Facet/TRX_March012013_V3Offset'
# # inFileName = '/Users/marian/Dropbox/To_Facet/TRX_February282013'
# TRX2 = 'TRX_PrunedByList_FACET'
# deltaSeconds2 = -5*60
# TRX_Storage = pruneTRXFromList(inFileName, filterDict, TRX2, deltaSeconds2)
#
# # TRX_fileList = [TRX1, TRX2]
# # outFileName = '/Volumes/Storage/OldDocuments/Research/FACE2/Sandbox/TRX_Combined'
# # CombineTRXFiles(TRX_fileList, outFileName)

    
    
    
    
    
    
    
    
    
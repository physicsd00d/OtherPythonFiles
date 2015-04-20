
ft2m = 0.3048

def readTRXIntoDictByCallsign(inFileName):
    # Starts by eliminating every single aircraft (shouldPrint = False), but if an AC matches a filter,
    #   then it will be allowed through.

    print 'readTRXIntoDictByCallsign for ' + str(inFileName)
    # # Unpack the filters and determine if they're active or not
    # callsigns           = set(filterDict['callsigns'])
    # filterCallsigns     = len(callsigns) > 0
    #
    # sectorNames         = filterDict['sectorNames']
    # filterSectorNames   = len(sectorNames) > 0

    # Best idea for keys is callsign_departureAirport
    TRX_Storage = dict()

    # printOkay = True
    # if len(outFileName) == 0:
    #     printOkay = False

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
                    callSign        = trackKeys[1]                          # string
                    latString       = trackKeys[3]                          # string
                    lonString       = trackKeys[4]                          # string
                    flightLevel     = float(trackKeys[6]) * 100. * ft2m     # 100s of feet, convert to meters

                    # # Lat/Lon comes in strings of DegMinSec, so parse that out.
                    # latSeconds      = float(latString[-2:])
                    # latMinutes      = float(latString[-4:-2])
                    # if len(latString) == 6:
                    #     latDegrees  = float(latString[:2])
                    # elif len(latString) == 7:
                    #     latDegrees  = float(latString[:3])
                    # elif latString == "000":
                    #
                    # else:
                    #     print "BAD LATITUDE FORMAT: {0}".format(latString)
                    #     raise RuntimeError
                    #
                    # lonSeconds      = float(lonString[-2:])
                    # lonMinutes      = float(lonString[-4:-2])
                    # if len(lonString) == 6:
                    #     lonDegrees  = float(lonString[:2])
                    # elif len(lonString) == 7:
                    #     lonDegrees  = float(lonString[:3])
                    # else:
                    #     print "BAD LONGITUDE FORMAT: {0}".format(lonString)
                    #     raise RuntimeError
                    #
                    # # Compute the decimal values for the positon
                    # latitude    = latDegrees + latMinutes/60. + latSeconds/3600.
                    # longitude   = -(lonDegrees + lonMinutes/60. + lonSeconds/3600.)   #All lons are given as West

                    latitude = -361
                    longitude = -361
                    # print 'latString = {0}, latitude = {1}'.format(latString, latitude)
                    # sys.exit()

                    # Pull departure airport out of flight plan
                    depAirport  = curFPLine.split()[1].split('.')[0]

                    ACkey = '{0}_{1}'.format(callSign, depAirport)

                    # Create this time record if necessary
                    if not TRX_Storage.has_key(ACkey):
                        TRX_Storage[ACkey] = []

                    # Store the info
                    TRX_Storage[ACkey].append([curTime, latitude, longitude, flightLevel])




                    # return [curTime, curTrackLine, curFPLine]

                    # # At this point, we will be done with the specific aircraf that we're looking at so save it if it's good
                    # if shouldPrint:
                    #     # Create this time record if necessary
                    #     if not TRX_Storage.has_key(curTime):
                    #         TRX_Storage[curTime] = ''
                    #
                    #     # Add it to the queue for printing
                    #     TRX_Storage[curTime] = TRX_Storage[curTime] + curTrackLine
                    #     TRX_Storage[curTime] = TRX_Storage[curTime] + curFPLine + '\n'
                    #
                    #     # Reset
                    #     shouldPrint = False

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


'''
Take a list of CallSigns and remove every track update that does come from an AC with that callsign
'''
def pruneTRXFromList(inFileName, filterDict, outFileName, deltaSeconds = 0):
    # Starts by eliminating every single aircraft (shouldPrint = False), but if an AC matches a filter,
    #   then it will be allowed through.

    print 'Pruning for ' + str(outFileName)
    # Unpack the filters and determine if they're active or not
    callsigns           = set(filterDict['callsigns'])
    filterCallsigns     = len(callsigns) > 0

    sectorNames         = filterDict['sectorNames']
    filterSectorNames   = len(sectorNames) > 0

    filterDepAirports   = filterDict['filterDepAirports']
    filterTimes         = filterDict['filterTimes']

    bigFilterKeys       = filterDict['bigFilterKeys']

    # filterDict = {'callsigns' : flightsToKeep, 'sectorNames' : [], 'filterDepAirports' : filterDepAirports,
              # 'filterTimes' : filterTimes, 'bigFilterKeys' : bigFilterKeys}

    # # departureAirports needs to match one-to-one with callsigns.  Check that
    # if filterDepartures and (len(filterDict['callsigns']) != len(departureAirports)):
    #     print 'ERROR: len(callsigns) != len(departureAirports)'
    #     print (len(callsigns) != len(departureAirports))
    #     print filterDepartures
    #     print len(callsigns)
    #     print len(departureAirports)
    #     raise RuntimeError

    # Keys are TRACK_TIMES, each value will be the strings (concatenated together) that are to be printed out
    TRX_Storage = dict()

    printOkay = True
    if len(outFileName) == 0:
        printOkay = False

    try:
        inputFile = open(inFileName, 'r')

        # This will hold the information as we run through the lines until it's time to save it to the dictionary
        curTime = -1
        curFPLine = ''
        curTrackLine = ''
        shouldPrint = False
        curCallSign = []    # Scope this here

        for line in inputFile:
            key = line.split()

            if len(key) > 0:
                if key[0] == 'TRACK_TIME':
                    # Indicates progress
                    curTime = str(int(key[1]) + deltaSeconds)

                elif key[0] == 'TRACK':
                    curCallSign = key[1]
                    if filterCallsigns:
                        shouldPrint = (curCallSign in callsigns)    #Sets it true

                    if filterSectorNames:
                        shouldPrint = shouldPrint or (key[8] in set(sectorNames))   # Another chance to be true

                    # modifiedSign = key[1] + '_' + suffixList[fileCounter]
                    # if (key[1] == 'EJM626'):
                    #     print 'DEBUG {0}, shouldPrint {1}'.format(key[1], shouldPrint)

                    curTrackLine = line

                elif key[0] == 'FP_ROUTE':
                    curFPLine = line

                    # At this point we need to check for the departure Airport
                    if shouldPrint:
                        # This means that the callsign is present, but not necessarily the other possible filters
                        if filterDepAirports and filterTimes:
                            # This means we're filtering based on departures, so make sure...
                            depAirport = key[1].split('.')[0]
                            filterKey = '{0}_{1}_{2}'.format(curCallSign, depAirport, curTime)
                            if filterKey not in bigFilterKeys:
                                shouldPrint = False
                        elif not (filterDepAirports and filterTimes):
                            #Do Nothing
                            None
                        else:
                            print 'You shoudl not have wound up here.  Handle this case if you want to proceed.'
                            raise RuntimeError

                    # At this point, we will be done with the specific aircraf that we're looking at so save it if it's good
                    if shouldPrint:
                        # Create this time record if necessary
                        if not TRX_Storage.has_key(curTime):
                            TRX_Storage[curTime] = ''

                        # Add it to the queue for printing
                        TRX_Storage[curTime] = TRX_Storage[curTime] + curTrackLine
                        TRX_Storage[curTime] = TRX_Storage[curTime] + curFPLine + '\n'

                        # Reset
                        shouldPrint = False

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







'''
NOTE: This function only cares about callsign, so it's not very robust.  Either fix or don't use.

RemoveTrackUpdates:
Generally, a TRX file will have many track updates for a single aircraft.  This
seems to produce some weird behavior when trying to simulate reroutes because it
will hit a track update and mess up the reroute.  I wrote this function a long time ago
so maybe i misunderstood the problem back then, but this function runs through a
TRX file and pulls out the first instance of every aircraft that it sees and then
records that collection of first-instances to a new TRX file.  This effectively strips
away all of the track updates and forces FACET to simulate the aircraft along its
flight plan (as it was at the time of the first track update).
'''
def RemoveTrackUpdates(inFileName,outFileName):
    index = -1
    currentAcList = []
    allAcSeenThusFar = []

    timeStorage = [];
    aircraftAtTimeStorage = []
    line1AtTimeStorage = []
    line2AtTimeStorage = []

    curLine1Storage = []
    curLine2Storage = []

    printOkay = 1

    try:
        inputFile = open(inFileName, 'r')
        for line in inputFile:
            key = line.split()
            if len(key) > 0:
                if key[0] == 'TRACK_TIME':
                    # Indicates progress
                    print str(index)
#                     import pdb; pdb.set_trace()  # XXX BREAKPOINT

                    # store the track time line
                    timeStorage.append(line)

                    # Only append things after the first run through, i.e. when index is no longer -1, so that everything lines up
                    if index >= 0:
                        # store the new AC we just found
                        aircraftAtTimeStorage.append(currentAcList)

                        # Compile the list of aircraft that have already been seen
                        allAcSeenThusFar.extend(currentAcList)

                        # Store the lines to print at this timestep
                        line1AtTimeStorage.append(curLine1Storage)
                        line2AtTimeStorage.append(curLine2Storage)

                        # Clear the cur variables
                        currentAcList = []
                        curLine1Storage = []
                        curLine2Storage = []

                    index += 1

                elif key[0] == 'TRACK':
                    shouldPrint = (key[1] not in set(allAcSeenThusFar))
                    if shouldPrint:
                        currentAcList.append(key[1])
                        curLine1Storage.append(line)

                elif key[0] == 'FP_ROUTE':
                    if shouldPrint:
                        curLine2Storage.append(line)

                elif key[0][0] == '#':
                    print 'COMMENT'

                else:
                    print "RemoveTrackUpdates: NewLine! This should not have been hit!"
                    print key

        # Now we're finished running through the file, have to play clean up to catch the last AC we filtered
        # store the new AC we just found
        aircraftAtTimeStorage.append(currentAcList)

        # Compile the list of aircraft that have already been seen
        allAcSeenThusFar.extend(currentAcList)

        # Store the lines to print at this timestep
        line1AtTimeStorage.append(curLine1Storage)
        line2AtTimeStorage.append(curLine2Storage)


    except:
        print "FAILURE in reading the file"
        printOkay = 0


    if printOkay:
        # Now write everything to file
        try:
            outFile = open(outFileName,'w')
            for ix in range(len(timeStorage)):
                outFile.write(timeStorage[ix])
                for ac in range(len(aircraftAtTimeStorage[ix])):
                    outFile.write(line1AtTimeStorage[ix][ac])
                    outFile.write(line2AtTimeStorage[ix][ac])
                    outFile.write('\n')


            print line1AtTimeStorage[-1][-3:]

        except:
            print "FAILURE in writing the file"


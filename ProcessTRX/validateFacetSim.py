'''
It's been so long, i'm not quite sure what this file is doing.  It seems to look at every single
 aircraft from the data and from the simulation and compare the flight times / starting locations.
 Further, it plots them both in google earth.
'''

from TRX_functions import readTRXIntoDictByCallsign
import sys
# Points to the python scripts needed from Francisco
friscoFiles = '../../../Prop3Dof/FriscoDebris/pythonFiles/'
sys.path.append(friscoFiles)
import data2GE

# Read in the raw ETMS data.  To be simple, this can come from the input TRX file.
ETMS_File       = 'TRX_Files/TRX_Columbia_HighRisk002'
ETMS_Storage    = readTRXIntoDictByCallsign(ETMS_File)

# Read in the simulated data that FACET output (TRX)
# SIM_File        = 'FilesToValidate/TRX_ColumbiaHighRiskSimToValidate'
SIM_File        = 'TRX_Files/TRX_Columbia_HighRisk004'
SIM_Storage     = readTRXIntoDictByCallsign(SIM_File)

# I currently assume both files contain the exact same aircraft, no more no less
# Loop through the aircraft
for ACkey in ETMS_Storage.keys():
    curETMS = ETMS_Storage[ACkey]
    curSIM  = SIM_Storage[ACkey]

    firstTrackTimeETMS  = curETMS[0][0]
    firstLatETMS        = curETMS[0][1]
    firstLonETMS        = curETMS[0][2]
    firstAltETMS        = curETMS[0][3]
    lastTrackTimeETMS   = curETMS[-1][0]

    # firstTrackTimeSIM   = curSIM[0][0]
    [firstTrackTimeSIM, firstLatSIM, firstLonSIM, firstAltSIM] = curSIM[0]

    lastTrackTimeSIM    = curSIM[-1][0]

    print ACkey
    print 'ETMS duration    = {0} minutes'.format((lastTrackTimeETMS - firstTrackTimeETMS)/60.)
    print '     LatLon0     = {0}, {1}'.format(firstLatETMS, firstLonETMS)
    print 'SIM  duration    = {0} minutes'.format((lastTrackTimeSIM  - firstTrackTimeSIM)/60.)
    print '     LatLon0     = {0}, {1}'.format(firstLatSIM, firstLonSIM)
    print ''

'''
# I could avoid errors due to the propagation of the trajectories (wind / other variables)
#   by simply finding the times when the ETMS data say the aircraft got near the Columbia debris.

Could make a big difference for the aircraft that were inbound to Texas.  Less impact on those outbound.

Debris is already in NAS within the first minute after breakup.  Just use the ETMS data starting a minute or so earlier.
** That's not quite true; I had a bug before.  Debris takes two minutes to enter NAS.
'''

# For all aircraft present, determine time of departure and landing

# Eventualy, determine distance flown if possible from the raw data
    # with present data, could do some integrated error from lat / lon.  Search Haversine


# Again find all the same metrics

# Print and compare
'''ETMS First'''
fileNameGE = 'ETMS.kml'

flatArray       = []  #lat lon alt vx vy vz lat lon alt vx vy vz lat lon ...
numTimeSteps    = []
callSigns       = []
filterAircraft  = []

for flightRecord in ETMS_Storage.iteritems():
    curSign = flightRecord[0]
    dataList = flightRecord[1]

    noFilter = (len(filterAircraft) == 0)

    # if curSign == 'AWI377_LNK':
    if noFilter or (curSign in filterAircraft):
        subFlatArray = []

        for entry in dataList:
            # Don't care about velocity information here, so just use zeros
            subFlatArray.extend(entry[1:])
            subFlatArray.extend([0,0,0])

        flatArray.extend(subFlatArray)
        numTimeSteps.extend([len(dataList)])
        callSigns.append(curSign)
data2GE.convertTJCAircraft(fileNameGE, flatArray, numTimeSteps, callSigns, numElementsPerLine = 6)




'''Then again with FACET sim'''
fileNameGE = 'INTERP.kml'

flatArray       = []  #lat lon alt vx vy vz lat lon alt vx vy vz lat lon ...
numTimeSteps    = []
callSigns       = []
filterAircraft  = []

for flightRecord in SIM_Storage.iteritems():
    curSign = flightRecord[0]
    dataList = flightRecord[1]

    noFilter = (len(filterAircraft) == 0)

    # if curSign == 'AWI377_LNK':
    if noFilter or (curSign in filterAircraft):
        subFlatArray = []

        for entry in dataList:
            # Don't care about velocity information here, so just use zeros
            subFlatArray.extend(entry[1:])
            subFlatArray.extend([0,0,0])

        flatArray.extend(subFlatArray)
        numTimeSteps.extend([len(dataList)])
        callSigns.append(curSign)
data2GE.convertTJCAircraft(fileNameGE, flatArray, numTimeSteps, callSigns, numElementsPerLine = 6)



'''
This function is not yet ready for primetime.  Used to plot TRX files in google earth
'''

import sys
import numpy as np

from datetime import datetime
from datetime import timedelta
refDate = datetime(1970,1,1,0,0,0)      #FACET refDate is refDate = datetime(1970,1,1,0,0,0)

from TRX_functions import readTRXIntoDictByCallsign


'''
Use the above functions
'''



fileToVisualize = 'TRX_Files/TRX_Columbia_HighRisk004'
filterAircraft = []


# fileToVisualize = 'TRX_tempFACET'
# fileToVisualize = 'TRX_tempAirTOp'
# fileToVisualize = 'TRX_NearFrontRange1Hour'

# fileToVisualize = 'TRX_ZDV_oneHour'
# filterAircraft = ['ASH7048_RAP',
#  'UAL565_DSM',
#  'SCX205_MSP',
#  'UAL593_BOS',
#  'UAL1426_DEN',
#  'SKW6649_DEN',
#  'SKW6702_DEN',
#  'NWA546_DEN',
#  'N701AV_BJC',
#  'VIR44_KLAS',
#  'N998SA_SLN',
#  'SKW6638_FSD',
#  'FFT822_DEN',
#  'JBU489_BOS',
#  'SKW6275_GJT',
#  'AWE491_DEN',
#  'UAL479_LGA',
#  'AWE64_LAS',
#  'QXE4177_DEN',
#  'UAL1229_DTW',
#  'UAL726_DEN',
#  'SKW6585_GEG',
#  'N574P_9U4',
#  'SKW6764_TUL',
#  'ASH7084_DEN',
#  'FFT799_DEN',
#  'UAL521_DFW',
#  'FFT491_DEN',
#  'UAL423_BWI',
#  'DAL1554_SLC',
#  'GLA129_DEN',
#  'N752S_IAH',
#  'DAL505_ATL',
#  'QXE4435_OMA',
#  'FFT129_DEN',
#  'FFT372_DEN',
#  'UAL1143_OMA',
#  'N700LH_TEB',
#  'DAL2059_JFK',
#  'SWA1901_OMA',
#  'SKW6579_BIS',
#  'AWI571_MSN',
#  'EJA609_APA',
#  'UAL1427_MSY',
#  'SKW6636_DEN',
#  'LOF5534_DEN',
#  'FFT859_DEN',
#  'UAL8224_DEN',
#  'UAL256_DEN',
#  'UAL1478_DEN',
#  'SWA1248_MDW',
#  'ASA521_DEN',
#  'SKW6712_DEN',
#  'BAW219_EGLL',
#  'N4403_DEN',
#  'MXA851_KDEN',
#  'UAL649_AUS',
#  'N900MK_STL',
#  'N394B_YUM',
#  'FFT237_DEN',
#  'SKW6271_CPR',
#  'SKW3844_SLC',
#  'N122TP_DEN',
#  'SKW6728_CLE',
#  'SKW6661_BOI',
#  'UEJ200_APA',
#  'N752S_FNL',
#  'EJA703_OQU',
#  'AAL1272_DEN',
#  'NWA106_PHX',
#  'COA228_EWR',
#  'SKW3861_SLC',
#  'UAL755_PHL',
#  'AAL2261_DEN',
#  'ACA1043_YYZ',
#  'ASH7070_DEN',
#  'SKW6699_ELP',
#  'UAL445_MSP',
#  'UAL548_DEN',
#  'FFT811_DEN',
#  'UAL324_SEA',
#  'SKW6796_DEN',
#  'FFT148_DEN',
#  'UAL719_STL',
#  'FFT577_DEN',
#  'GLA797_DEN',
#  'SKW6639_BZN',
#  'UAL270_DEN',
#  'UAL299_PIT',
#  'UAL216_LAX',
#  'SKW6766_SGF',
#  'GLA139_DEN',
#  'JBU295_JFK',
#  'SKW6698_DEN',
#  'AMT4378_DEN',
#  'UAL728_DEN',
#  'UAL537_ORD',
#  'UAL452_DEN',
#  'SKW6645_DEN',
#  'UAL448_DEN',
#  'UAL595_DEN',
#  'GLA731_LBL',
#  'FFT108_DEN',
#  'ASH218_PHX',
#  'USA135_PIT',
#  'MEP811_MKE',
#  'GLA133_DEN',
#  'SKW6640_DEN',
#  'FFT673_MCO',
#  'SKW6670_FAR',
#  'GLA705_DEN',
#  'SKW6735_MSO',
#  'AWI340_DEN',
#  'LYM1011_BFF',
#  'FFT888_KDEN',
#  'AWI577_MKE',
#  'SKW6738_BNA',
#  'SKW6739_DEN',
#  'UAL8225_IAD',
#  'ASH7155_DEN',
#  'UAL251_EWR',
#  'CHQ7682_DEN',
#  'FFT551_DEN',
#  'UAL1126_DEN',
#  'GLA727_DEN',
#  'LYM726_PUB',
#  'ASH7079_DEN',
#  'SKW6756_IND',
#  'UAL1241_DCA',
#  'AAL1513_ORD',
#  'DAL664_DEN',
#  'NWA1937_IND',
#  'FFT683_DEN',
#  'COA1503_LAX',
#  'QXE4331_DEN',
#  'UAL365_CLT',
#  'UAL368_DEN',
#  'UAL338_DEN',
#  'SKW6650_YWG',
#  'GLA758_ALS']



TRX_Storage = readTRXIntoDictByCallsign(fileToVisualize)

# #
# secondsFromRefDate = timedelta(seconds=curTime)
# print 'today is {0}'.format(refDate + secondsFromRefDate)


# So the easiest thing to do is just use an already written python file to visualize
#   the flight tracks.  It won't be an animation, it'll just show the static flight data.
# data2GE.convertTJC(fileNameGE, flatArray, numTimeSteps, numRuns, cutoffNAS = False, maxTimeSteps = 1e10)
# We'll have to hack it a little bit, though, such that numTimeSteps is the number of data points
#   to plot for each trajectory

fileNameGE = 'testFlightTracks.kml'

flatArray       = []  #lat lon alt vx vy vz lat lon alt vx vy vz lat lon ...
numTimeSteps    = []
callSigns       = []

for flightRecord in TRX_Storage.iteritems():
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

import sys
# Points to the python scripts needed from Francisco
friscoFiles = '../../../Prop3Dof/FriscoDebris/pythonFiles/'
sys.path.append(friscoFiles)

import data2GE

# data2GE.convertTJC(fileNameGE, flatArray, numTimeSteps, numRuns = len(numTimeSteps), cutoffNAS = False, maxTimeSteps = 1e10)
data2GE.convertTJCAircraft(fileNameGE, flatArray, numTimeSteps, callSigns, numElementsPerLine = 6)

# import numpy as np
# curArray = np.array(subFlatArray)
# curArray = curArray.reshape((numTimeSteps[0], 6))
#
# for val in curArray[:,1]:
#     print val




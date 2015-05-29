#!/usr/bin/python
'''
Do this for an entire folder of filters and data.

This script first takes a filter and uses it prune down a large TRX file so that it only contains
  the aircraft seen in the filter.  Then, on the reduced TRX, it attempts to keep only the first
  track time seen for each aircraft.  This latter step is necessary because FACET has issues with
  simulations and track updates, so just remove the track updates and let it simulate the flight
  based on the first state vector.

  Author: Thomas J Colvin
'''

fileToFilterOn = "TRX_FrontRange450_TRX_DW2015013119201337.trx"
fileToPrune    = "TRX_DW2015013119201337.trx"

filterPath = "/Users/tcolvin1/Desktop/aiaaSpace/FilteredTRX/"
rawPath    = "/Users/tcolvin1/Desktop/aiaaSpace/RawTRX/"
outputPath =

# First off, make sure the filter and the file match up.  Last thing before .trx is the salient info.
filterBaseName = fileToFilterOn.split('.')[0].split('_')[-1]
rawBaseName = fileToPrune.split('.')[0].split('_')[-1]
if filterBaseName != rawBaseName:
    print "ERROR!  {0} != {1]".format(filterBaseName, rawBaseName)
    raise AssertionError

from os.path import abspath
import subprocess
callString = "0} {1} {2} {3}".format(abspath(filterTRX.py), filterPath+fileToFilterOn, rawPath+fileToPrune, "testOutputTRX")
subprocess.call(callString)

callString = "./filterTRX.py {0} {1} {2}".format(filterPath+fileToFilterOn, rawPath+fileToPrune, "testOutputTRX")

callString = "python {0} {1} {2} {3}".format(abspath("filterTRX.py"), filterPath+fileToFilterOn, rawPath+fileToPrune, "testOutputTRX")
# subprocess.Popen(callString, shell=True)
# subprocess.call(callString, shell=True)

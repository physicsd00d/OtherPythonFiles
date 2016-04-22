'''
Read in all the custom FACET output files and save them as pickles for fast subsequent processing.
"Custom" files must end in .cst
"Filter" files must end in .flt
The file name convention is ###_anythingYouWant.cst, ###_anythingYouWant.flt
The numbers (or text) that precede the first underscore will become the name of the pickle ###.pkl
'''

''' This gets the function arguments '''
import sys
import os.path

print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)

if len(sys.argv) != 2:
    print "   Error: need exactly 1 arguments after file name"
    print "          inputFolderName"
    sys.exit()

# Unpack Inputs
inputFolderName = sys.argv[1]

# Check that inputs exist
if not os.path.isdir(inputFolderName):
    print "   Error: {0} does not exist".format(inputFolderName)
    sys.exit()


import glob
inputFilters = glob.glob1(inputFolderName, "*.flt")
inputCustoms = glob.glob1(inputFolderName, "*.cst")
print inputFilters
print inputCustoms

## Check that the .cst and .flt files match up
if len(inputFilters) == len(inputCustoms):
    for ix in range(len(inputFilters)):
        curFlt = inputCustoms[ix].split('_')[0]
        curCst = inputFilters[ix].split('_')[0]
        if curFlt != curCst:
            print "  ERROR: {0} vs {1}".format(inputCustoms[ix], inputFilters[ix])
            sys.exit()
else:
    print "  ERROR: Different Lengths \n{0} \n{1}".format(inputCustoms, inputFilters)
    sys.exit()


''' Now start the actual processing work '''
from customFunctions import *

import pickle

for (curFilter, curCustom) in zip(inputFilters, inputCustoms):
    acFilter             = readFilter(inputFolderName + "/" + curFilter)
    acDict, sectorDict   = readCustomFacetFile(inputFolderName + "/" + curCustom)

    curOutFile = curFilter.split('_')[0] + ".pkl"
    pickle.dump([acDict, acFilter], open(curOutFile,'wb'))

    print "Just wrote {0}".format(curOutFile)

sys.exit()




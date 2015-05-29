# '''
# Take a list of CallSigns and remove every track update that comes from an AC with that callsign
# '''


function pruneTRXFromList(inFileName::String, filterDict::Dict, outFileName::String, deltaSeconds = 0)
  # Starts by eliminating every single aircraft (shouldPrint = False), but if an AC matches a filter,
  #   then it will be allowed through.

  print("Pruning for " * outFileName)
  sortedKeys = sort(collect(keys(filterDict)))
  plainCallsigns = [split(curFlight, '_')[1] for curFlight in sortedKeys]

  # Keys are TRACK_TIMES, each value will be the strings (concatenated together) that are to be printed out
  TRX_Storage = Dict()

  printOkay = true
  if length(outFileName) == 0
    printOkay = false
  end

  inputFile = open(inFileName, "r")

  # This will hold the information as we run through the lines until it's time to save it to the dictionary
  curTime = -1
  curFPLine = ""
  curTrackLine = ""
  shouldPrint = true
  curCallSign = []    # Scope this here

  for line in eachline(inputFile)
    key = split(strip(line))

    if length(key) > 0
      #println(key)
      #println(length(key))

      if key[1] == "TRACK_TIME"
        # Indicates progress

        curTimeInt = int(key[2]) + deltaSeconds
        curTime = string(curTimeInt)

      elseif key[1] == "TRACK"
        curCallSign = key[2]

#         shouldPrint = (curCallSign in plainCallsigns)
#         shouldPrint = true
        curTrackLine = line

      elseif key[1] == "FP_ROUTE"
        curFPLine = line

        # At this point we need to check for the departure Airport
#         if shouldPrint
          #               depAirport = key[1].split('.')[0]
          depAirport = split(key[2],".")[1]
          sign_dep = "$(curCallSign)_$depAirport"

          if !(sign_dep in sortedKeys)
            shouldPrint = false
          elseif !(curTimeInt in filterDict[sign_dep])
            shouldPrint = false
          end
#         end


        # At this point, we will be done with the specific aircraf that we're looking at so save it if it's good
        if shouldPrint
          # Create this time record if necessary
          if !haskey(TRX_Storage, curTime)
            TRX_Storage[curTime] = ""
          end

          # Add it to the queue for printing
          TRX_Storage[curTime] = TRX_Storage[curTime] * curTrackLine
          TRX_Storage[curTime] = TRX_Storage[curTime] * curFPLine * "\n"

        else
          # Reset
          shouldPrint = true
        end

      elseif key[1][1] == "#"
        # print 'COMMENT'
      else
        print("pruneTRXFromList: NewLine! This should not have been hit!\n")
        print(key)
        error()
      end
    end
  end

  close(inputFile) # It's likely that the output file will be the same file, so make sure to close this first.

  if printOkay
    # # Now write everything to file
    outFile = open(outFileName,"w")

    for key in sort(collect(keys(TRX_Storage)))
      if length(TRX_Storage[key]) > 0
        write(outFile, "TRACK_TIME " * key * "\n")
        write(outFile, TRX_Storage[key])
      end
    end

    close(outFile)
  end
end


cd(dirname(@__FILE__))   # Set pwd to location of this file
ENV["PYTHONPATH"] = pwd()   # Tell python where to look for modules
using PyCall
@pyimport TRX_functions
readTRXIntoDictByCallsign = TRX_functions.readTRXIntoDictByCallsign


filterPath = "/Users/tcolvin1/Desktop/aiaaSpace/FilteredTRX/"
rawPath    = "/Users/tcolvin1/Desktop/aiaaSpace/RawTRX/"

fileToFilterOn = filterPath * "TRX_FrontRange450_TRX_DW2015013119201337.trx"
# fileToPrune    = rawPath * "TRX_DW2015013119201337.trx"
fileToPrune    = rawPath * "testRaw1337.trx"


# from TRX_functions import readTRXIntoDictByCallsign
# from TRX_functions import pruneTRXFromList

tempOutFileName = "TempTRX"   # This is good for debugging
# tempOutFileName = outputFile  # This should be okay if everything is working...

# Just load the entire TRX, since it's been filtered, it should be relatively small
TRX_Storage = readTRXIntoDictByCallsign(fileToFilterOn)
sortedKeys = sort(collect(keys(TRX_Storage)))


curTimes = TRX_Storage[sortedKeys[1]][:,1]
jumpIXs = find(diff(curTimes)/60 .> 5)
keepIXs = unique(vcat([1], jumpIXs+1, [length(curTimes)]))
curTimes[keepIXs]

(936000/388. * 0.75)/60   #minutes.  I don't think it took 30 minutes in python!

# jumpIXs are the LAST times before the jump.
# Have to add 1 to index to get the first time of the next flight.

# So will want to keep times for all of the jumps, the first time seen and the last time seen
filterDict = Dict()

for curCallSign in sortedKeys
  curTimes = TRX_Storage[curCallSign][:,1]
  jumpIXs = find(diff(curTimes)/60 .> 5)
  keepIXs = unique(vcat([1], jumpIXs+1, [length(curTimes)]))
  filterDict[curCallSign] = curTimes[keepIXs]

end

filterDict

@time pruneTRXFromList(fileToPrune, filterDict, tempOutFileName)
@profile pruneTRXFromList(fileToPrune, filterDict, tempOutFileName)
Profile.print()







cd(dirname(@__FILE__))    # Set the pwd to the directory that contains this file
push!(LOAD_PATH, pwd())   # Allow me to define modules and "using" them from this folder
# push!(LOAD_PATH, abspath("./includeFiles"))

inFileName = "../AirwayData/ENHIGH.DAT"
altLevel = 180.



inFile = open(inFileName, "r")

routeDict = Dict()
curRouteName = ""
keys = ""  #temp, delete this
for line in eachline(inFile)

#   line = lstrip(line)        # Strip out the new-line character and any trailing spaces
  # Will never care about the first two characters, delete them
  line = line[3:end]
  line = replace(line, r"\s+", " ")
  keys = split(line, " ")    # Split based on spaces

  # Skip all the (basically) empty lines
  if keys[1] == "0"
    continue
  end

  # Have we found a new route yet?
  if keys[2] == "ROUTE"
    # This is a new route.  Create the data structure
    curRouteName = join(keys[1:4], " ")
    println(curRouteName)
    routeDict[curRouteName] = zeros(3,0)  # This is an empty matrix with three columns
                                          #[lat lon fl]

    # Now trash the next three lines
    for trashIX = 1:3
      readline(inFile)
    end
    continue
  end

  # We haven't yet seen a route yet, so still sifting through the preamble.  Skip it.
  if length(curRouteName) == 0
    continue
  end

  # If we've made it here, then we're reading in a route.
  if length(keys) > 4
    # There are some lines that lack lat/lon data but that aren't total garbage.  Just skip them.
#     println(float64(keys[3:8]))
#     println(routeDict[curRouteName])
#     println(keys)
    curLat = convertDegMinSecToDecimal(float64(keys[3:5]))
    curLon = convertDegMinSecToDecimal(float64(keys[6:8]))
    routeDict[curRouteName] = hcat(routeDict[curRouteName],[curLat, -curLon, altLevel])
#     routeDict[curRouteName] = vcat(routeDict[curRouteName], float64(keys[3:8]'))
  end

end

close(inFile)

routeDict
curRouteName
routeDict[curRouteName]

include("googleEarth.jl")
makeLineString(routeDict[curRouteName])


for (key, obj) in routeDict
  println(key)
end


staticBoxes("testAirways.kml", routeDict, 2.)


#   function makeLineString(llfl)
#     lineString = ["""    <LineString>\n""",
#                   """      <altitudeMode>relativeToGround</altitudeMode>\n""",
#                   """      <coordinates>\n""",
#                   "", # THIS LINE MUST CONTAIN THE DATA!!!
#                   """      </coordinates>\n""",
#                   """    </LineString>\n"""]

#     #   lineStr = ""
#     curAlt = llfl[3,1]
#     for (curLat, curLon) in zip(llfl[1,:], llfl[2,:]+360.)
#       lineString[4] *= "$curLon,$curLat,$curAlt\n"
#     end

#     lineString
#   end

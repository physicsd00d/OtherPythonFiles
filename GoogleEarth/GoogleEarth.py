def convertTJCAircraft(fileNameGE, flatArray, numTimeSteps, callSigns, numElementsPerLine):
    # I expect the Lat/Lon/Alt in flatArray to be in Deg / Deg / M, just what GE expects

    # Make this an input!!!!
#    numElementsPerLine = 6

    numRuns = len(numTimeSteps)

    #fileNameGE = 'GE.kml'
    outFileGE = open(fileNameGE,'w')

    line1GE  = '<?xml version="1.0" encoding="UTF-8"?>\n'
    line2GE  = '<kml xmlns="http://www.opengis.net/kml/2.2">\n'
    line3GE  = ' <Document>\n'
    line4GE  = '  <Style id="style1">\n'
    line5GE  = '   <LineStyle>\n'
    line6GE  = '    <colorMode>random</colorMode>\n'
    line7GE  = '    <width>4</width>\n'
    line8GE  = '   </LineStyle>\n'
    line9GE  = '  </Style>\n'
    line10GE = ' <name>Debris-Path</name>\n\n'
    outFileGE.write(line1GE)
    outFileGE.write(line2GE)
    outFileGE.write(line3GE)
    outFileGE.write(line4GE)
    outFileGE.write(line5GE)
    outFileGE.write(line6GE)
    outFileGE.write(line7GE)
    outFileGE.write(line8GE)
    outFileGE.write(line9GE)
    outFileGE.write(line10GE)


    lineCounter = 0
    for curRun in range(0,numRuns):

        line1GE = '  <Placemark>\n'
        line2GE = '   <name>' + callSigns[curRun] + '</name>\n'
        line3GE = '   <styleUrl>#style1</styleUrl>\n'
        line4GE = '   <MultiGeometry>\n'
        line5GE = '    <LineString>\n'
        line6GE = '      <altitudeMode>relativeToGround</altitudeMode>\n'
        line7GE = '      <coordinates>\n'

        outFileGE.write(line1GE)
        outFileGE.write(line2GE)
        outFileGE.write(line3GE)
        outFileGE.write(line4GE)
        outFileGE.write(line5GE)
        outFileGE.write(line6GE)
        outFileGE.write(line7GE)

        for tx in range(numTimeSteps[curRun]):
            lat = flatArray[lineCounter]
            lon = flatArray[lineCounter+1]
            alt = flatArray[lineCounter+2]
            lineCounter += numElementsPerLine

            newLine = str(lon)+','+str(lat)+','+str(alt)+'\n'
            outFileGE.write(newLine)

        line1GE = '    </coordinates>\n'
        line2GE = '   </LineString>\n'
        line3GE = '  </MultiGeometry>\n'
        line4GE = ' </Placemark>\n\n'

        outFileGE.write(line1GE)
        outFileGE.write(line2GE)
        outFileGE.write(line3GE)
        outFileGE.write(line4GE)


    line1GE = '  </Document>\n'
    line2GE = '</kml>'


    outFileGE.write(line1GE)
    outFileGE.write(line2GE)

    outFileGE.close()




def convertTJCAircraftRedGreen(fileNameGE, flatArray, numTimeSteps, callSigns, isRed, numElementsPerLine):
    # I expect the Lat/Lon/Alt in flatArray to be in Deg / Deg / M, just what GE expects

    # Make this an input!!!!
    #    numElementsPerLine = 6

    numRuns = len(numTimeSteps)

    #fileNameGE = 'GE.kml'
    outFileGE = open(fileNameGE,'w')

#    line1GE  = '<?xml version="1.0" encoding="UTF-8"?>\n'
#    line2GE  = '<kml xmlns="http://www.opengis.net/kml/2.2">\n'
#    line3GE  = ' <Document>\n'
#    line4GE  = '  <Style id="style1">\n'
#    line5GE  = '   <LineStyle>\n'
#    line6GE  = '    <colorMode>random</colorMode>\n'
#    line7GE  = '    <width>4</width>\n'
#    line8GE  = '   </LineStyle>\n'
#    line9GE  = '  </Style>\n'
#    line10GE = ' <name>Debris-Path</name>\n\n'
#    outFileGE.write(line1GE)
#    outFileGE.write(line2GE)
#    outFileGE.write(line3GE)
#    outFileGE.write(line4GE)
#    outFileGE.write(line5GE)
#    outFileGE.write(line6GE)
#    outFileGE.write(line7GE)
#    outFileGE.write(line8GE)
#    outFileGE.write(line9GE)
#    outFileGE.write(line10GE)

    preamble = ['<?xml version="1.0" encoding="UTF-8"?>\n',
                '<kml xmlns="http://www.opengis.net/kml/2.2">\n',
                ' <Document>\n',
                '  <Style id="styleRed">\n',
                '   <LineStyle>\n',
                '    <color>ff0000ff</color>\n',
                '    <colorMode>normal</colorMode>\n',
                '    <width>4</width>\n',
                '   </LineStyle>\n',
                '  </Style>\n',
                '  <Style id="styleGreen">\n',
                '   <LineStyle>\n',
                '    <color>ff00ff00</color>\n',
                '    <colorMode>normal</colorMode>\n',
                '    <width>4</width>\n',
                '   </LineStyle>\n',
                '  </Style>\n',
                ' <name>Debris-Path</name>\n\n']

    for line in preamble:
        outFileGE.write(line)

    lineCounter = 0
    for curRun in range(0,numRuns):

        curStyle = 'styleRed'
        if not isRed[curRun]:
            curStyle = 'styleGreen'

        line1GE = '  <Placemark>\n'
        line2GE = '   <name>' + callSigns[curRun] + '</name>\n'
        line3GE = '   <styleUrl>#' + curStyle + '</styleUrl>\n'
        line4GE = '   <MultiGeometry>\n'
        line5GE = '    <LineString>\n'
        line6GE = '      <altitudeMode>relativeToGround</altitudeMode>\n'
        line7GE = '      <coordinates>\n'

        outFileGE.write(line1GE)
        outFileGE.write(line2GE)
        outFileGE.write(line3GE)
        outFileGE.write(line4GE)
        outFileGE.write(line5GE)
        outFileGE.write(line6GE)
        outFileGE.write(line7GE)

        for tx in range(numTimeSteps[curRun]):
            lat = flatArray[lineCounter]
            lon = flatArray[lineCounter+1]
            alt = flatArray[lineCounter+2]
            lineCounter += numElementsPerLine

            newLine = str(lon)+','+str(lat)+','+str(alt)+'\n'
            outFileGE.write(newLine)

        line1GE = '    </coordinates>\n'
        line2GE = '   </LineString>\n'
        line3GE = '  </MultiGeometry>\n'
        line4GE = ' </Placemark>\n\n'

        outFileGE.write(line1GE)
        outFileGE.write(line2GE)
        outFileGE.write(line3GE)
        outFileGE.write(line4GE)


    line1GE = '  </Document>\n'
    line2GE = '</kml>'


    outFileGE.write(line1GE)
    outFileGE.write(line2GE)

    outFileGE.close()
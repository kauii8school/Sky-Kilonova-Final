import subprocess
import sys
sys.path.insert(0, "/home/n/Documents/Research/GW170817-Milky-Way/DataVisualization/Graphs")
sys.path.insert(0, "/home/n/Documents/Research/GW170817-Milky-Way/Dynamic Range/Data")
from GraphicalFunctions import *
from GrayScale import camResponse
from Star import GW170817
from Tracking import findMarker
import random
#Note in order to not have this cluttered you MUST run this file's working directory to : /home/user/Documents/Research/GW170817-Milky-Way/Natron/NatronScriptsr

#PARAMS
shutterSpeed = 1 #Second

def photometryToNatronTapperness(phot, shutterSpeed):
    return .3 + phot * shutterSpeed  * 162.2341235123333

def photometryToNatronBrightness(phot):
    return 100

def photometryToBrightnesses(phot, shutterSpeed):
    tapperness = .3 + phot * shutterSpeed  * 162.2341235123333
    brightness = (phot * 70000)
    causticGhostSize = phot * 3000 + random.uniform(-1, 1)
    globalSize = .05
    mirisSize = phot * 5700 + random.uniform(-2, 2)
    mixValue = .5
    if mirisSize < 0:
        mirisSize = 0

    if causticGhostSize < 0:
        causticGhostSize = 0

    return tapperness, brightness, causticGhostSize, globalSize, mirisSize, mixValue

sunRayCount = 15
print(len(GW170817.interpolatedColorList))
for i in [0, 41, 152]: #[20, 0, 41, 152, 263, 374, 485, 596, 707]: #range(0, len(GW170817.interpolatedColorList)):

    #rgb = tintzGB((rgb), 1)
    rgb = GW170817.interpolatedColorList[i]
    apMag = float(GW170817.interpolatedBandDict["V"][1][i])
    print(i)

    varboxFile = open("/home/n/Documents/Research/GW170817-Milky-Way/Natron/natron-plugins/Lens_Flare_Presets/Flare_ScifiLite/VarBox.py", "w")
    r = str(rgb[0])
    g = str(rgb[1])
    b = str(rgb[2])


    # #No foreground no plot
    # includeStar = True
    # includePlot = False
    # staticBackground = False
    # backgroundFileName = "StellBack"
    # name = "StellBack"
    # posX = 670 #921 for stellarium
    # posY = 750 #528 for stellarium
    # card1AxisTranslate = 0 #For no plot
    # card2AxisTranslate = -.0115
    # xText = 1740.0
    # yText = 1070
    # dimensions = (19.2, 3.5)
    # fileDimensions = "1920x1080" #No plot

    # #No foreground plot
    # includeStar = True
    # includePlot = True
    # staticBackground = False
    # backgroundFileName = "StellBack"
    # name = "StellBack"
    # posX = 670 #921 for stellarium
    # posY = 750 #528 for stellarium
    # card1AxisTranslate = .1625 #For no plot
    # card2AxisTranslate = -.0115
    # xText = 1740.0
    # yText = 1070
    # dimensions = (19.2, 3.5)
    # fileDimensions = "1920x1380"

    # #Perth no plot
    # includeStar = True
    # includePlot = False
    # staticBackground = False
    # backgroundFileName = "Perth"
    # name = "Perth"
    # posX = 670 #921 for stellarium
    # posY = 1050 #528 for stellarium
    # card1AxisTranslate = 0 #For no plot
    # card2AxisTranslate = -.0115
    # xText = 1870.0
    # yText = 1355.0
    # dimensions = (19.2, 3.5)
    # fileDimensions = "2048x1365" #No plot

    # #Perth plot
    # includeStar = True
    # includePlot = True
    # staticBackground = False
    # backgroundFileName = "Perth"
    # name = "Perth"
    # posX = 670 #921 for stellarium
    # posY = 1050 #528 for stellarium
    # card1AxisTranslate = .165 #For no plot
    # card2AxisTranslate = -.006
    # xText = 1870.0
    # yText = 1355.0
    # dimensions = (20.5, 3.5)
    # fileDimensions = "2048x1700" #No plot

    # #Manhattan no plot
    # includeStar = True
    # includePlot = False
    # staticBackground = False
    # backgroundFileName = "Manhattan"
    # name = "Manhattan"
    # posX = 570 #921 for stellarium
    # posY = 550 #528 for stellarium
    # card1AxisTranslate = 0 #For no plot
    # card2AxisTranslate = -.0115
    # xText = 1740.0
    # yText = 680.0
    # dimensions = (19.2, 3.5)
    # fileDimensions = "1920x680" #No plot

    # #Manhattan Settings  Plot 
    # includePlot = True
    # includeStar = True
    # staticBackground = False
    # backgroundFileName = "Manhattan2"
    # name = "Manhattan"
    # posX = 570 #921 for stellarium
    # posY = 550 #528 for stellarium
    # card1AxisTranslate = .1625
    # card2AxisTranslate = -.0115
    # xText = 1740.0
    # yText = 750.0
    # dimensions = (19.2, 3.5)
    # fileDimensions = "1920x1080" #For plot also

    # #Statue of Liberty 2 no plot
    # includeStar = True
    # includePlot = False
    # staticBackground = False
    # backgroundFileName = "StatueOfLiberty"
    # name = "StatueOfLiberty"
    # posX = 1200 #921 for stellarium
    # posY = 900 #528 for stellarium
    # card1AxisTranslate = 0 #For no plot
    # card2AxisTranslate = -.0115
    # xText = 1740.0
    # yText = 1270.0
    # dimensions = (19.2, 3.5)
    # fileDimensions = "1920x1280" #No plot

    # #Statue of Liberty 3 no plot
    # includeStar = True
    # includePlot = False
    # staticBackground = False
    # backgroundFileName = "StatueOfLiberty3"
    # name = "StatueOfLiberty3"
    # posX = 500 #921 for stellarium
    # posY = 900 #528 for stellarium
    # card1AxisTranslate = 0 #For no plot
    # card2AxisTranslate = -.0115
    # xText = 540
    # yText = 1070.0
    # dimensions = (19.2, 3.5)
    # fileDimensions = "719x1080" #No plot

    #Statue of Liberty 4 no plot
    includeStar = True
    includePlot = False
    staticBackground = False
    backgroundFileName = "StatueOfLiberty4"
    name = "StatueOfLiberty4"
    posX = 500 #921 for stellarium
    posY = 900 #528 for stellarium
    card1AxisTranslate = 0 #For no plot
    card2AxisTranslate = -.0115
    xText = 540
    yText = 1070.0
    dimensions = (19.2, 3.5)
    fileDimensions = "719x1080" #No plot

    # #Statue of Manhattan 3 no plot
    # includeStar = True
    # includePlot = False
    # staticBackground = False
    # backgroundFileName = "Manhattan3"
    # name = "Manhattan3"
    # posX = 1400#921 for stellarium
    # posY = 900 #528 for stellarium
    # card1AxisTranslate = 0 #For no plot
    # card2AxisTranslate = -.0115
    # xText = 1740
    # yText = 1280
    # dimensions = (19.2, 3.5)
    # fileDimensions = "1920x1278" #No plot

    # #Fort Knox Settings  Plot 
    # includePlot = True
    # includeStar = True
    # staticBackground = True
    # backgroundFileName = "FortKnox"
    # name = "FortKnox"
    # posX = 770 #921 for stellarium
    # posY = 690 #528 for stellarium
    # card1AxisTranslate = .1885
    # card2AxisTranslate = -.013
    # xText = 1020.0
    # yText = 780.0
    # dimensions = (12, 2.5)
    # fileDimensions = "1200x1015" #For plot also

    # #Fort Knox Settings No Plot 
    # includePlot = False 
    # includeStar = True
    # staticBackground = True
    # backgroundFileName = "FortKnox"
    # name = "FortKnox"
    # posX = 770 #921 for stellarium
    # posY = 690 #528 for stellarium
    # card1AxisTranslate = 0
    # card2AxisTranslate = -.013
    # xText = 1020.0
    # yText = 780.0
    # dimensions = (12, 2.5)
    # fileDimensions = "1200x791" 

    # # #Liberty settings no plot
    # includePlot = False
    # includeStar = True
    # staticBackground = True
    # backgroundFileName = "Liberty"
    # name = "Liberty"
    # posX = 1370 #921 for stellarium
    # posY = 950 #528 for stellarium
    # card1AxisTranslate = 0
    # card2AxisTranslate = -.0115
    # xText = 1825.0
    # yText = 1330.0
    # dimensions = (19.2, 3.5)
    # fileDimensions = "2000x1333" #For plot also

    # # #Liberty settings no plot
    # includePlot = True
    # includeStar = True
    # staticBackground = True
    # backgroundFileName = "Liberty"
    # name = "Liberty"
    # posX = 1370 #921 for stellarium
    # posY = 950 #528 for stellarium
    # card1AxisTranslate = .165
    # card2AxisTranslate = -.009
    # xText = 1825.0
    # yText = 1330.0
    # dimensions = (20, 3.5)
    # fileDimensions = "2000x1660" #For plot also

    # #Century Tower Settings
    # includeStar = True
    # includePlot = True
    # staticBackground = True
    # backgroundFileName = "CenturyTower3"
    # name = "Century"
    # posX = 270 #921 for stellarium
    # posY = 700 #528 for stellarium
    # card1AxisTranslate = .3325
    # card2AxisTranslate = -.02
    # xText = 590
    # yText = 900
    # dimensions = (7.7, 2.7)
    # fileDimensions = "763x1150"

    # #Century Tower Settings no plot
    # includePlot = False
    # staticBackground = False
    # backgroundFileName = "CenturyTower3"
    # name = "Century"
    # posX = 270 #921 for stellarium
    # posY = 700 #528 for stellarium
    # card1AxisTranslate = 0
    # card2AxisTranslate = -.02
    # xText = 590
    # yText = 900
    # dimensions = (7.7, 2.7)
    # fileDimensions = "763x900"

    # if staticBackground == False:
    #     #Finding position of merger
    #     posX, posY = findMarker(i)
    #     if (posX, posY) == (None, None):
    #         includeStar = False
    #     else:
    #         includeStar = True

    #Brightness vars
    sunHardness = .01 #Controlls how wide sun is 
    illuminance = apMagToIlluminance(apMag)
    sunTapperness = photometryToNatronTapperness(illuminance, shutterSpeed)
    sunRayCount = sunRayCount + random.randint(-1, 1)
    sunRayDepth = .123
    starBrightness = photometryToNatronBrightness(illuminance)
    time = GW170817.interpolatedTimeList[i]
    timeSinceMerger = timeMJDToSinceEvent(57982.36180556, time)
    plotFileName = "Plot{0:03d}".format(i)
    includeCausticGhosts = True
    includeText = True
    causticGhostSize = 8
    globalSize = .05
    mirisSize = 10
    mixValue = .5


    #Video vars
    timeLimit = 7 #days

    if int(timeSinceMerger[0]) > timeLimit:
        exit()

    GW170817.plotPhotometryInterpolated()
    GW170817.pointPlotPhotometry(inputIndex = i)
    GW170817.savePlot("/home/n/Documents/Research/GW170817-Milky-Way/Natron/ReadImages/Plots/", plotFileName, dimensions, name = name, xlim = (57982.36180556, 57990))

    filename = "/home/n/Documents/Research/GW170817-Milky-Way/Natron/WriteImages/Image{0:03}.png".format(i)
    if includeStar == True:
        sunTapperness, starBrightness, causticGhostSize, globalSize, mirisSize, mixValue = photometryToBrightnesses(illuminance, shutterSpeed)
        #print(sunTapperness, starBrightness, causticGhostSize, globalSize, mirisSize, mixValue)
        #0.8157751891139848 100 9.969496895871496 0.05 16.848714176009818 0.5
        #Creating a varbox in Flare_ScifiLIte so that Flare_SciFiLite.py can read variables from there and use them in the video
        varboxFile.write("globalRed = {}\n".format(r))
        varboxFile.write("globalGreen = {}\n".format(g))
        varboxFile.write("globalBlue =  {}\n".format(b))
        varboxFile.write("sunHardness = {}\n".format(sunHardness))
        varboxFile.write("sunTapperness = {}\n".format(sunTapperness))
        varboxFile.write("starBrightness = {}\n".format(starBrightness))
        varboxFile.write("sunRayCount = {}\n".format(sunRayCount))
        varboxFile.write("sunRayDepth = {}\n".format(sunRayDepth))
        varboxFile.write("includeCausticGhosts = {}\n".format(includeCausticGhosts))
        varboxFile.write("posX =  {}\n".format(posX))
        varboxFile.write("posY = {}\n".format(posY))
        varboxFile.write("causticGhostSize = {}\n".format(causticGhostSize))
        varboxFile.write("globalScale = {}\n".format(globalSize))
        varboxFile.write("mirisSize = {}\n".format(mirisSize))
        varboxFile.close()

    #Creating a varbox for CreateStar.py
    CreateStarVarBoxFile = open("/home/n/Documents/Research/GW170817-Milky-Way/Natron/NatronScripts/CreateStarVarBox.py", "w")
    CreateStarVarBoxFile.write("timeText = '{}'\n".format(timeSinceMerger))
    CreateStarVarBoxFile.write("skyFileName = \"{}\"\n".format("frame_{0:03}".format(i)))
    CreateStarVarBoxFile.write("backgroundFileName = \"{}\"\n".format(backgroundFileName))
    CreateStarVarBoxFile.write("plotFileName = \"{}\"\n".format(plotFileName))
    CreateStarVarBoxFile.write("mixValue = {}\n".format(mixValue))
    CreateStarVarBoxFile.write("includeText = {}\n".format(includeText))
    CreateStarVarBoxFile.write("includeStar = {}\n".format(includeStar))
    CreateStarVarBoxFile.write("includePlot = {}\n".format(includePlot))
    CreateStarVarBoxFile.write("staticBackground = {}\n".format(staticBackground))
    CreateStarVarBoxFile.write("card1AxisTranslate = {}\n".format(card1AxisTranslate))
    CreateStarVarBoxFile.write("card2AxisTranslate = {}\n".format(card2AxisTranslate))
    CreateStarVarBoxFile.write("xText = {}\n".format(xText))
    CreateStarVarBoxFile.write("yText = {}\n".format(yText))
    CreateStarVarBoxFile.write("fileDimensions = '{}'\n".format(fileDimensions))
    CreateStarVarBoxFile.close()

    subprocess.call('ls', shell = True)
    subprocess.call(['NatronRenderer', 'CreateStar.py', '-w', 'MyWriter', '1', filename])
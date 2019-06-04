import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import matplotlib as mpl
import sys
from astropy.time import Time
from scipy import interpolate 
from scipy.signal import savgol_filter

ciePath = "/home/n/Documents/Research/GW170817-Milky-Way/CIE"
graphPath = "/home/n/Documents/Research/GW170817-Milky-Way/DataVisualization/Graphs/OldStuff"
sys.path.insert(0, graphPath)
sys.path.insert(0, ciePath)
from ColorSystem import cs_hdtv
from Spectra import GW170817SpectraFull
from GraphicalFunctions import *
spectraList = GW170817SpectraFull.spectraList




timeList, pointsR, pointsG, pointsB = [], [], [], []
for spectra in spectraList:
    rgbTrio = findRGBColor(spectra, cs_hdtv)
    timeList.append(spectra[0])
    pointsR.append(rgbTrio[0])
    pointsG.append(rgbTrio[1])
    pointsB.append(rgbTrio[2])

averagedRPoints, averagedGPoints, averagedBPoints, averagedTimePoints = [], [], [], []
#Averaging points that are very close
averagedRPoints, averagedGPoints, averagedBPoints, averagedTimePoints = pointAveraging(timeList, pointsR, pointsG, pointsB)

# for i in range(0, len(averagedBPoints)):
#     print(averagedTimePoints[i], averagedRPoints[i], averagedGPoints[i], averagedBPoints[i])

# print('----------')
# for i, time in enumerate(timeList):
#     print(timeList[i], pointsR[i], pointsG[i], pointsB[i])

#Creates iterpolation functions
print(averagedTimePoints)
rInterpolated = interpolate.interp1d(averagedTimePoints, averagedRPoints)
gInterpolated = interpolate.interp1d(averagedTimePoints, averagedGPoints)
bInterpolated = interpolate.interp1d(averagedTimePoints, averagedBPoints)

timeInterpolatedList, rgbListInterpolated = recreateXYZ(1000, rInterpolated, gInterpolated, bInterpolated)

#Interpolation NOTE look into different interpolators 
rListInterpolated = [rgbTrio[0] for rgbTrio in rgbListInterpolated]
gListInterpolated = [rgbTrio[1] for rgbTrio in rgbListInterpolated]
bListInterpolated = [rgbTrio[2] for rgbTrio in rgbListInterpolated]

#Smoothing see https://en.wikipedia.org/wiki/Savitzky%E2%80%93Golay_filter
smoothedR = savgol_filter(rListInterpolated, 51, 3)
smoothedG = savgol_filter(gListInterpolated, 51, 3)
smoothedB = savgol_filter(bListInterpolated, 51, 3)

timeInterpolatedListUTC = []
for time in timeInterpolatedList: #Reformatting time
    mjdTime = Time(time, format='mjd')
    utcTime = mjdTime.iso
    timeInterpolatedListUTC.append(utcTime)

#This is kind of weird becausee you think i would include in spectra but actually you can't because you have to create the entire spectrum first beffore interpolating

rgbList = []
for time, r, g, b in zip(timeInterpolatedList, smoothedR, smoothedG, smoothedB): #Plots background color spectrum
    #Sometimes the Savgol filter makes the rgb over 1 so i will just take it as 1 here as it is usually only 1.00001 or something
    rgbList.append((r, g, b))
    plt.bar([time], [1.05], color = [normalizeRGB(r), normalizeRGB(g), normalizeRGB(b)], zorder = 1)


timeInterpolatedList = list(timeInterpolatedList)
# plt.plot(timeInterpolatedList, rListInterpolated, label='Red', color = [1, 0, 0])
# plt.plot(timeInterpolatedList, gListInterpolated, label='Green', color = [0, 1, 0])
# plt.plot(timeInterpolatedList, bListInterpolated, label='Blue', color = [0, 0, 1]) 
plt.plot(timeInterpolatedList, smoothedR, color = [.5, 0, 0])
plt.plot(timeInterpolatedList, smoothedG, color = [0, .5, 0])
plt.plot(timeInterpolatedList, smoothedB, color = [0, 0, .5])

plt.xticks([57983 + i for i in range(0, 10)], [i for i in range(0, 10)])
# plt.scatter(averagedTimePoints, averagedRPoints, color = 'r', zorder = 10)
# plt.scatter(averagedTimePoints, averagedGPoints, color = 'g', zorder = 10)
# plt.scatter(averagedTimePoints, averagedBPoints, color = 'b', zorder = 10)
plt.xlim(timeList[0], timeList[len(timeList) - 1])
plt.ylim(0, 1.05)
plt.xlabel('Time (Days)')
plt.ylabel("RGB Value")
plt.show()

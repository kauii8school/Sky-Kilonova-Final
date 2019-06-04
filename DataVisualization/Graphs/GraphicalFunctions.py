import numpy as np
import sys
import os
import math
from scipy.integrate import simps
import astropy
cwd = os.getcwd()

def limTrimmer(data, lowerWaveLim, upperWaveLim): #Trims everything that isn't within the limits
    waveLengthList = data[0]
    fluxList = data[1]
    newWavList, newFluxList = [], []
    for i, waveLength in enumerate(waveLengthList):
        if not(waveLength <= lowerWaveLim or waveLength >= upperWaveLim): 
            newWavList.append(waveLength)
            newFluxList.append(fluxList[i])

    return (newWavList, newFluxList)

def findRGBColor(spectra, cs_hdtv): #Finds color givin a spectra that is wavelength list and flux list

    wavelengthList, fluxList = spectra[1][0], spectra[1][1]
    wavelengthList = [wavelength / 10 for wavelength in wavelengthList] #Convert to nm
    trimmedTuple = limTrimmer((wavelengthList, fluxList), 380, 780) #Trims to fit limits
    wavelengthList, fluxArray = list(trimmedTuple[0]), np.array(trimmedTuple[1]) #Sets new wavelength and flux list
    cs_hdtv.cmfCreation(wavelengthList) #creates matrix for cmf
    graphColorRGB = cs_hdtv.spec_to_rgb(fluxArray)
    return graphColorRGB

def recreateXYZ(numTimePoints, xFunc, yFunc, zFunc): #Returns list with interpolated xyz values 

    timeList = np.linspace(57983, 57992, numTimePoints) #Min to max time 
    retList = []

    for time in timeList:
        xyzTrio = [float(xFunc(time)), float(yFunc(time)), float(zFunc(time))]
        retList.append(xyzTrio)
    
    return timeList, retList

def pointAveraging(timeList, rList, gList, bList):
    digit = 1
    timeComparator = 0
    tempRList, tempGList, tempBList = [], [], []
    tempTimeList = []
    averagedRList, averagedGList, averagedBList = [], [], []
    averagedTimeList = []
    tempIndexList = []
    for i, time in enumerate(timeList):
        if round(time, digit) == timeComparator: #If has same 2 decimals
            tempRList.append(rList[i])
            tempGList.append(gList[i])
            tempBList.append(bList[i])
            tempIndexList.append(i)
            if tempTimeList == []: #If list is empty we also need to add the previous element
                tempTimeList.append(time) 
                tempTimeList.append(timeList[i-1]) #Won't error as index 0 doesn't actually enter here
            else:
                tempTimeList.append(time)
            
        elif tempRList != []:
            averageR = normalizeRGB(sum(tempRList) / len(tempRList)) #Average 
            averageG = normalizeRGB(sum(tempGList) / len(tempGList))
            averageB = normalizeRGB(sum(tempBList) / len(tempBList))
            averageT = sum(tempTimeList) / len(tempTimeList)
            averagedRList.append(averageR)
            averagedGList.append(averageG)
            averagedBList.append(averageB)
            averagedTimeList.append(averageT)
            tempRList, tempGList, tempBList, tempTimeList = [], [], [], [] #LIST DUMP

        timeComparator = round(time, digit)
    
    for i, time in enumerate(timeList): #Adds all values that were not averaged
        if i not in tempIndexList:
            averagedTimeList.append(time)
            averagedRList.append(rList[i])
            averagedGList.append(gList[i])
            averagedBList.append(bList[i])

    return averagedRList, averagedGList, averagedBList, averagedTimeList

def pointAverageGeneral(list1, list2, closeness):
    high = 0
    retList1, retList2 = [], []
    for i, time in enumerate(list1):
        if time > high:
            low = time - closeness
            high = time + closeness
            tempList1, tempList2 = findBetween(list1, list2, low, high)
            retList1.append(sum(tempList1) / len(tempList1))
            retList2.append(sum(tempList2) / len(tempList2))
    
    return retList1, retList2

def findBetween(list1, list2, low, high):

    retList1, retList2 = [], []
    for i, j in enumerate(list1):
        if(j >= low and j <= high):
            retList1.append(list1[i])
            retList2.append(list2[i])

    return retList1, retList2

def normalizeRGB(value): #Normalizes rgb values 
    if value > 1:
        return 1
    else:
        return value

sys.path.insert(0, os.path.join(cwd, "Data"))

def filterVBandForFlux(lamS, spec): #Taken from here: https://astronomy.stackexchange.com/questions/16286/how-can-i-convolve-a-template-spectrum-with-a-photometric-filter-response-spectr
    from VFilter import lambV, filterV
    filterProperLamb  = np.interp(lamS,lambV,filterV)              #Interpolate to common wavelength axis
    filtSpec  = filterProperLamb * spec                        #Calculate throughput
    flux      = simps(filtSpec,lamS)                   #Integrate over wavelength
    return flux

def filterVBandForApMag(lamb, spectra):
    from VFilter import lambV, filterV
    filterX, filterY = np.array(lambV), np.array(filterV)
    spectrumX = np.array(lamb)
    spectrumY = np.array(spectra)
    filterYInterp = np.interp(spectrumX, filterX, filterY)
    filterMultSpec = filterYInterp * spectrumY
    I = simps(filterMultSpec, spectrumX)
    m = -2.5 * np.log10(I) - 13.5
    return m

def scaleApMag(oldDistance, newDistance, apMag):
    abMag = apMag - (5 * np.log10(oldDistance /  10))
    newApMag = abMag +  (5 * np.log10(newDistance / 10))
    return newApMag

def apMagToIlluminance(apMag):
    return 10 ** ((-14.18 - apMag) / 2.5)

def timeMJDToSinceEvent(start, current):
    current = astropy.time.Time(current, format='mjd')
    start = astropy.time.Time(start, format='mjd')
    td = current - start
    days = math.floor(td.sec / (60 * 60 * 24))
    hours = math.floor((td.sec % (60 * 60 * 24)) / (60 * 60))
    minutes = math.floor(((td.sec % (60 * 60 * 24)) % (60 * 60)) / 60)
    seconds = math.floor(((td.sec % (60 * 60 * 24)) % (60 * 60)) % 60)
    return "{}d ".format(days) + "{0:02d}h".format(hours)
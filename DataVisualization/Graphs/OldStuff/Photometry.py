import matplotlib.pyplot as plt 
import json
import sys
from pprint import pprint
from scipy import interpolate 
from scipy.signal import savgol_filter
import numpy as np
from GraphicalFunctions import filterVBandForFlux, filterVBandForApMag, scaleApMag

dataPath = "/home/n/Documents/Research/GW170817-Milky-Way/Data"
sys.path.insert(0, dataPath)

class Photometry():
    """A class implementingy Photometry, should contain any and all functions relating to photometry, should not really be color related very much"""

    def __init__(self, data =  None, spectrum = None, distance = 40e6): #Initialization via photometry data
        self.bandDictionary = {} #Band as key and tuple of lists 1st list is time second is magnitude
        self.distance = 40e6 #Mpc
        timeList, magnitudeList = [], []

        if spectrum == None:
            i = 0
            bandNameList = []
            while True: #Takes all band names because sometimes they are out of order
                try:
                    bandName = data["GW170817"]["photometry"][i]["band"]

                    if bandName not in bandNameList:
                        bandNameList.append(bandName)
                    i += 1
                except:
                    break

            for bandName in bandNameList: #prep
                self.bandDictionary[bandName] = ([],[]) #Just inputs empty lists for now

            i = 0
            while True:
                try:
                    try: #In a few cases there is no band for some reason 
                        bandName = data["GW170817"]["photometry"][i]["band"] #Name of the band
                    except KeyError:
                        i += 1 
                        continue
                    time = data["GW170817"]["photometry"][i]["time"]
                    magnitude = data["GW170817"]["photometry"][i]["magnitude"]

                    for bandNameIterator in bandNameList:
                        if bandName == bandNameIterator:
                            self.bandDictionary[bandName][0].append(float(time)) #Adds to list in tuple
                            self.bandDictionary[bandName][1].append(float(magnitude))

                    i += 1
                except IndexError: #For when we run out of data
                    break
        else: #Not interpolated spectra colors
            timeList, fluxList, magnitudeList = [], [], []
            for i, spectraPacket in enumerate(spectrum.spectraList):
                time = spectraPacket[0]
                lamb = spectrum.spectraList[i][1][0] #Lambda list from Spectra Class
                spectra = spectrum.spectraList[i][1][1]
                flux = filterVBandForFlux(lamb, spectra) #Gets flux according to V band
                magnitude = filterVBandForApMag(lamb, spectra)
                timeList.append(time)
                fluxList.append(flux)
                magnitudeList.append(magnitude)
            
            self.bandDictionary['V'] = (timeList, magnitudeList)
            self.rescaleDistance(distance)
            self.distance = distance
            
        #Interpolation section, makes dictionary similar to bandDictionary but with interpolated values
        interpolatedBandMagList = []
        self.interpolatedBandDict = {}
        for bandName, timeMagPair in self.bandDictionary.items():
            temp = self.interpolatePhotometry(timeMagPair)
            interpolatedTime = temp[0]
            interpolatedBandMagList = temp[1]
            self.interpolatedBandDict[bandName] = ([interpolatedTime, interpolatedBandMagList])

    def interpolatePhotometry(self, timeMagPair):
        extendedTimeList = np.linspace(timeMagPair[0][0], timeMagPair[0][-1], 1000)
        interpolatedBand = interpolate.interp1d(timeMagPair[0], timeMagPair[1], kind = 'linear')
        interpolatedBandMagList = [interpolatedBand(time) for time in extendedTimeList]
        return (extendedTimeList, interpolatedBandMagList)

    def apMagToIlluminance(self, apMag):
        return 10 ** (-14.18 - apMag) / 2.5

    def plotPhotometryScatter(self, userBandNames = []):
        if userBandNames == []: #If the user didn't input anything just plot all of them
            userBandNames = self.bandDictionary.keys()
        for bandName, timeMagPair in self.bandDictionary.items():
            if bandName in userBandNames: #only plots ones in the list 
                plt.scatter(timeMagPair[0], timeMagPair[1], marker='o', s = 5, label = bandName)

    def plotPhotometryInterpolated(self, userBandNames = []):
        if userBandNames == []:
            userBandNames = self.bandDictionary.keys()
    
        for bandName, timeMagPair in self.interpolatedBandDict.items():
            if bandName in userBandNames: #only plots ones in the list 
                extendedTimeList = timeMagPair[0]
                interpolatedBandMagList = timeMagPair[1]
                interpolatedBandMagList = savgol_filter(interpolatedBandMagList, 51, 3)
                plt.plot(extendedTimeList, interpolatedBandMagList, label = bandName)

    def plotStandard(self):
        plt.xticks([57983 + i for i in range(0, 10)], [i for i in range(0, 10)])
        #plt.ylim([16, 40])
        plt.ylabel("Apparant Magnitude (d = 300pc)")
        plt.xlabel("Time since Merger (days)")
        plt.gca().invert_yaxis()
        plt.legend()
        plt.show()

    def plotFlux(self):
        plt.ylabel("Flux")
        plt.yscale("Log")
        plt.show()

    def rescaleDistance(self, newDistance):
        for bandName, timeMagPair in self.bandDictionary.items():
            for i, apMag in enumerate(timeMagPair[1]):
                newApMag = scaleApMag(self.distance, newDistance, apMag)
                self.bandDictionary[bandName][1][i] = newApMag

GW170817_json_data = open("/home/n/Documents/Research/GW170817-Milky-Way/Data/GW170817DataGeneric.json").read()
data = json.loads(GW170817_json_data)

from Spectra import GW170817SpectraFull
GW170817Generic = Photometry(data = data)
GW170817Generic.rescaleDistance(300)
GW170817Generic.plotPhotometryScatter(["V"])
#GW170817Generic.plotPhotometryInterpolated(["V"])
GW170817Photometry = Photometry(spectrum = GW170817SpectraFull)
print(GW170817Photometry.bandDictionary)
# GW170817Photometry.plotPhotometryScatter()

GW170817Generic.plotStandard()
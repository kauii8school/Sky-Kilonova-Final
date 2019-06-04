import matplotlib.pyplot as plt 
import json
import sys
from astropy.time import Time
import numpy as np
from scipy import interpolate
from scipy.signal import savgol_filter
import matplotlib as mpl
ciePath = ciePath = "/home/n/Documents/Research/GW170817-Milky-Way/CIE"
dataPath = "/home/n/Documents/Research/GW170817-Milky-Way/Data"
sys.path.insert(0, ciePath)
sys.path.insert(0, dataPath)
from GraphicalFunctions import *
from ColorSystem import cs_hdtv

class Star:

    def __init__(self, _name, _data, _values, _distance, _numInterpPts = 1000):
        self.name = _name
        self.distance = _distance
        self.numInterpPts = _numInterpPts

        #Beginning of Spectra data 
        self.data = _data
        self.spectraList, self.spectraSkipList  = [], [] #of the form [time, (wavelengthList, fluxList)] the skip has skipped sections where the transmission jumps

        for i in _values: #We iterate through values because these are the ones where the full info is defines #NOTE# later you should change this so that there is no need for user specified values, it just takes a dataset and cleverly chooses values which have their domain in (380nm, 780nm)
            wavelengthList, fluxSkipList, fluxList = [], [], []
            j = 0
            while(True):
                time = float(self.data["GW170817"]["spectra"][i][0]) #not in innter try catch because if this is out of range we want to fully kill loop
                try:
                    wavelength = float(self.data["GW170817"]["spectra"][i][1][j][0])
                    flux = float(self.data["GW170817"]["spectra"][i][1][j][1])
                    wavelengthList.append(wavelength)
                    fluxList.append(flux) #Always appends no matter what

                    if 13363 < wavelength < 14389 or 17860 < wavelength < 19429 or 9536 < wavelength < 10000: #Skips the wavelengths that peak the  graph and cause it to look weird
                        j += 20
                        fluxSkipList.append(None)
                        continue 

                    fluxSkipList.append(flux)
                    j += 20 #Just speeding up the process 20 is a good number but at the end you may want to change it around #NOTE#

                except IndexError: #For when i runs out 
                    break

            self.spectraSkipList.append((time, [wavelengthList, fluxSkipList])) #For ones with skipped values primarily for graphing purposes
            self.spectraList.append((time, [wavelengthList, fluxList]))
            self.colorList = self.findSpectraColor()

        #After spectrum is created we must next create photometry from it for our purposes we are only concerned w/ the Johnson V band
        timeList, fluxList, magnitudeList = [], [], []
        for i, spectraPacket in enumerate(self.spectraList):
            time = spectraPacket[0]
            lamb = self.spectraList[i][1][0] #Lambda list from Spectra Class
            spectra = self.spectraList[i][1][1]
            flux = filterVBandForFlux(lamb, spectra) #Gets flux according to V band
            magnitude = filterVBandForApMag(lamb, spectra)
            timeList.append(time)
            fluxList.append(flux)
            magnitudeList.append(magnitude)
        
        self.bandDictionary = {} #Band as key and tuple of lists 1st list is time second is magnitude
        self.bandDictionary['V'] = (timeList, magnitudeList)
        self.distance = self.distance
        
        #Interpolation section, makes dictionary similar to bandDictionary but with interpolated values
        interpolatedBandMagList = []
        self.interpolatedBandDict = {}
        for bandName, timeMagPair in self.bandDictionary.items():
            temp = self.interpolatePhotometry(timeMagPair)
            interpolatedTime = temp[0]
            interpolatedBandMagList = [float(i) for i in temp[1]]
            self.interpolatedBandDict[bandName] = ([interpolatedTime, interpolatedBandMagList])

        self.interpolatedColorList = self.interpolateColor()
        self.interpolatedTimeList = interpolatedTime
        #Illuminance allready interpolated
        self.illuminanceList = [apMagToIlluminance(i) for i in self.interpolatedBandDict['V'][1]]
        
        self.interpolatedTimeListUTC = []
        for time in self.interpolatedTimeList: #Reformatting time
            mjdTime = Time(time, format='mjd')
            utcTime = mjdTime.iso
            self.interpolatedTimeListUTC.append(utcTime)

    def interpolateColor(self):
        """ Interpolates and smoothes colors """

        #Unpacking data
        timeList, pointsR, pointsG, pointsB = [], [], [], []
        for (time, rgbTrio) in zip(self.bandDictionary['V'][0], self.colorList):
            timeList.append(time)
            pointsR.append(rgbTrio[0])
            pointsG.append(rgbTrio[1])
            pointsB.append(rgbTrio[2])

        #Averaging points 
        averagedRPoints, averagedGPoints, averagedBPoints, averagedTimePoints = [], [], [], []
        averagedRPoints, averagedGPoints, averagedBPoints, averagedTimePoints = pointAveraging(timeList, pointsR, pointsG, pointsB)

        #Creates iterpolation functions
        rInterpolated = interpolate.interp1d(averagedTimePoints, averagedRPoints)
        gInterpolated = interpolate.interp1d(averagedTimePoints, averagedGPoints)
        bInterpolated = interpolate.interp1d(averagedTimePoints, averagedBPoints)

        #Repacks data in interpolated form
        interpolatedTimeList, rgbListInterpolated = recreateXYZ(self.numInterpPts, rInterpolated, gInterpolated, bInterpolated)

        #Unpacks data
        #Interpolation NOTE look into different interpolators 
        rListInterpolated = [rgbTrio[0] for rgbTrio in rgbListInterpolated]
        gListInterpolated = [rgbTrio[1] for rgbTrio in rgbListInterpolated]
        bListInterpolated = [rgbTrio[2] for rgbTrio in rgbListInterpolated]

        #Smoothing see https://en.wikipedia.org/wiki/Savitzky%E2%80%93Golay_filter
        smoothedR = list(savgol_filter(rListInterpolated, 51, 3))
        smoothedG = list(savgol_filter(gListInterpolated, 51, 3))
        smoothedB = list(savgol_filter(bListInterpolated, 51, 3))

        rgbList = [(normalizeRGB(r), normalizeRGB(g), normalizeRGB(b)) for r, g, b in zip(smoothedR, smoothedG, smoothedB)]
        return rgbList

    def findSpectraColor(self, fmt = 'rgb'):

        """Find color for entire time dependent spectrum and returns a list of it"""
        colorList = []
        for spectra in self.spectraList:
            #Color part for a more detailed explanation see CIE. Basically finds color 
            wavelengthList, fluxList = spectra[1][0], spectra[1][1]
            wavelengthList = [wavelength / 10 for wavelength in wavelengthList] #Convert to nm
            trimmedTuple = limTrimmer((wavelengthList, fluxList), 380, 780)
            wavelengthList, fluxArray = list(trimmedTuple[0]), np.array(trimmedTuple[1])
            cs_hdtv.cmfCreation(wavelengthList)

            if fmt == 'hex':
                color = cs_hdtv.spec_to_rgb(fluxArray, out_fmt = 'html')
            elif fmt == 'XYZ':
                color = list(cs_hdtv.spec_to_xyz(fluxArray))
            else:
                color = list(cs_hdtv.spec_to_rgb(fluxArray))

            colorList.append(color)

        return colorList

    def rescaleDistance(self, newDistance):
        """ Rescales distance to newDistance according to new distance, distance should be in units of pc. This should never be in the __init__ """

        #NOTE 
        newSpectraList = []
        timeList = []
        for spectra in self.spectraList:
            time = spectra[0]
            wavelengthList, fluxList = spectra[1][0], spectra[1][1]
            newFluxList = []
            for flux in fluxList:
                energy = flux * 4 * np.pi * (self.distance ** 2)
                flux = energy / (4 * np.pi * (newDistance ** 2))
                newFluxList.append(flux)
            
            newSpectraList.append([time, (wavelengthList, newFluxList)])     #[time, (wavelengthList, fluxList)] 

        #rescaling distance for  photometry (I'm sure this is correct though)
        for bandName, timeMagPair in self.bandDictionary.items():
            for i, apMag in enumerate(timeMagPair[1]):
                newApMag = scaleApMag(self.distance, newDistance, apMag)
                self.bandDictionary[bandName][1][i] = newApMag

        #Rescaling interpolated lists
        #rescaling distance for  photometry (I'm sure this is correct though)
        for bandName, timeMagPair in self.interpolatedBandDict.items():
            for i, apMag in enumerate(timeMagPair[1]):
                newApMag = scaleApMag(self.distance, newDistance, apMag)
                self.interpolatedBandDict[bandName][1][i] = newApMag

        self.interpolatedBandDict['V'][1] = savgol_filter(self.interpolatedBandDict['V'][1], 51, 3)
        self.illuminanceList = [apMagToIlluminance(i) for i in self.interpolatedBandDict['V'][1]]

    def interpolatePhotometry(self, timeMagPair):
        """ Interpolates photometry, note this should only called by the initializer """
        extendedTimeList = np.linspace(timeMagPair[0][0], timeMagPair[0][-1], self.numInterpPts)
        timeList, magList = pointAverageGeneral(timeMagPair[0], timeMagPair[1], 1)
        # plt.scatter(timeList, [scaleApMag(self.distance, 300, apMag) for apMag in magList])
        # print(timeList, magList)
        # plt.gca().invert_yaxis()
        interpolatedBand = interpolate.interp1d(timeList, magList, bounds_error = False, fill_value = "extrapolate", kind  = 'cubic')
        interpolatedBandMagList = [interpolatedBand(time) for time in extendedTimeList]
        return (extendedTimeList, interpolatedBandMagList)

    def plotPhotometryScatter(self, userBandNames = []):
        if userBandNames == []: #If the user didn't input anything just plot all of them
            userBandNames = self.bandDictionary.keys()
        for bandName, timeMagPair in self.bandDictionary.items():
            if bandName in userBandNames: #only plots ones in the list 
                plt.scatter(timeMagPair[0], timeMagPair[1], marker='o', s = 5, label = bandName)
        
        plt.xticks([57983 + i for i in range(0, 10)], [i for i in range(0, 10)])
        plt.ylabel("Apparant Magnitude")
        plt.xlabel("Time since Merger (days)")
        plt.gca().invert_yaxis()
        plt.legend()

    def plotPhotometryInterpolated(self, userBandNames = []):
        if userBandNames == []:
            userBandNames = self.bandDictionary.keys()
        for bandName, timeMagPair in self.interpolatedBandDict.items():
            if bandName in userBandNames: #only plots ones in the list 
                extendedTimeList = timeMagPair[0]
                interpolatedBandMagList = timeMagPair[1]
                plt.plot(extendedTimeList, interpolatedBandMagList, label = bandName, color = 'w')

        plt.xticks([57982.36180556 + i for i in range(0, 10)], [i for i in range(0, 10)])
        plt.ylabel("Apparant Magnitude")
        plt.xlabel("Time since Merger (days since merger)") 
        plt.gca().invert_yaxis()
        #plt.legend()

    def plotIlluminance(self):
        plt.plot(self.interpolatedTimeList, self.illuminanceList)
        plt.yscale('log')
        plt.ylabel('Luminance lumen/m^2')
        

    def plotSpectra(self):
        """ Plots spectra all spectra values with appropriate colors. Note it will plot the skip list because otherwise it looks very weird """
        for i, spectra in enumerate(self.spectraSkipList):
            time = spectra[0]
            plt.plot(spectra[1][0], spectra[1][1], label = Time(time, format='mjd').datetime, color = self.colorList[i])

        #Formatting 
        fig = plt.gcf()
        fig.set_size_inches(10, 40)
        plt.legend()
        plt.xlabel("Wavelength (Angstroms)")
        plt.ylabel(r"Flux erg/s/cm^2/Angstrom")
        

    def plotColor(self):
        rListInterpolated, gListInterpolated, bListInterpolated = [], [], []
        for rgb in self.interpolatedColorList:
            rListInterpolated.append(rgb[0])
            gListInterpolated.append(rgb[1])
            bListInterpolated.append(rgb[2])

        for time, rgb in zip(self.interpolatedTimeList, self.interpolatedColorList): #Plots background color spectrum
            plt.bar([time], [1.05], color = [rgb[0], rgb[1], rgb[2]], zorder = 1)

        plt.plot(self.interpolatedTimeList, rListInterpolated, label='Red', color = [1, 0, 0])
        plt.plot(self.interpolatedTimeList, gListInterpolated, label='Green', color = [0, 1, 0])
        plt.plot(self.interpolatedTimeList, bListInterpolated, label='Blue', color = [0, 0, 1]) 
        plt.xticks([57982.36180556 + i for i in range(0, 10)], [i for i in range(0, 10)])
        plt.xlim(self.interpolatedTimeList[0], self.interpolatedTimeList[len(self.interpolatedTimeList) - 1])
        plt.ylim(0, 1.05)
        plt.xlabel("Time (days since merger)")
        plt.ylabel("RGB Value")

    def pointPlotPhotometry(self, inputIndex = None, inputTime = None, userBandNames = []):
        """ Plots a point on the graph where the user wants, can be done via index or time. Returns true if worked """
        if userBandNames == []: #If the user didn't input anything just plot all of them
            userBandNames = self.interpolatedBandDict.keys()
        for bandName, timeMagPair in self.interpolatedBandDict.items():
            if bandName in userBandNames: #only plots ones in the list 
                for index, time in enumerate(timeMagPair[0]):
                    if inputIndex == index or inputTime == time:

                        plt.scatter(timeMagPair[0][index], timeMagPair[1][index], marker='o', s = 100, label = bandName, color = 'r', zorder = 10)
                        plt.gca().invert_yaxis()
                        return True

        return False

    @staticmethod
    def savePlot(fileDirectory, fileName, dimensions, name, xlim = (None, None)):
        plt.gca().invert_yaxis()
        plt.xlim(xlim[0], xlim[1])
        if name == "Liberty":
            mpl.rcParams.update({'font.size' : 18}) 
        else:
            mpl.rcParams.update({'font.size' : 15}) 

        #Manhattan
        if name == "Manhattan":
            plt.text(57985.8, -8, "(c) Gupte & Bartos 2019 |  Image credit: King of Hearts / Wikimedia Commons / CC-BY-SA-3.0")

        #Century
        elif name == "Century":
            plt.rcParams.update({'font.size': 10})
            plt.text(57988, -8, "(c) Gupte & Bartos 2019")
            plt.text(57987.85, -7.4, "Image credit: Lynn Palmer")

        #Liberty
        elif name == "Liberty":
            plt.rcParams.update({'font.size': 18})
            plt.text(57987.25, -8, "(c) Gupte & Bartos 2019 | Image credit: Max Touhey")

        #Fort Knox
        elif name == "FortKnox":
            plt.rcParams.update({'font.size': 10})
            plt.text(57988.7, -8, "(c) Gupte & Bartos 2019")
            plt.text(57988.1, -7.4, "Image credit: Bettmann/Getty Images")
    
        elif name == "Perth":
            plt.rcParams.update({'font.size': 13})
            plt.text(57989.1, -8, "(c) Gupte & Bartos 2019")
            plt.text(57989.17, -7.4, "Image credit: Pixelbay")

        fig = plt.gcf()
        fig.set_size_inches(dimensions[0], dimensions[1])
        fig.tight_layout()
        plt.savefig("{}{}".format(fileDirectory, fileName))
        plt.close()
        
GW170817_json_spectra_time_data = open('/home/n/Documents/Research/GW170817-Milky-Way/Data/time+data+instrument+telescope+source.json').read()
data = json.loads(GW170817_json_spectra_time_data)
GW170817 = Star("GW170817", data, [0, 1, 2, 4, 5, 6, 7, 8, 9, 13, 14, 15, 19, 20, 21, 22, 23, 24, 27, 28, 32, 34, 35, 36, 40, 42, 47], 40e6)
GW170817.rescaleDistance(300)
plt.style.use('dark_background')
fig, ax = plt.subplots()

# GW170817.plotColor()
# plt.show()

# GW170817.pointPlotPhotometry(inputIndex=5)
# GW170817.plotPhotometryInterpolated()
#GW170817.savePlot("/home/n/Documents/Research/GW170817-Milky-Way/Natron/ReadImages/Plots/", "AAA.png")
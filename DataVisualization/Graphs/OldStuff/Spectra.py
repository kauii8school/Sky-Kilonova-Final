import matplotlib.pyplot as plt 
import json
import sys
from pprint import pprint
from astropy.time import Time
import numpy as np
import os
cwd = os.getcwd()
ciePath = ciePath = "/home/n/Documents/Research/GW170817-Milky-Way/CIE"
dataPath = "/home/n/Documents/Research/GW170817-Milky-Way/Data"
sys.path.insert(0, ciePath)
sys.path.insert(0, dataPath)
from GraphicalFunctions import *
from ColorSystem import cs_hdtv
from scipy import interpolate
from scipy.signal import savgol_filter


class Spectra:
    """ A class implementing spectra, should contain spectra data and how to manipulate that spectral data """

    def __init__(self, data, values):

        self.distance = 40e6 #Mpc
        self.data = data
        self.spectraList, self.spectraSkipList  = [], [] #of the form [time, (wavelengthList, fluxList)] the skip has skipped sections where the transmission jumps
        for i in values:#[18, 32, 35, 40]: #[0, 9, 18, 32, 35, 40] gives a pretty one!
            wavelengthList, fluxSkipList, fluxList = [], [], []
            j = 0
            while(True):
                time = float(data["GW170817"]["spectra"][i][0]) #not in innter try catch because if this is out of range we want to fully kill loop
                try:
                    wavelength = float(data["GW170817"]["spectra"][i][1][j][0])
                    flux = float(data["GW170817"]["spectra"][i][1][j][1])
                    wavelengthList.append(wavelength)
                    fluxList.append(flux) #Always appends no matter what

                    if 13363 < wavelength < 14389 or 17860 < wavelength < 19429 or 9536 < wavelength < 10000: #Skips the wavelenghts that peak the graph and cause it to look weird
                        j += 20
                        fluxSkipList.append(None)
                        continue 

                    fluxSkipList.append(flux)
                    j += 20 #Just speeding up the process

                except IndexError: #For when i runs out 
                    break

            self.spectraSkipList.append((time, [wavelengthList, fluxSkipList])) #For ones with skipped values primarily for graphing purposes
            self.spectraList.append((time, [wavelengthList, fluxList]))
            self.colorList = self.findSpectraColor()


    def plotSpectra(self):

        for i, spectra in enumerate(self.spectraSkipList):
            time = spectra[0]
            plt.plot(spectra[1][0], spectra[1][1], label = "{} days".format(i+1), color = self.colorList[i])

    def plotStandard(self):
        fig = plt.gcf()
        fig.set_size_inches(10, 40)
        plt.legend()
        plt.xlabel("Wavelength (Angstrom)")
        plt.ylabel(r"Flux erg/s/cm^2/Angstrom")
        plt.show()

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
        #Rescales spectra to distance we specify  newDistance in units of pc

        newSpectraList = []
        for spectra in self.spectraList:
            time = spectra[0]
            wavelengthList, fluxList = spectra[1][0], spectra[1][1]
            newFluxList = []
            for flux in fluxList:
                energy = flux * 4 * np.pi * (self.distance ** 2)
                flux = energy / (4 * np.pi * (newDistance ** 2))
                newFluxList.append(flux)
            
            newSpectraList.append([time, (wavelengthList, newFluxList)])     #[time, (wavelengthList, fluxList)] 

        self.spectraList = newSpectraList


#Reading data from a 
import matplotlib as mpl
mpl.rcParams.update({'font.size' : 15})
GW170817_json_spectra_time_data = open(os.path.join(dataPath, 'time+data+instrument+telescope+source.json')).read()
data = json.loads(GW170817_json_spectra_time_data)
values = range(0, 50)
#GW170817SpectraAll = Spectra(data, values) #Values is where a list where we should evaluated
GW170817SpectraFull = Spectra(data, [0, 9, 18, 32, 35, 40])
# GW170817SpectraFull.plotSpectra()
# GW170817SpectraFull.plotStandard()
# [0, 1, 2, 4, 5, 6, 7, 8, 9, 13, 14, 15, 19, 20, 21, 22, 23, 24, 27, 28, 32, 34, 35, 36, 40, 42, 47]) #Full only 
# GW170817SpectraFull.plotSpectra()
# GW170817SpectraFull.plotStandard()
#has values with full range of wavelengths
#print(GW170817SpectraFull.findSpectraColor(fmt = 'XYZ'))
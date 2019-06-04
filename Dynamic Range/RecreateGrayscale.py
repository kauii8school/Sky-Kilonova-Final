import sys
from scipy import interpolate
import numpy as np
import math
import matplotlib.pyplot as plt
from PIL import Image

sys.path.insert(0, "/home/n/Documents/Research/GW170817-Milky-Way/Dynamic Range/Data")
sys.path.insert(0, "/home/n/Documents/Research/GW170817-Milky-Way/DataVisualization/Graphs")
from GrayScale import camResponse
from Star import GW170817
#Going to use spencer's PSF function for photopic vision for testing 

def PSFp(theta):

    """ Point spread function for a photopic normal observer. See luthuli.cs.uiuc.edu/~daf/courses/rendering/papers3/spencer95.pdf """

    #Assuming a point source so a = 0 in the spencer paper equation 2
    def f1(theta):
        return 20.91 / ((theta + .02) ** 3)

    def f2(theta):
        return 72.37 / ((theta + .02) ** 2)

    def f0(theta):
        return 2.61e6 * math.exp(-((theta / .02) ** 2))

    return ((.384 * f0(theta)) + (.478 * f1(theta)) + (.138 * f2(theta)))  #The last term is to normalize NOTE do I need to normalize?

luxList = GW170817.illuminanceList
thetaList = np.linspace(0, 90, 100)

shutterSpeed = 1/30 #s
pixelValuesForTheta = []
for lux in luxList:
    pixelValuesForTheta.append(float(camResponse(lux * shutterSpeed)))
    print(lux, float(camResponse(lux * shutterSpeed)))

#Image creation
imageWidth, imageHeight = 512, 512
im = Image.new("RGB", (imageWidth, imageHeight))
pix = im.load()
for x in range(imageWidth):
    for y in range(imageHeight):
        pix[x,y] = (100, 100, 100)

im.save("/home/n/Documents/Research/GW170817-Milky-Way/Dynamic Range/Images/test.png", "PNG")
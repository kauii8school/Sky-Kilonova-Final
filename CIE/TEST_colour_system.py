# import matplotlib.pyplot as plt
# import numpy as np
# from colour_system import cs_hdtv

# def planck(wav, T):
#     wav = 1e-9 * wav
#     h = 6.626e-34
#     c = 3.0e+8
#     k = 1.38e-23
#     a = 2.0*h*c**2
#     b = h*c/(wav*k*T)
#     intensity = a/ ( (wav**5) * (np.exp(b) - 1.0) )
#     return intensity
# def parabola(wav, T):
#     return 
# wavelengthList = np.linspace(380, 780)
# for T in [500, 1500, 4500, 6000, 7000, 8000, 10000, 14000, 16000, 18000]:
#     intensity = np.array([parabola(wav, T) for wav in wavelengthList])
#     cs_hdtv.cmfCreation(wavelengthList)
#     color = cs_hdtv.spec_to_rgb(intensity, out_fmt='html')
#     plt.plot(wavelengthList, intensity, color = color, label = str(T) + "K")

# print(list(wavelengthList), intensity)

# plt.xlabel('Wavelength (nm)')
# plt.ylabel("Intensity")
# plt.legend()
# plt.show()

import os
cwd = os.getcwd()
print(cwd)
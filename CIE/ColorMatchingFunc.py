import math

#Color matching function approximations taken from this paper : http://jcgt.org/published/0002/02/01/paper.pdf

def xBar(l):
    return .398 * math.exp(-1250 * (math.log( (l + 570.1) / 1014)  ** 2) ) + 1.132 * math.exp(-234 * (math.log( (1338 - l) / 743.5 ) ** 2))

def yBar(l):
    return 1.011 * math.exp(-.5 * (((l - 556.1) / 46.14)  ** 2))

def zBar(l):
    return 2.060 * math.exp(-32 * (math.log((l - 265.8) / 180.4) ** 2))

# import matplotlib.pyplot as plt
# import numpy as np
# plt.plot(np.linspace(380, 780, 1000), [xBar(i) for i in np.linspace(380, 780, 1000)], label = r'$\bar{x}$')
# plt.plot(np.linspace(380, 780, 1000), [yBar(i) for i in np.linspace(380, 780, 1000)], label = r'$\bar{y}$')
# plt.plot(np.linspace(380, 780, 1000), [zBar(i) for i in np.linspace(380, 780, 1000)], label = r'$\bar{z}$')
# plt.legend()
# plt.xlabel("Wavelength (nm)")
# plt.show()
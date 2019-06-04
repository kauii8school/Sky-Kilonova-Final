import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import sys
sys.path.insert(0, "C:\\Users\\gupte\\Documents\\Everything\\Research\\GW170817 in Milky Way\\Data Visualization\\Graphs")
sys.path.insert(0, "C:\\Users\\gupte\\Documents\\Everything\\Research\\GW170817 in Milky Way\\Data Visualization\\CIE")
from SpectraHumanColor import spectraList, cs_hdtv
from Tristimulus import limTrimmer
global spectraList 
global cs_hdtv
from SpectraHumanColor import spectraList
global spectraList 

# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure()
fig.set_size_inches(30, 30)
ax = plt.axes(xlim=(380, 780), ylim=(2e-19, 2e-15))
line, = ax.plot([], [], lw=2)

# initialization function: plot the background of each frame
def init():
    line.set_data([], [])
    return line,


# animation function.  This is called sequentially
def animate(i):
    wavelengthList, fluxList = spectraList[i][1][0], spectraList[i][1][1]
    wavelengthList = [wavelength / 10 for wavelength in wavelengthList] #Convert to nm
    trimmedTuple = limTrimmer((wavelengthList, fluxList), 380, 780) #Trims to fit limits
    wavelengthList, fluxArray = list(trimmedTuple[0]), np.array(trimmedTuple[1]) #Sets new wavelength and flux list
    cs_hdtv.cmfCreation(wavelengthList) #creates matrix for cmf
    graphColor = cs_hdtv.spec_to_rgb(fluxArray, out_fmt = 'html')
    line.set_data(wavelengthList, list(fluxArray))
    line.set_color(graphColor)
    return line,

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init,
           frames=200, interval=3000, blit=True)

plt.show()
anim.save('C:\\Users\\gupte\\Documents\\Everything\\Research\\GW170817 in Milky Way\\Data_Visualization\\Animation\\ basic_animation.html', fps=30, extra_args=['-vcodec', 'libx264'])


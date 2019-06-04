from PIL import Image

def findMarker(frameNumber):
    im = Image.open("/home/n/Documents/Research/GW170817-Milky-Way/Natron/ReadImages/StellMarker/frame_{0:03}.png".format(frameNumber))
    width, height = im.size
    pix = im.load()

    posPosX, posPosY = [], []
    for  i in range(width):
        for j in range(height):
            pixel = im.getpixel((i, j))
            r,g,b = pixel[0], pixel[1], pixel[2]
            r,g,b = r/255, g/255, b/255

            if g == 1 and 0 < r < .2 and 0 < b < .2: #r, g, b) == (0.1411764705882353, 1, 0.16470588235294117):
                posPosX.append(i)
                posPosY.append(1080 - j)


    #Averaging posPosX and posPosY
    if len(posPosX) == 0:
        return None, None
    posX = int(round(sum(posPosX) / len(posPosX)))
    posY = int(round(sum(posPosY) / len(posPosY)))

    return posX, posY
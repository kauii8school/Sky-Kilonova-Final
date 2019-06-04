global timeText
global backgroundFileName
global mixValue
global includeText
global skyFileName
global includeStar
global staticBackground
global includePlot
global plotFileName
global card1AxisTranslate
global card2AxisTranslate
global xText
global yText
global fileDimensions

from CreateStarVarBox import * #Imports vars from CreateVideo.py

def createInstance(app,group):

    #Beginning of app format
    app.addFormat("Star {} 1".format(fileDimensions))

    param = app.getProjectParam("outputFormat")
    param.setValue("Star")
    #End of app format

    #Beginning of starReader
    starReader = app.createReader("/home/n/Documents/Research/GW170817-Milky-Way/Natron/ReadImages/StellNoMarker/StellBack{}.png".format(skyFileName))
    #End of starReader

    #Beginning of background star reader
    backgroundReader = app.createReader("/home/n/Documents/Research/GW170817-Milky-Way/Natron/ReadImages/{}.png".format(backgroundFileName))
    #End of background star reader

    if includeStar == True:
        flare = app.createNode("hilol")

    writer = app.createWriter("/home/n/Documents/Research/GW170817-Milky-Way/Natron/WriteImages/AAAA.png")
    writer.setScriptName("MyWriter")

    #Beginning of Merge1
    lastNode = app.createNode("net.sf.openfx.MergePlugin")
    lastNode.setScriptName("Merge1")
    lastNode.setLabel("Merge1")

    param = lastNode.getParam("mix")
    param.setValue(mixValue)

    param = lastNode.getParam("operation")
    param.setValue("plus")

    merge1 = lastNode
    del lastNode
    #End of Merge1

    #Beginning of Merge2
    lastNode = app.createNode("net.sf.openfx.MergePlugin")
    lastNode.setScriptName("Merge2")
    lastNode.setLabel("Merge2")

    param = lastNode.getParam("operation")
    param.setValue("plus")

    merge2 = lastNode
    del lastNode
    #End of Merge2

    #Beginning of Merge3
    lastNode = app.createNode("net.sf.openfx.MergePlugin")
    lastNode.setScriptName("Merge3")
    lastNode.setLabel("Merge3")

    param = lastNode.getParam("operation")
    param.setValue("plus")

    merge3 = lastNode
    del lastNode
    #End of Merge3

    #Beginning of Card1
    lastNode = app.createNode("net.sf.openfx.Card3D")
    lastNode.setScriptName("Card3D1")
    lastNode.setLabel("Card3D1")

    param = lastNode.getParam("axisTranslate")
    param.setValue(card1AxisTranslate, 1)

    card1 = lastNode
    del lastNode
    #End of Card1

    #Beginning of Card2
    lastNode = app.createNode("net.sf.openfx.Card3D")
    lastNode.setScriptName("Card3D2")
    lastNode.setLabel("Card3D2")

    param = lastNode.getParam("axisTranslate")
    param.setValue(card2AxisTranslate, 1)

    card2 = lastNode
    del lastNode
    #End of Card2    

    #Beginning of readPlot
    plotReader = app.createReader("/home/n/Documents/Research/GW170817-Milky-Way/Natron/ReadImages/Plots/{}.png".format(plotFileName))
    #End of readPlot

    #Beginning of Merge4
    lastNode = app.createNode("net.sf.openfx.MergePlugin")
    lastNode.setScriptName("Merge4")
    lastNode.setLabel("Merge4")

    param = lastNode.getParam("operation")
    param.setValue("over")

    merge4 = lastNode
    #End of Merge4

    #Beginning of Text
    lastNode = app.createNode("net.fxarena.openfx.Text")

    param = lastNode.getParam("text")
    param.setDefaultValue(timeText)
    param.setValue("t={}".format(timeText))
    del param

    param = lastNode.getParam("scale")
    param.setValue(.5, 0)
    param.setValue(.5, 1)
    del param
 
    param = lastNode.getParam("center")

    param.setValue(xText, 0)
    param.setValue(yText, 1)

    del param

    text = lastNode
    del lastNode
    #End of Text

    #Node connections
    if staticBackground == False:
        merge1.connectInput(0, starReader)

    if includeStar == True:
        merge1.connectInput(1, flare)

    merge2.connectInput(0, merge1)
    merge2.connectInput(1, backgroundReader)

    if includeText == True:
        merge3.connectInput(0, text)
    
    merge3.connectInput(1, merge2)
    card1.connectInput(0, merge3)

    if includePlot == True:
        card2.connectInput(0, plotReader)
        merge4.connectInput(0, card2)

    merge4.connectInput(1, card1)
    #reformat.connectInput(0, backgroundReader)

    writer.connectInput(0, merge4)
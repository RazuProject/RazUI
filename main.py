import razui

coolWindow = razui.Window("window.ini")

coolObjects = coolWindow.Frames["frame_1.ini"]["Objects"]
otherCoolObjects = coolWindow.Frames["frame_2.ini"]["Objects"]

def buttonClicked():
    coolObjects["SecondButton"].setVisible(not(coolObjects["SecondButton"].getVisible()))

def secondButtonClicked():
    coolWindow.setFrame("frame_2.ini")

def frame2ButtonClicked():
    coolWindow.setFrame("frame_1.ini")

coolObjects["Button"].bindEvent("click", buttonClicked)
coolObjects["SecondButton"].bindEvent("click", secondButtonClicked)
otherCoolObjects["Button"].bindEvent("click", frame2ButtonClicked)

coolWindow.run()
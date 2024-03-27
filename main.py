import razui

coolWindow = razui.Window("window.ini")

coolObjects = coolWindow.Frames["frame_1.ini"]["Objects"]

def buttonClicked():
    print("Click!!!!")

def secondButtonClicked():
    coolWindow.setFrame("frame_2.ini")

coolObjects["Button"].bindEvent("active", buttonClicked)
coolObjects["SecondButton"].bindEvent("active", secondButtonClicked)

coolWindow.run()
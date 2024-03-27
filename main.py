import razui

coolWindow = razui.Window("window.ini")

coolObjects = coolWindow.Objects

def buttonClicked():
    print("Click!!!!")

coolObjects["Button"].bindEvent("active", buttonClicked)
coolObjects["SecondButton"].bindEvent("active", buttonClicked)

coolWindow.run()
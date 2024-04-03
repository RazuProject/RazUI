from .object import *

class Rendering:
    @staticmethod
    def calculateObjectSize(object: Object, windowSize: tuple, gridSize: int) -> Object:
        xList = range(0, int(windowSize[0] / gridSize))
        yList = range(0, int(windowSize[1] / gridSize))

        startX = xList[object.getAreaWidth()[0]] * gridSize
        endX = xList[object.getAreaWidth()[1]] * gridSize
        startY = yList[object.getAreaHeight()[0]] * gridSize
        endY = yList[object.getAreaHeight()[1]] * gridSize
        
        xSize = endX - startX
        ySize = endY - startY
        
        object.setPosition((startX, startY))
        object.renderSprite((xSize, ySize))

        return object
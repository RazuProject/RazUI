from .ini import *
from .render import *
from .object import *

import random

from os import environ
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame

def calculateObjectSize(object: Object | ContainerObject, windowSize: tuple, gridSize: int) -> Object:
    xList = range(0, int(windowSize[0] / gridSize))
    yList = range(0, int(windowSize[1] / gridSize))

    startX = xList[object.areaWidth[0]] * gridSize
    endX = xList[object.areaWidth[1]] * gridSize
    startY = yList[object.areaHeight[0]] * gridSize
    endY = yList[object.areaHeight[1]] * gridSize
    
    xSize = endX - startX
    ySize = endY - startY
    
    object.setPosition((startX, startY))
    object.renderSprite((xSize, ySize))

    return object

class Window:
    def __init__(self, config: str):
        self.config = read_ini(config)

        self.layout = read_ini(self.config["Layout"]["Frames"].split(",")[0])
        self.Objects = getObjectsFromConfigFile(self.layout)
        self.size = (self.config["Window"]["Width"],self.config["Window"]["Height"])

        print("setted up??? (real!??????)")

        background_color = (255, 255, 255) # flashbang o_O
  
        screen = pygame.display.set_mode(self.size) 
        
        pygame.display.set_caption(self.config["Window"]["Title"]) 
        
        screen.fill(background_color) 
        
        pygame.display.flip() 
        
        # https://images-ext-1.discordapp.net/external/JBZ3yVKtL-rx2ZbgqjePnzMIjqhqTB8ETpE9KI3n-Q4/https/media.tenor.com/n5rrafoDxAUAAAPo/pan-cake.mp4

        
        for object in self.Objects:
            renderedObject = calculateObjectSize(self.Objects[object], self.size, self.config["Layout"]["Grid"])
            screen.blit(Renderer.convertPillowImageToPygameImage(renderedObject.getRenderedSprite()), renderedObject.getPosition())

        pygame.display.flip()
        
        running = True
        
        while running: 
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    running = False
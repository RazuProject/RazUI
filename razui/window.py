from .ini import *
from .render import *
from .object import *

import random

from os import environ
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame
import pygame.freetype

def calculateObjectSize(object: Object | ContainerObject, windowSize: tuple, gridSize: int) -> Object:
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

class Window:
    def renderFrame(self):
        background_color = (255, 255, 255) # flashbang o_O

        self.__screen.fill(background_color)
        
        # https://images-ext-1.discordapp.net/external/JBZ3yVKtL-rx2ZbgqjePnzMIjqhqTB8ETpE9KI3n-Q4/https/media.tenor.com/n5rrafoDxAUAAAPo/pan-cake.mp4

        my_font = pygame.freetype.SysFont('Sans', 16)
        
        for object in self.Objects:
            renderedObject = calculateObjectSize(self.Objects[object], self.size, self.config["Layout"]["Grid"])
            renderedObject.setPygameSprite(Renderer.convertPillowImageToPygameImage(renderedObject.getRenderedSprite()))

            self.__screen.blit(renderedObject.getPygameSprite(), renderedObject.getPosition())

            if renderedObject.getRenderText():
                spriteX, spriteY = renderedObject.getPosition()
                spriteWidth, spriteHeight = renderedObject.getRenderedSprite().size

                textX, textY, textWidth, textHeight = my_font.get_rect(renderedObject.getLabel(), size = 16)

                fontPosition = (
                    spriteX + int(spriteWidth/2) - int(textWidth/2),
                    spriteY + int(spriteHeight/2) - int(textHeight/2)
                )

                my_font.render_to(self.__screen, fontPosition, renderedObject.getLabel(), (0, 0, 0))

        pygame.display.flip()

    def __init__(self, config: str):
        self.config = read_ini(config)

        self.layout = read_ini(self.config["Layout"]["Frames"].split(",")[0])
        self.Objects = getObjectsFromConfigFile(self.layout)
        self.size = (self.config["Window"]["Width"],self.config["Window"]["Height"])

        print("setted up??? (real!??????)")
  
        self.__screen = pygame.display.set_mode(self.size) 
        
        pygame.display.set_caption(self.config["Window"]["Title"]) 

        pygame.init()

        self.renderFrame()

    def run(self):
        running = True
        
        while running:
            for event in pygame.event.get():
                for object in self.Objects:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if self.Objects[object].getCollissionRect().collidepoint(event.pos):
                            self.Objects[object].onActive()
                            self.renderFrame()
                    if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        if self.Objects[object].getCollissionRect().collidepoint(event.pos):
                            self.Objects[object].onHover()
                            self.renderFrame()
                    elif event.type == pygame.MOUSEMOTION:
                        if self.Objects[object].getCollissionRect().collidepoint(event.pos):
                            self.Objects[object].onHover()
                            self.renderFrame()
                        else:
                            self.Objects[object].onStatic()
                            self.renderFrame()
                        
                if event.type == pygame.QUIT: 
                    running = False
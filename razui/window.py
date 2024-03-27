from .ini import *
from .render import *
from .object import *

import random

from os import environ
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame
import pygame.freetype

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

class Window:
    def renderFrame(self):
        background_color = (255, 255, 255) # flashbang o_O

        self.__screen.fill(background_color)
        
        # https://images-ext-1.discordapp.net/external/JBZ3yVKtL-rx2ZbgqjePnzMIjqhqTB8ETpE9KI3n-Q4/https/media.tenor.com/n5rrafoDxAUAAAPo/pan-cake.mp4

        for object in self.__frame["Objects"]:

            if self.__frame["Objects"][object].getVisible():
                renderedObject = calculateObjectSize(self.__frame["Objects"][object], self.__size, self.config["Layout"]["Grid"])
                renderedObject.setPygameSprite(Renderer.convertPillowImageToPygameImage(renderedObject.getRenderedSprite()))

                self.__screen.blit(renderedObject.getPygameSprite(), renderedObject.getPosition())

                if renderedObject.getRenderText():
                    font = pygame.freetype.SysFont('Sans', self.__frame["Objects"][object].getLabelSize())

                    spriteX, spriteY = renderedObject.getPosition()
                    spriteWidth, spriteHeight = renderedObject.getRenderedSprite().size

                    textX, textY, textWidth, textHeight = font.get_rect(renderedObject.getLabel(), size=self.__frame["Objects"][object].getLabelSize())

                    fontPosition = (
                        spriteX + int(spriteWidth/2) - int(textWidth/2),
                        spriteY + int(spriteHeight/2) - int(textHeight/2)
                    )

                    font.render_to(self.__screen, fontPosition, renderedObject.getLabel(), (0, 0, 0))

        pygame.display.flip()

    def setFrame(self, frame: str):
        self.__frame = self.Frames[frame]
        self.renderFrame()

    def __init__(self, config: str):
        self.config = read_ini(config)

        self.Frames = {}

        for frame in self.config["Layout"]["Frames"].split("\",\""):
            self.Frames[frame] = read_ini(frame)
            self.Frames[frame]["Objects"] = getObjectsFromConfigFile(self.Frames[frame])
            
        self.__frame = self.Frames[self.config["Layout"]["Frames"].split("\",\"")[0]]

        self.__size = (
            self.config["Window"]["Width"] * self.config["Layout"]["Grid"],
            self.config["Window"]["Height"] * self.config["Layout"]["Grid"]
        )

        print("setted up??? (real!??????)")
  
        self.__screen = pygame.display.set_mode(self.__size) 
        
        pygame.display.set_caption(self.config["Window"]["Title"]) 

        pygame.init()

        self.renderFrame()

    def run(self):
        running = True
        
        while running:
            for event in pygame.event.get():
                for object in self.__frame["Objects"]:
                    if self.__frame["Objects"][object].getVisible():
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            if self.__frame["Objects"][object].getCollissionRect().collidepoint(event.pos):
                                self.__frame["Objects"][object].onActive()
                                self.renderFrame()
                        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                            if self.__frame["Objects"][object].getCollissionRect().collidepoint(event.pos):
                                self.__frame["Objects"][object].onHover()
                                self.renderFrame()
                        elif event.type == pygame.MOUSEMOTION:
                            if self.__frame["Objects"][object].getCollissionRect().collidepoint(event.pos):
                                self.__frame["Objects"][object].onHover()
                                self.renderFrame()
                            else:
                                self.__frame["Objects"][object].onStatic()
                                self.renderFrame()
                        
                if event.type == pygame.QUIT: 
                    running = False
from .ini import *
from .render import *
from .rendering import *
from .object import *

import random, os, secrets, subprocess, shutil
from zipfile import ZipFile

from os import environ
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame
import pygame.freetype

class Window:
    def renderFrame(self):
        background_color = (255, 255, 255) # flashbang o_O

        self.__screen.fill(background_color)
        
        # https://images-ext-1.discordapp.net/external/JBZ3yVKtL-rx2ZbgqjePnzMIjqhqTB8ETpE9KI3n-Q4/https/media.tenor.com/n5rrafoDxAUAAAPo/pan-cake.mp4

        for object in self.__frame["Objects"]:

            if self.__frame["Objects"][object].getVisible():
                oldObject = self.__frame["Objects"][object]
                
                if self.__packed and oldObject.getIsImage() and not(oldObject.getImage().startswith(self.__subPath)):
                    oldObject.setImage(self.__subPath + oldObject.getImage())
                
                renderedObject = Rendering.calculateObjectSize(oldObject, self.__size, self.config["Layout"]["Grid"])
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
        for object in self.__frame["Objects"]:
            self.__frame["Objects"][object].onStatic()
        self.renderFrame()

    def __init__(self, config: str, subPath="", packedCheck=False):
        self.__subPath = subPath
        self.__packedCheck = packedCheck
        self.__packed = False
        if self.__packedCheck and os.path.exists("packed"):
            self.__packed = True

            n = 4*3//4

            packedFile = ZipFile("packed", "r")
            self.__tempDirectory = "PCK-" + secrets.token_urlsafe(n)
            os.mkdir(self.__tempDirectory, 0o666)
            subprocess.check_call(["attrib","+H",self.__tempDirectory])

            packedFile.extractall(self.__tempDirectory)
            packedFile.close()

            self.__subPath = self.__tempDirectory + "/"

        self.config = read_ini(self.__subPath + config)

        self.Frames = {}

        for frame in self.config["Layout"]["Frames"].split("\",\""):
            self.Frames[frame] = read_ini(self.__subPath + frame)
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

        def objectCheck(event, object: Object):
            collissionRect = object.getCollissionRect()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if collissionRect.collidepoint(event.pos):
                    object.onActive()
                    self.renderFrame()
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if collissionRect.collidepoint(event.pos):
                    object.onClicked()
                    self.renderFrame()
            elif event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0] and collissionRect.collidepoint(event.pos):
                    object.onActive()
                elif collissionRect.collidepoint(event.pos):
                    object.onHover()
                    self.renderFrame()
                else:
                    object.onStatic()
                    self.renderFrame()
        
        while running:
            for event in pygame.event.get():
                for object in self.__frame["Objects"]:
                    try:
                        if self.__frame["Objects"][object].getVisible():
                            objectCheck(event, self.__frame["Objects"][object])
                    except KeyError:
                        pass
                if event.type == pygame.QUIT: 
                    if self.__packed:
                        shutil.rmtree(self.__tempDirectory)
                    running = False
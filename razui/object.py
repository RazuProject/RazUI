from .render import *
from PIL import Image as image

from os import environ
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame

class Object:
    def __init__(self, object: dict):
        self.__areaWidth = [eval(i) for i in object["AreaWidth"].split(":")]
        self.__areaHeight = [eval(i) for i in object["AreaHeight"].split(":")]
        self.__renderText = False
        self.__label = ""
        self.__labelAlign = "left"
        self.__type = object["Type"]
        self.__hoverBinded = []
        self.__activeBinded = []
        self.__clickBinded = []
        self.__visible = True
        self.__imagePath = ""
        self.__isImage = False

        try:
            self.__labelSize = int(object["LabelSize"])
        except:
            self.__labelSize = 16

        match self.__type:
            case "Button":
                self.__sprites = Renderer.spritesFromSpriteSheet(image.open("razui/default_assets/button.png"), (12,12))
                self.__sprite = self.__sprites[0]
                self.__spriteBorderWidth = 4
                self.__renderText = True
                self.__label = object["Label"]
                try:
                    self.__labelAlign = object["LabelAlign"]
                except:
                    self.__labelAlign = "Center"
            case "Label":
                self.__sprite = image.open("razui/default_assets/label.png")
                self.__spriteBorderWidth = 4
                self.__renderText = True
                self.__label = object["Label"]
                try:
                    self.__labelAlign = object["LabelAlign"]
                except:
                    self.__labelAlign = "Left"
            case "Image":
                self.__renderText = False
                self.__isImage = True
                try:
                    self.__imagePath = object["Image"]
                    self.__image = image.open(self.__imagePath)
                except:
                    pass

    def getCollissionRect(self) -> pygame.rect:
        return self.getPygameSprite().get_rect(topleft=self.getPosition())

    def renderSprite(self, spriteSize: tuple):
        if self.__type == "Image":
            try:
                self.__renderedSprite = self.__image.resize(spriteSize).convert("RGBA")
            except:
                self.__renderedSprite = Renderer.generateFallbackImage(Renderer, spriteSize)
        else:
            self.__renderedSprite = Renderer.generateSplitSpritesheetFrameImage(self.__sprite, self.__spriteBorderWidth, spriteSize)
    def getRenderedSprite(self) -> image:
        return self.__renderedSprite

    def setPosition(self, position: tuple):
        self.__position = position
    def getPosition(self) -> tuple:
        return self.__position
    
    def getRenderText(self) -> bool:
        return self.__renderText
    
    def getLabel(self) -> str:
        return self.__label
    def setLabel(self, label: str):
        self.__label = label
    def getLabelSize(self):
        return self.__labelSize
    def setLabelSize(self, size: int):
        self.__labelSize = size
    def getLabelAlign(self) -> str:
        return self.__labelAlign
    def setLabelAlign(self, align: str):
        self.__labelAlign = align if align in ["Left","Center","Right"] else None
    
    def setPygameSprite(self, sprite):
        self.__pygameSprite = sprite
    def getPygameSprite(self):
        return self.__pygameSprite
    
    def getAreaWidth(self) -> list:
        return self.__areaWidth
    def getAreaHeight(self) -> list:
        return self.__areaHeight

    def setVisible(self, visible: bool):
        self.__visible = visible
    def getVisible(self) -> bool:
        return self.__visible
        
    def getIsImage(self) -> bool:
        return self.__isImage
    def setImage(self, path: str):
        self.__imagePath = path
        self.__image = image.open(self.__imagePath)
    def getImage(self) -> str:
        return self.__imagePath
    
    # ===== Events =====
    
    def bindEvent(self, event: str, func):
        match event:
            case "hover":
                self.__hoverBinded.append(func)
            case "active":
                self.__activeBinded.append(func)
            case "click":
                self.__clickBinded.append(func)

    def unbindEvent(self, event: str, func):
        match event:
            case "hover":
                self.__hoverBinded.remove(func)
            case "active":
                self.__activeBinded.remove(func)
            case "click":
                self.__clickBinded.remove(func)

    def onStatic(self):
        match self.__type:
            case "Button":
                self.__sprite = self.__sprites[0]
    def onHover(self):
        match self.__type:
            case "Button":
                self.__sprite = self.__sprites[1]
                for func in self.__hoverBinded: func()
    def onActive(self):
        match self.__type:
            case "Button":
                self.__sprite = self.__sprites[2]
                for func in self.__activeBinded: func()
    def onClicked(self):
        match self.__type:
            case "Button":
                self.__sprite = self.__sprites[1]
                for func in self.__clickBinded: func()

def getObjectsFromConfigFile(config: dict) -> dict:
    result = {}

    for object in config:
        result[object] = Object(config[object])

    return result
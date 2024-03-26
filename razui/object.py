from .render import *
from PIL import Image as image

class Object:
    def __init__(self, object: dict):
        self.areaWidth =[eval(i) for i in object["AreaWidth"].split(":")]
        self.areaHeight = [eval(i) for i in object["AreaHeight"].split(":")]

        match object["Type"]:
            case "Button":
                self.sprites = Renderer.spritesFromSpriteSheet(image.open("razui/default_assets/button.png"), (12,12))
                self.sprite = self.sprites[0]
                self.spriteBorderWidth = 4
            case "Label":
                self.sprite = image.open("razui/default_assets/label.png")
                self.spriteBorderWidth = 4

    def bindEvent(self):
        pass

    def renderSprite(self, spriteSize: tuple):
        self.renderedSprite = Renderer.generateSplitSpritesheetFrameImage(self.sprite, self.spriteBorderWidth, spriteSize)

    def setPosition(self, position: tuple):
        self.position = position

    def getRenderedSprite(self) -> image:
        return self.renderedSprite
    def getPosition(self) -> tuple:
        return self.position

class ContainerObject:
    def __init__(self, object: dict, children: dict):
        self.children = {}

        for child in children:
            if child in object["Children"].split(","): self.children[child] = children[child]

        print(self.children)
        print("creation of container object")

def getObjectsFromConfigFile(config: dict) -> dict:
    result = {}

    for object in config:
        objectType = config[object]["Type"]

        if objectType == "Container":
            result[object] = ContainerObject(config[object], config)
        elif objectType in ["Label", "Button"]:
            result[object] = Object(config[object])

    return result
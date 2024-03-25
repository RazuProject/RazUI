from .render import *

class Object:
    def __init__(self, object: dict):
        print("creation of button object")

        self.areaWidth =[eval(i) for i in object["AreaWidth"].split(":")]
        self.areaHeight = [eval(i) for i in object["AreaHeight"].split(":")]

        match object["Type"]:
            case "Button":
                print("creation of button object")
            case "Label":
                print("creation of label object")

    def bindEvent(self):
        pass
    

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
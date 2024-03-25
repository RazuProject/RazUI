from .ini import *
from .render import *
from .object import *

import random

from os import environ
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame

class Window:
    def __init__(self, config: str):
        self.config = read_ini(config)

        self.layout = read_ini(self.config["Layout"]["Frames"].split(",")[0])
        self.Objects = getObjectsFromConfigFile(self.layout)

        print("setted up??? (real!??????)")

        background_color = (255, 255, 255) # flashbang o_O
  
        screen = pygame.display.set_mode((self.config["Window"]["Width"],self.config["Window"]["Height"])) 
        
        pygame.display.set_caption(self.config["Window"]["Title"]) 
        
        screen.fill(background_color) 
        
        pygame.display.flip() 
        
        # https://images-ext-1.discordapp.net/external/JBZ3yVKtL-rx2ZbgqjePnzMIjqhqTB8ETpE9KI3n-Q4/https/media.tenor.com/n5rrafoDxAUAAAPo/pan-cake.mp4

        pygame.display.flip()
        
        running = True
        
        while running: 
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    running = False
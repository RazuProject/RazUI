from PIL import Image as image
from PIL import ImageDraw as imageDraw

from os import environ
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame

class Renderer:
    @staticmethod
    def generateSplitSpritesheetFrameImage(spriteSheet: image, borderWidth: int, newFrameSize: tuple) -> image:
        width, height = spriteSheet.size

        # pain
        topLeft = spriteSheet.crop((
            0,
            0,
            borderWidth,
            borderWidth
        ))
        topRight = spriteSheet.crop((
            width - borderWidth,
            0,
            width,
            borderWidth
        ))
        bottomLeft = spriteSheet.crop((
            0,
            height - borderWidth,
            borderWidth,
            height
        ))
        bottomRight = spriteSheet.crop((
            width - borderWidth,
            height - borderWidth,
            width,
            height
        ))
        # pain
        top = spriteSheet.crop((
            borderWidth,
            0,
            width - borderWidth,
            borderWidth
        ))
        left = spriteSheet.crop((
            0,
            borderWidth,
            borderWidth,
            height - borderWidth
        ))
        right = spriteSheet.crop((
            width - borderWidth,
            borderWidth,
            width,
            height - borderWidth
        ))
        bottom = spriteSheet.crop((
            borderWidth,
            height - borderWidth,
            width - borderWidth,
            height
        ))
        # pain
        center = spriteSheet.crop((
            borderWidth,
            borderWidth,
            width - borderWidth,
            height - borderWidth
        ))

        newWidth, newHeight = newFrameSize
        result = image.new(mode="RGBA", size=newFrameSize)

        result.paste(topLeft, (0,0))
        result.paste(topRight, (newWidth-borderWidth,0))
        result.paste(bottomLeft, (0,newHeight-borderWidth))
        result.paste(bottomRight, (newWidth-borderWidth,newHeight-borderWidth))

        if newWidth-borderWidth*2 > 0:
            top = top.resize((newWidth-borderWidth*2,borderWidth))
            result.paste(top, (borderWidth,0))
        
        if newWidth-borderWidth*2 > 0:
            bottom = bottom.resize((newWidth-borderWidth*2, borderWidth))
            result.paste(bottom, (borderWidth,newHeight-borderWidth))

        if newHeight-borderWidth*2 > 0:
            left = left.resize((borderWidth, newHeight-borderWidth*2))
            result.paste(left, (0,borderWidth))

        if newHeight-borderWidth*2 > 0:
            right = right.resize((borderWidth, newHeight-borderWidth*2))
            result.paste(right, (newWidth-borderWidth,borderWidth))
        
        if newWidth-borderWidth*2 > 0 and newHeight-borderWidth*2 > 0:
            center = center.resize((newWidth-borderWidth*2,newHeight-borderWidth*2))
            result.paste(center, (borderWidth,borderWidth))

        return result
    
    def generateFallbackImage(self, size: tuple) -> image:
        frame = self.generateSplitSpritesheetFrameImage(image.open("razui/default_assets/fallback_image.png"), 8, size)
        icon = image.open("razui/default_assets/icon.png")

        frameWidth, frameHeight = frame.size

        frame.paste(icon, (int(frameWidth/2)-8,int(frameHeight/2)-8))

        text = imageDraw.Draw(frame)
        textWidth = text.textlength(f"{frameWidth} x {frameHeight}")

        text.text((int((frameWidth-textWidth)/2),int(frameHeight/2)+32), f"{frameWidth}x{frameHeight}", (255,255,255), align="center")

        return frame

    @staticmethod
    def convertPillowImageToPygameImage(image: image) -> pygame.image:
        return pygame.image.fromstring(image.tobytes(), image.size, "RGBA")
    
    @staticmethod
    def spritesFromSpriteSheet(spriteSheet: image, spriteSize: tuple) -> image:
        sprites = []
        sheetWidth, sheetHeight = spriteSheet.size

        for y in range(0, sheetHeight, int(spriteSize[1])):
            for x in range(0, sheetWidth, spriteSize[0]):
                sprite = spriteSheet.crop((
                    x,
                    y,
                    x + spriteSize[0],
                    y + spriteSize[1]
                ))
                sprite = sprite.convert("RGBA")
                sprites.append(sprite)

        return sprites
    
    @staticmethod
    def reszizQASDFsdfoiüpkasdasdöskdaksdöaksdö():
        print("reszizQASDFsdfoiüpkasdasdöskdaksdöaksdö ;()")
        return "reszizQASDFsdfoiüpkasdasdöskdaksdöaksdö ;()"
    
    @staticmethod
    def fitnessGramPacerTest():
        print("The FitnessGram™ Pacer Test is a multistage aerobic capacity test that progressively gets more difficult as it continues. The 20 meter pacer test will begin in 30 seconds. Line up at the start. The running speed starts slowly, but gets faster each minute after you hear this signal. [beep] A single lap should be completed each time you hear this sound. [ding] Remember to run in a straight line, and run as long as possible. The second time you fail to complete a lap before the sound, your test is over. The test will begin on the word start. On your mark, get ready, start.")
    
    def do_thingy(self, size):
        im = image.new(mode="RGBA", size=size)
        im.show()

        data = im.tobytes()

        return pygame.image.fromstring(data, size, im.mode)
    
rendererThing = Renderer()

rendererThing.generateSplitSpritesheetFrameImage(image.open("razui/default_assets/fallback_image.png"), 8, (240, 160))
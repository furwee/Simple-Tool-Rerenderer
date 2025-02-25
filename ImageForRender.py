import colorsys
from collections import Counter

import numpy as np
from PIL import Image, ImageTk, ImageFilter, ImageEnhance


def generatePalette(dominantC, shadeCount=2):
    palette = []
    for i in range(0, len(dominantC)):
        for j in range(0, shadeCount):
            h, s, v = colorsys.rgb_to_hsv(dominantC[i][0] / 255.0, dominantC[i][1] / 255.0, dominantC[i][2] / 255.0)
            v_shade = j * 250 / shadeCount
            r, g, b = colorsys.hsv_to_rgb(h, s, v_shade)
            palette.append((int(r), int(g), int(b)))

    newPal = []
    for item in palette:
        if item not in newPal:
            newPal.append(item)
    # print(np.array(newPal))
    return [palette, newPal]


def closestColor(pixel, palette):
    # print("palette",palette)
    # print(pixel)
    pixel = np.array(pixel, dtype=np.int32)
    palette = np.array(palette, dtype=np.int32)
    distances = np.sum((palette - pixel) ** 2, axis=1)
    # print(distances)
    # print(np.argmin(distances))
    # print(palette[np.argmin(distances)])
    # print(pixel)
    return palette[np.argmin(distances)]


class ImageRender:

    def __init__(self, path: str):
        self.path = path
        self.image = Image.open(path)

    def resizeNT(self, targetSize=128):
        if "png" in self.path:
            self.convertRGB()
        if targetSize > 0:
            self.image = self.image.resize((int((self.getWidth() / (self.getWidth() / targetSize))),
                                            int(self.getHeight() / (self.getWidth() / targetSize))),
                                           Image.Resampling.NEAREST)
        return self.image

    def resize(self, dispSize=128):
        if "png" in self.path:
            self.convertRGB()
        if dispSize > 0:
            self.image = self.image.resize((int((self.getWidth() / (self.getWidth() / dispSize))),
                                            int(self.getHeight() / (self.getWidth() / dispSize))),
                                           Image.Resampling.LANCZOS)
        return self.image

    def getSize(self):
        return f" ({self.getWidth()},{self.getHeight()})"

    def getArea(self):
        return self.getHeight() * self.getWidth()

    def getWidth(self):
        # print(self.image.width)
        return self.image.width

    def getHeight(self):
        # print(self.image.height)
        return self.image.height

    def getPixel(self, x, y):
        return self.image.getpixel((x, y))

    def show(self):
        self.image.show()

    def save(self, path=""):
        self.image.save(path)

    def convertHSV(self):
        self.image = self.image.convert("HSV")

    def convertRGB(self):
        self.image = self.image.convert("RGB")

    def convertTK(self):
        return ImageTk.PhotoImage(self.image)

    def convertNP(self):
        # print(np.array(self.image))
        self.convertRGB()
        return np.array(self.image).reshape(-1, 3)

    def palette(self, colour, shadeCount):
        try:
            palette = generatePalette(self.domColour(colour), shadeCount)[1]
            paletteAsArray = np.array(palette)
            # print(paletteAsArray)

            paletteIMG = Image.new(mode='P', size=(len(paletteAsArray), 1))
            for i in range(0, len(paletteAsArray)):
                # print(palette[i])
                paletteIMG.putpixel((i, 0), palette[i])

            paletteIMG.save("testPalette.png")
            return paletteAsArray
        except ValueError:
            print("palette issue")

    def convertPart(self, paletteArr):
        imgArr = self.convertNP()
        newImgArr = self.changeImageColour(imgArr, paletteArr)
        newIMG = Image.new("RGB", (self.getWidth(), self.getHeight()))
        # print(newImgArr)
        newImgTU = tuple(map(tuple, newImgArr))

        # print(len(newImgTU))
        k = 0
        # print(self.getArea())
        for i in range(0, self.getHeight()):
            for j in range(0, self.getWidth() - 1):
                newIMG.putpixel((j, i), newImgTU[k])
                # print(k, newImgTU[k])
                if k == self.getArea():
                    break
                else:
                    k += 1
            if k == self.getArea():
                break
            else:
                k += 1
        return newIMG

    def crop(self):
        self.image = self.image.crop((0, 0, self.getWidth() - 1, self.getHeight()))

    def changeImageColour(self, imageArr, paletteArr):
        imageArr = imageArr.astype(np.uint8)
        paletteArr = paletteArr.astype(np.uint8)

        for i in range(self.getArea()):
            # newImageArrCoord = imageArr[i]
            # print(newImageArrCoord)
            imageArr[i] = closestColor(imageArr[i], paletteArr)
            # print(imageArr[i])
        return imageArr

    def domColour(self, topColour):
        imgArr = self.convertNP()

        # print(self.getWidth() * self.getHeight() / 3)
        # print(int(len(imgArr)/3))
        # print(pixels)
        colourCounts = Counter(map(tuple, imgArr))
        domC = [color for color, count in colourCounts.most_common(topColour) if count > 1]
        # print(colourCounts)
        # print(domC)
        return domC

    def scale(self, scale=1):
        imgArray = np.array(self.image)
        if scale < 20:
            self.image = Image.fromarray(np.repeat(np.repeat(imgArray, scale, axis=0), scale, axis=1))
        else:
            self.image = Image.fromarray(np.repeat(np.repeat(imgArray, 20, axis=0), scale, axis=1))

    def medianFilter(self):
        self.image = self.image.filter(ImageFilter.MedianFilter(size=1))

    def sharpen(self, sharp):
        enhancer = ImageEnhance.Sharpness(self.image)
        self.image = enhancer.enhance(sharp)

    def enhanceBrightness(self, bright):
        enhancer = ImageEnhance.Brightness(self.image)
        self.image = enhancer.enhance(bright)


def main():
    pass


main()

if __name__ == "__main__": main()

import colorsys
from array import array
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


def RGBtoHSV(rgb):  # unutbu
    rgb = rgb.astype('float')
    hsv = np.zeros_like(rgb)
    hsv[..., 3:] = rgb[..., 3:]
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    maxc = np.max(rgb[..., :3], axis=-1)
    minc = np.min(rgb[..., :3], axis=-1)
    hsv[..., 2] = maxc
    mask = maxc != minc
    hsv[mask, 1] = (maxc - minc)[mask] / maxc[mask]
    rc = np.zeros_like(r)
    gc = np.zeros_like(g)
    bc = np.zeros_like(b)
    rc[mask] = (maxc - r)[mask] / (maxc - minc)[mask]
    gc[mask] = (maxc - g)[mask] / (maxc - minc)[mask]
    bc[mask] = (maxc - b)[mask] / (maxc - minc)[mask]
    hsv[..., 0] = np.select(
        [r == maxc, g == maxc], [bc - gc, 2.0 + rc - bc], default=4.0 + gc - rc)
    hsv[..., 0] = (hsv[..., 0] / 6.0) % 1.0
    return hsv


def HSVtoRGB(hsv):  # unutbu
    rgb = np.empty_like(hsv)
    rgb[..., 3:] = hsv[..., 3:]
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    i = (h * 6.0).astype('uint8')
    f = (h * 6.0) - i
    p = v * (1.0 - s)
    q = v * (1.0 - s * f)
    t = v * (1.0 - s * (1.0 - f))
    i = i % 6
    conditions = [s == 0.0, i == 1, i == 2, i == 3, i == 4, i == 5]
    rgb[..., 0] = np.select(conditions, [v, q, p, p, t, v], default=v)
    rgb[..., 1] = np.select(conditions, [v, v, v, q, p, p], default=t)
    rgb[..., 2] = np.select(conditions, [v, p, t, v, v, q], default=p)
    return rgb.astype('uint8')


def hue(arr, hueV):
    hsv = RGBtoHSV(arr)
    hsv[..., 0] = hueV
    rgb = HSVtoRGB(hsv)
    return rgb


class ImageRender:

    def __init__(self, path: str = None):
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

    def resizeLC(self, targetSize=128):
        if "png" in self.path:
            self.convertRGB()
        if targetSize > 0:
            self.image = self.image.resize((int((self.getWidth() / (self.getWidth() / targetSize))),
                                            int(self.getHeight() / (self.getWidth() / targetSize))),
                                           Image.Resampling.LANCZOS)
        return self.image

    def resize(self, targetSize=128):
        if "png" in self.path:
            self.convertRGB()
        if targetSize > 0:
            self.image = self.image.resize((int((self.getWidth() / (self.getWidth() / targetSize))),
                                            int(self.getHeight() / (self.getWidth() / targetSize))),
                                           )
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

    def palette(self, colour, shadeCount, hueV):
        try:
            palette = generatePalette(self.domColour(colour), shadeCount)[1]
            paletteAsArray = np.array(palette)
            paletteAsArray = hue(paletteAsArray, hueV)
            # print(paletteAsArray)

            paletteIMG = Image.new(mode='P', size=(len(paletteAsArray), 1))
            for i in range(0, len(paletteAsArray)):
                # print(palette[i])
                paletteIMG.putpixel((i, 0), palette[i])

            paletteIMG.save("_internal\\Asset\\testPalette.png")
            return paletteAsArray
        except ValueError:
            print("palette issue")
            return ImageRender("_internal\\asset\\testPremadePalette.png").convertNP()

    def convertPartPPM(self, paletteArr):
        imgArr = self.convertNP()
        newImgArr = self.changeImageColour(imgArr, paletteArr)
        newIMGLi = newImgArr.flatten().tolist()
        ppmHeader = f"P6 {self.getWidth()} {self.getHeight()} 255\n"
        newIMGPPMArr = array('B', newIMGLi)
        ppm = open('_internal\\asset\\hidden.ppm', 'wb')
        ppm.write(bytearray(ppmHeader, 'ascii'))
        newIMGPPMArr.tofile(ppm)
        ppm.close()
        newIMGPPM = Image.open("_internal\\asset\\hidden.ppm")
        self.image = newIMGPPM

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
            for j in range(0, self.getWidth()):
                newIMG.putpixel((j, i), newImgTU[k])
                k += 1
        self.image = newIMG

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
            return self.image
        else:
            self.image = Image.fromarray(np.repeat(np.repeat(imgArray, 20, axis=0), scale, axis=1))
            return self.image

    def medianFilter(self):
        self.image = self.image.filter(ImageFilter.MedianFilter)

    def sharpen(self, sharp):
        enhancer = ImageEnhance.Sharpness(self.image)
        self.image = enhancer.enhance(sharp)

    def colorLvl(self, colorlvl):
        enhancer = ImageEnhance.Color(self.image)
        self.image = enhancer.enhance(colorlvl)

    def enhanceBrightness(self, bright):
        enhancer = ImageEnhance.Brightness(self.image)
        self.image = enhancer.enhance(bright)

    def getfileName(self):
        return self.path


def main():
    pass


main()

if __name__ == "__main__": main()

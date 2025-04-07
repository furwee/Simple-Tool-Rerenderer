from array import array
import numpy as np
from numba import jit
from PIL import Image, ImageTk, ImageEnhance
from collections import Counter


@jit(nopython=True)
def generatePalette(dominantC, shadeCount: int = 2):
    palette = []
    for colour in dominantC:
        print(colour)
        for j in range(0, 255, 255//shadeCount):
            vShade = j / 255
            r = int(colour[0] * vShade)
            g = int(colour[1] * vShade)
            b = int(colour[2] * vShade)
            palette.append((r, g, b))

    newPal = []
    for item in palette:
        if item not in newPal:
            newPal.append(item)
    # print(newPal)
    return newPal


@jit(nopython=True)
def closestColorJit(pixel, palette):
    minDistance = float('inf')
    closestColor = None
    for color in palette:
        dist = 0.0
        for p, c in zip(pixel, color):
            dist += (p - c) ** 2
        if dist < minDistance:
            minDistance = dist
            closestColor = color
    return closestColor


def warmUP():
    imageArr = ImageRender("asset\\test.jpg").convertNP().astype(np.int32)
    paletteArr = ImageRender("asset\\testPremadePalette.png").convertNP().astype(np.int32)
    for i in imageArr:
        closestColorJit(i, paletteArr)


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


def hue(arr, hueV=-1):
    if hueV == -1:
        return arr
    else:
        hueV /= 360
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

    def save(self, path=""):
        self.image.save(path)

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
            palette = generatePalette(self.domColour(colour), shadeCount)
            paletteAsArray = np.array(palette)
            paletteAsArray = hue(paletteAsArray, hueV)
            return paletteAsArray
        except ValueError:
            print("palette issue")
            return ImageRender("asset\\testPremadePalette.png").convertNP()

    def convertPartPPM(self, paletteArr):
        newImgArr = self.changeImageColour(self.convertNP(), np.array(paletteArr).astype(np.int32))
        newIMGLi = newImgArr.flatten().tolist()
        ppmHeader = f"P6 {self.getWidth()} {self.getHeight()} 255\n"
        newIMGPPMArr = array('B', newIMGLi)
        ppm = open('asset\\hidden.ppm', 'wb')
        ppm.write(bytearray(ppmHeader, 'ascii'))
        newIMGPPMArr.tofile(ppm)
        ppm.close()
        newIMGPPM = Image.open("asset\\hidden.ppm")
        self.image = newIMGPPM

    def changeImageColour(self, imageArr, paletteArr):
        for i in range(self.getArea()):
            imageArr[i] = closestColorJit(imageArr[i], paletteArr)
        return imageArr

    def domColour(self, colour: int = 5):
        imgArr = self.convertNP()
        colourCounts = Counter(map(tuple, imgArr))
        domC = [color for color, count in colourCounts.most_common(colour) if count > 1]
        return domC


    def scale(self, scale=1):
        imgArray = np.array(self.image)
        if scale < 20:
            self.image = Image.fromarray(np.repeat(np.repeat(imgArray, scale, axis=0), scale, axis=1))
            return self.image
        else:
            self.image = Image.fromarray(np.repeat(np.repeat(imgArray, 20, axis=0), scale, axis=1))
            return self.image

    def sharpen(self, sharp):
        enhancer = ImageEnhance.Sharpness(self.image)
        self.image = enhancer.enhance(sharp)

    def enhanceBrightness(self, bright):
        enhancer = ImageEnhance.Brightness(self.image)
        self.image = enhancer.enhance(bright)

    def getfileName(self):
        return self.path


def main():
    pass


main()

if __name__ == "__main__": main()

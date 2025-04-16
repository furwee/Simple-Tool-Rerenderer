from array import array
import numpy as np
from numba import jit
from colorsys import *
from PIL import Image, ImageTk, ImageEnhance
from sklearn.cluster import MiniBatchKMeans


# noinspection PyTypeChecker
def LiconvertToPPMToImage(Li, header, fileName):
    newIMGPPMArr = array('B', Li)
    ppm = open(f'asset\\{fileName}.ppm', 'wb')
    ppm.write(bytearray(header, 'ascii'))
    newIMGPPMArr.tofile(ppm)
    ppm.close()


def generatePalette(dominantC, shadeCount: int = 2):
    palette = []
    for colour in dominantC:
        if shadeCount == 1:
            return dominantC
        else:
            for j in range(0, 255, 255 // shadeCount):
                vShade = j / 255
                r = int(colour[0] * vShade)
                g = int(colour[1] * vShade)
                b = int(colour[2] * vShade)
                rgb = (int(r), int(g), int(b))
                if rgb not in palette:
                    palette.append((r, g, b))
    return np.array(palette).reshape(-1, 3).astype(np.int32)


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


def hue(arr, hueV=-1):
    if hueV == -1:
        return arr
    else:
        arr2 = arr.copy()
        for i in range(arr2.shape[0]):
            r, g, b = arr2[i] / 255
            h, s, v = rgb_to_hsv(r, g, b)
            h = hueV / 360
            if s > 0.04:
                s = min(max(s * 1.5, 0.5), 1.0)
            r, g, b = hsv_to_rgb(h, s, v)
            arr2[i] = (r * 255, g * 255, b * 255)
    return arr2


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

    def palette(self, kMean, shadeCount, hueV):
        try:
            palette = generatePalette(self.adaptiveConvertToPalPreset(kMean), shadeCount)
            huePalette = hue(palette, hueV)
            return huePalette
        except ValueError:
            print("palette issue")
            return ImageRender("asset\\testPremadePalette.png").convertNP()

    def convertPartPPM(self, paletteArr):
        # print(paletteArr)
        newImgArr = self.changeImageColour(self.convertNP(), np.array(paletteArr).astype(np.int32))
        newIMGLi = newImgArr.flatten().tolist()
        ppmHeader = f"P6 {self.getWidth()} {self.getHeight()} 255\n"
        LiconvertToPPMToImage(newIMGLi, ppmHeader, "hidden")
        self.selfImageUpdate()

    def adaptiveConvertToPalPreset(self, kMean):
        imgArr = self.convertNP().astype(np.int32)
        kMeans = MiniBatchKMeans(n_clusters=kMean, compute_labels=False, max_no_improvement=1)
        kMeans.fit(imgArr.reshape(-1, 1))
        labels = kMeans.predict(imgArr.reshape(-1, 1))
        qX = kMeans.cluster_centers_[labels]
        qImg = np.uint8(qX.reshape(-1, 3)).tolist()
        return qImg

    def changeImageColour(self, imageArr, paletteArr):
        for i in range(self.getArea()):
            imageArr[i] = closestColorJit(imageArr[i], paletteArr)
        return imageArr

    def selfImageUpdate(self):
        newIMGPPM = Image.open("asset\\hidden.ppm")
        self.image = newIMGPPM

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

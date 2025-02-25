import tkinter as tk
from tkinter import filedialog

from ImageForRender import *


class TKGUI:
    def __init__(self, root):
        self.root = root
        root.title("Simple Tool Rerender (Made by Furwee,collab with someone0s)")
        self.openFilePath = ""
        self.saveFilePath = "Downloads/save.jpg"
        self.newIMG = ImageRender("test.jpg")
        self.dispSize = 512

        self.frameMaster = tk.Frame(self.root)
        self.frameMaster.grid(row=0, column=0)

        # top section
        self.frameTop = tk.Frame(self.frameMaster)  # ultilities: open image button, convert button, save button
        self.frameTop.grid(row=0, column=0, sticky=tk.N, padx=5, pady=5)

        self.imageOpen1 = tk.Button(self.frameTop, text="open image", command=self.openImage)
        self.imageOpen1.grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)

        self.imageConvertAdaptive1 = tk.Button(self.frameTop, text="convert image (adaptive)",
                                               command=self.convertImageAdaptive)
        self.imageConvertAdaptive1.grid(row=0, column=1, sticky=tk.N, padx=5, pady=5)

        self.imageConvertPremade1 = tk.Button(self.frameTop, text="convert image (premade)",
                                              command=self.convertImagePremade)
        self.imageConvertPremade1.grid(row=0, column=2, sticky=tk.N, padx=5, pady=5)

        self.imageSave1 = tk.Button(self.frameTop, text="save image", command=self.saveImage)
        self.imageSave1.grid(row=0, column=3, sticky=tk.W, padx=5, pady=5)

        self.defaultButton1 = tk.Button(self.frameTop, text="default", command=self.default)
        self.defaultButton1.grid(row=0, column=4, sticky=tk.W, padx=5, pady=5)

        # middle high section
        self.frameMidHigh = tk.Frame(self.frameMaster)  # image section: original image, new Image
        self.frameMidHigh.grid(row=1, column=0, sticky=tk.S, padx=5, pady=5)

        self.originalIMGDisp = tk.Label(self.frameMidHigh)
        self.originalIMGDisp.grid(row=0, column=0, padx=5, pady=5)

        self.originalIMGLabel = tk.Label(self.frameMidHigh, text="")
        self.originalIMGLabel.grid(row=1, column=0, padx=5, pady=5)

        self.newIMGDisp = tk.Label(self.frameMidHigh)
        self.newIMGDisp.grid(row=0, column=2, padx=5, pady=5)

        self.newIMGLabel = tk.Label(self.frameMidHigh, text="")
        self.newIMGLabel.grid(row=1, column=2, padx=5, pady=5)

        # middle section
        self.frameMiddle = tk.Frame(self.frameMaster)  # ultilities: open image button, convert button, save button
        self.frameMiddle.grid(row=2, column=0, sticky=tk.N, padx=5, pady=5)

        self.imageOpen = tk.Button(self.frameMiddle, text="open image", command=self.openImage)
        self.imageOpen.grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)

        self.imageConvertAdaptive = tk.Button(self.frameMiddle, text="convert image (adaptive)",
                                              command=self.convertImageAdaptive)
        self.imageConvertAdaptive.grid(row=0, column=1, sticky=tk.N, padx=5, pady=5)

        self.imageConvertPremade = tk.Button(self.frameMiddle, text="convert image (premade)",
                                             command=self.convertImagePremade)
        self.imageConvertPremade.grid(row=0, column=2, sticky=tk.N, padx=5, pady=5)

        self.imageSave = tk.Button(self.frameMiddle, text="save image", command=self.saveImage)
        self.imageSave.grid(row=0, column=3, sticky=tk.W, padx=5, pady=5)

        self.defaultButton = tk.Button(self.frameMiddle, text="default", command=self.default)
        self.defaultButton.grid(row=0, column=4, sticky=tk.W, padx=5, pady=5)

        # bottom section
        self.frameBottom = tk.Frame(self.frameMaster)  # resizeSize,colour,kmean
        self.frameBottom.grid(row=3, column=0)

        self.colourL = tk.Label(self.frameBottom, text="Number of Colour (min 1)")
        self.colourL.grid(row=0, column=0, padx=5, pady=5)
        self.colour = tk.Entry(self.frameBottom)
        self.colour.grid(row=1, column=0, padx=5, pady=5)
        self.colour.insert(0, "8")
        self.colourV = int(self.colour.get())

        self.tgtSizeL = tk.Label(self.frameBottom, text="Target Size (px)")
        self.tgtSizeL.grid(row=0, column=1, padx=5, pady=5)
        self.tgtSize = tk.Entry(self.frameBottom)
        self.tgtSize.insert(0, "128")
        self.tgtSizeV = int(self.tgtSize.get())
        self.tgtSize.grid(row=1, column=1, padx=5, pady=5)

        self.shadeCountL = tk.Label(self.frameBottom, text="Shade Count (min 2)")
        self.shadeCountL.grid(row=0, column=2, padx=5, pady=5)
        self.shadeCount = tk.Entry(self.frameBottom)
        self.shadeCount.insert(0, "8")
        self.shadeCountV = int(self.shadeCount.get())
        self.shadeCount.grid(row=1, column=2, padx=5, pady=5)

        self.brightnessL = tk.Label(self.frameBottom, text="brightness (float)")
        self.brightnessL.grid(row=0, column=3, padx=5, pady=5)
        self.brightness = tk.Entry(self.frameBottom)
        self.brightness.insert(0, "1")
        self.brightnessV = int(self.shadeCount.get())
        self.brightness.grid(row=1, column=3, padx=5, pady=5)

        self.sharpnessL = tk.Label(self.frameBottom, text="sharpness (float)")
        self.sharpnessL.grid(row=0, column=4, padx=5, pady=5)
        self.sharpness = tk.Entry(self.frameBottom)
        self.sharpness.insert(0, "1")
        self.sharpnessV = int(self.shadeCount.get())
        self.sharpness.grid(row=1, column=4, padx=5, pady=5)

        self.scaleL = tk.Label(self.frameBottom, text="Scale")
        self.scaleL.grid(row=0, column=5, padx=5, pady=5)
        self.scale = tk.Entry(self.frameBottom)
        self.scale.insert(0, "1")
        self.scaleV = int(self.scale.get())
        self.scale.grid(row=1, column=5, padx=5, pady=5)

        self.scaleC = tk.Button(self.frameBottom, text="scale", command=self.scaleS)
        self.scaleC.grid(row=1, column=6, sticky=tk.W, padx=5, pady=5)

    def openImage(self):
        self.originalIMGDisp.Image = None
        filePath = filedialog.askopenfilename(filetypes=[("Image files", "")])
        self.openFilePath = filePath
        if self.openFilePath:
            pic = ImageRender(self.openFilePath)
            filePath = filePath + str(pic.getSize())
            pic.resize(self.dispSize)
            pic.medianFilter()
            picTK = pic.convertTK()
            self.originalIMGDisp.config(image=picTK)
            self.originalIMGDisp.Image = picTK
            self.originalIMGLabel.config(text=filePath)

    def saveImage(self):
        filePath = filedialog.asksaveasfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        self.newIMG.save(filePath)
        # self.newIMG.show()

    def convertImageAdaptive(self):
        self.tgtSizeV = int(self.tgtSize.get())
        self.colourV = int(self.colour.get())
        self.shadeCountV = int(self.shadeCount.get())
        self.brightnessV = float(self.brightness.get())
        self.sharpnessV = float(self.sharpness.get())
        self.scaleV = int(self.scale.get())
        img = ImageRender("test.jpg")
        img.resize(self.tgtSizeV)
        self.newIMGDisp.config(image=img.convertTK())
        self.newIMGDisp.Image = None
        self.newIMG = ImageRender(self.openFilePath)
        pic = self.newIMG
        pic.medianFilter()
        pic.resizeNT(targetSize=self.tgtSizeV)
        pic.resize(self.tgtSizeV)
        pic.medianFilter()
        pic.sharpen(self.sharpnessV)
        pic2 = pic
        pic2 = pic2.palette(colour=self.colourV, shadeCount=self.shadeCountV)
        pic = pic.convertPart(pic2)
        pic.save("Saved.png")
        pic = ImageRender("Saved.png")
        pic.medianFilter()
        pic.sharpen(self.sharpnessV)
        pic.enhanceBrightness(self.brightnessV)
        pic.crop()
        pic.scale(self.scaleV)
        picTK = pic.convertTK()
        self.newIMGDisp.config(image=picTK)
        self.newIMGDisp.Image = picTK
        self.newIMGLabel.config(text=pic.getSize())
        self.newIMG.Text = pic.getSize()
        self.newIMG = pic

    def convertImagePremade(self):
        self.tgtSizeV = int(self.tgtSize.get())
        self.brightnessV = float(self.brightness.get())
        self.sharpnessV = float(self.sharpness.get())
        self.scaleV = float(self.scale.get())
        img = ImageRender("test.jpg")
        img.resize(self.tgtSizeV)
        self.newIMGDisp.config(image=img.convertTK())
        self.newIMGDisp.Image = None
        self.newIMG = ImageRender(self.openFilePath)
        pic = self.newIMG
        pic.medianFilter()
        pic.resizeNT(targetSize=self.tgtSizeV)
        pic.resize(self.tgtSizeV)
        pic.medianFilter()
        pic.sharpen(self.sharpnessV)
        pic2 = ImageRender("testPremadePalette.png").convertNP()
        pic = pic.convertPart(pic2)
        pic.save("Saved.png")
        pic = ImageRender("Saved.png")
        # pic.medianFilter()
        pic.sharpen(self.sharpnessV)
        pic.enhanceBrightness(self.brightnessV)
        pic.crop()
        pic.scale(self.scaleV)
        picTK = pic.convertTK()
        self.newIMGDisp.config(image=picTK)
        self.newIMGDisp.Image = picTK
        self.newIMGLabel.config(text=pic.getSize())
        self.newIMGLabel.Text = pic.getSize()
        self.newIMG = pic

    def scaleS(self):
        self.scaleV = float(self.scale.get())
        pic = ImageRender("Saved.png")
        # pic.medianFilter()
        pic.sharpen(self.sharpnessV)
        pic.enhanceBrightness(self.brightnessV)
        pic.crop()
        pic.scale(self.scaleV)
        picTK = pic.convertTK()
        self.newIMGDisp.config(image=picTK)
        self.newIMGDisp.Image = picTK
        self.newIMGLabel.config(text=pic.getSize())
        self.newIMG.Text = pic.getSize()
        self.newIMG = pic

    def default(self):
        self.colour.delete(0, 'end')
        self.colour.insert(0, "8")
        self.tgtSize.delete(0, 'end')
        self.tgtSize.insert(0, "128")
        self.shadeCount.delete(0, 'end')
        self.shadeCount.insert(0, "8")
        self.brightness.delete(0, 'end')
        self.brightness.insert(0, "1")
        self.sharpness.delete(0, 'end')
        self.sharpness.insert(0, "1")
        self.scale.delete(0, 'end')
        self.scale.insert(0, "4")


def main():
    rootTK = tk.Tk()
    rootTK.resizable(False, False)
    rootTK.iconbitmap("STR_Logo_PA.ico")
    TKGUI(rootTK)
    rootTK.mainloop()


if __name__ == "__main__": main()

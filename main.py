import tkinter as tk
from tkinter import filedialog, messagebox
from time import *
from asset.ImageForRender import *
from asset.Stack import *
import os


class TKGUI:
    def __init__(self, root):
        self.root = root
        root.title("Simple Tool Rerender v0.0.62 (Made by Furwee,collab with someone0s)")
        self.openFilePath = ""
        self.saveFilePath = ""
        self.imageStack = Stack(None)
        self.newIMG = ImageRender("asset\\test.jpg")
        self.dispSize = 512
        self.palette = ImageRender("asset\\testPremadePalette.png").convertNP()
        self.k = 0
        self.openedImage = None
        self.ADAFLAG = False

        self.frameMaster = tk.Frame(self.root)
        self.frameMaster.grid(row=0, column=0)

        # top section
        self.frameTop = tk.Frame(self.frameMaster)  # ultilities: open image button, convert button, save button
        self.frameTop.grid(row=0, column=0, padx=5, pady=5)

        self.imageOpen1 = tk.Button(self.frameTop, text="open image", command=self.openImage)
        self.imageOpen1.grid(row=0, column=0, padx=5, pady=5)

        self.imageConvertAdaptive1 = tk.Button(self.frameTop, text="convert image (adaptive)",
                                               command=lambda: self.convertImage(True))
        self.imageConvertAdaptive1.grid(row=0, column=1, padx=5, pady=5)

        self.importPalette1 = tk.Button(self.frameTop, text="import palette", command=self.importPalette)
        self.importPalette1.grid(row=0, column=2, padx=5, pady=5)

        self.imageConvertPremade1 = tk.Button(self.frameTop, text="convert image (premade)",
                                              command=self.convertImage)
        self.imageConvertPremade1.grid(row=0, column=3, sticky=tk.N, padx=5, pady=5)

        self.imageSave1 = tk.Button(self.frameTop, text="save image", command=self.saveImage)
        self.imageSave1.grid(row=0, column=4, padx=5, pady=5)

        self.defaultButton1 = tk.Button(self.frameTop, text="reset", command=self.default)
        self.defaultButton1.grid(row=0, column=5, padx=5, pady=5)

        # middle high section
        self.frameMidHigh = tk.Frame(self.frameMaster)  # image section: original image, new Image
        self.frameMidHigh.grid(row=1, column=0, padx=5, pady=5)

        self.originalIMGDisp = tk.Label(self.frameMidHigh)
        self.originalIMGDisp.grid(row=0, column=0, padx=5, pady=5)

        self.originalIMGLabel = tk.Label(self.frameMidHigh, text="")
        self.originalIMGLabel.grid(row=1, column=0, padx=5, pady=5)

        # Middle utilities
        self.frameIMGMID = tk.Frame(self.frameMidHigh)  # resizeSize,colour,kmean
        self.frameIMGMID.grid(row=0, column=1)

        self.frameStack = tk.Frame(self.frameIMGMID)
        self.frameStack.grid(row=0, column=0, padx=5, pady=5)
        self.undoB = tk.Button(self.frameStack, text="undo", command=self.undo, state=tk.DISABLED)
        self.undoB.grid(row=0, column=0, padx=5, pady=5)
        self.redoB = tk.Button(self.frameStack, text="redo", command=self.redo, state=tk.DISABLED)
        self.redoB.grid(row=0, column=1, padx=5, pady=5)

        self.colourL = tk.Label(self.frameIMGMID, text="kMean (min 1)")
        self.colourL.grid(row=1, column=0, padx=5, pady=5)
        self.colour = tk.Entry(self.frameIMGMID)
        self.colour.grid(row=2, column=0, padx=5, pady=5)
        self.colour.insert(0, "8")
        self.colourV = int(self.colour.get())

        self.tgtSizeL = tk.Label(self.frameIMGMID, text="Target Size (px)")
        self.tgtSizeL.grid(row=3, column=0, padx=5, pady=5)
        self.tgtSize = tk.Entry(self.frameIMGMID)
        self.tgtSize.insert(0, "128")
        self.tgtSizeV = int(self.tgtSize.get())
        self.tgtSize.grid(row=4, column=0, padx=5, pady=5)

        self.shadeCountL = tk.Label(self.frameIMGMID, text="Shade Count (min 2)")
        self.shadeCountL.grid(row=5, column=0, padx=5, pady=5)
        self.shadeCount = tk.Entry(self.frameIMGMID)
        self.shadeCount.insert(0, "8")
        self.shadeCountV = int(self.shadeCount.get())
        self.shadeCount.grid(row=6, column=0, padx=5, pady=5)

        self.hueL = tk.Label(self.frameIMGMID, text="hue (0-360)*, -1 for no hue change")
        self.hueL.grid(row=7, column=0, padx=5, pady=5)
        self.hue = tk.Entry(self.frameIMGMID)
        self.hue.insert(0, "-1")
        self.hueV = float(self.hue.get())
        self.hue.grid(row=8, column=0, padx=5, pady=5)

        self.brightnessL = tk.Label(self.frameIMGMID, text="brightness (float)")
        self.brightnessL.grid(row=9, column=0, padx=5, pady=5)
        self.brightness = tk.Entry(self.frameIMGMID)
        self.brightness.insert(0, "1")
        self.brightnessV = int(self.brightness.get())
        self.brightness.grid(row=10, column=0, padx=5, pady=5)

        self.bright = tk.Button(self.frameIMGMID, text="brighten", command=self.brightC)
        self.bright.grid(row=10, column=1, sticky=tk.W, padx=5, pady=5)

        self.sharpnessL = tk.Label(self.frameIMGMID, text="sharpness (float)")
        self.sharpnessL.grid(row=11, column=0, padx=5, pady=5)
        self.sharpness = tk.Entry(self.frameIMGMID)
        self.sharpness.insert(0, "1")
        self.sharpnessV = int(self.sharpness.get())
        self.sharpness.grid(row=12, column=0, padx=5, pady=5)

        self.sharp = tk.Button(self.frameIMGMID, text="sharpen", command=self.sharpC)
        self.sharp.grid(row=12, column=1, sticky=tk.W, padx=5, pady=5)

        self.scaleL = tk.Label(self.frameIMGMID, text="Scale")
        self.scaleL.grid(row=13, column=0, padx=5, pady=5)
        self.scale = tk.Entry(self.frameIMGMID)
        self.scale.insert(0, "1")
        self.scaleV = int(self.scale.get())
        self.scale.grid(row=14, column=0, padx=5, pady=5)

        self.scaleC = tk.Button(self.frameIMGMID, text="scale", command=self.scaleS)
        self.scaleC.grid(row=14, column=1, sticky=tk.W, padx=5, pady=5)

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
                                              command=lambda: self.convertImage(True))
        self.imageConvertAdaptive.grid(row=0, column=1, sticky=tk.N, padx=5, pady=5)

        self.importPaletteB = tk.Button(self.frameMiddle, text="import palette", command=self.importPalette)
        self.importPaletteB.grid(row=0, column=2, padx=5, pady=5)

        self.imageConvertPremade = tk.Button(self.frameMiddle, text="convert image (premade)",
                                             command=self.convertImage)
        self.imageConvertPremade.grid(row=0, column=3, sticky=tk.N, padx=5, pady=5)

        self.imageSave = tk.Button(self.frameMiddle, text="save image", command=self.saveImage)
        self.imageSave.grid(row=0, column=4, sticky=tk.W, padx=5, pady=5)

        self.defaultButton = tk.Button(self.frameMiddle, text="reset", command=self.default)
        self.defaultButton.grid(row=0, column=5, sticky=tk.W, padx=5, pady=5)

        # bottom section

    def importPalette(self, path=""):
        if path == "":
            filePath = filedialog.askopenfilename(filetypes=[("Image files", "")])
        if filePath:
            test = ImageRender(filePath)
            if test.getArea() < 300:
                self.palette = test.convertNP()
            else:
                self.palette = ImageRender("asset\\testPremadePalette.png").convertNP()

    def openImage(self):
        self.k = 0
        self.imageStack.last = 0
        if self.openFilePath != "":
            self.openedImage = True
        filePath = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        self.openFilePath = filePath
        if self.openFilePath:
            self.undoRedoChange()
            pic = ImageRender(self.openFilePath)
            pic.resizeLC(self.dispSize)
            pic.save(f"cache\\Saved(0).png")
            self.imageStack.list2stack = (
                [[pic,
                  [f"cache\\Saved(0).png", self.tgtSize.get(), self.colour.get(), self.shadeCount.get(), self.hue.get(),
                   self.brightness.get(),
                   self.sharpness.get(), self.scale.get()]]])
            filePath = filePath + str(ImageRender(self.openFilePath).getSize())
            picTK = pic.convertTK()
            self.originalIMGDisp.config(image=picTK)
            self.originalIMGDisp.Image = picTK
            self.originalIMGLabel.config(text=filePath)

    def saveImage(self):
        filePath = filedialog.asksaveasfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        self.imageStack.getCurrent()[0].save(filePath)
        # self.newIMG.show()

    def convertImage(self, adaptive=False):
        if self.openedImage:
            self.imageStack.last = 0
            self.openedImage = False
        self.k += 1
        try:
            self.tgtSizeV = int(self.tgtSize.get())
            self.colourV = int(self.colour.get())
            self.shadeCountV = int(self.shadeCount.get())
            self.brightnessV = float(self.brightness.get())
            self.sharpnessV = float(self.sharpness.get())
            self.scaleV = int(self.scale.get())
            self.hueV = float(self.hue.get())
        except ValueError:
            quit(1)
        img = ImageRender("asset\\test.jpg")
        self.newIMGDisp.config(image=img.convertTK())
        self.newIMGDisp.Image = None
        print(self.imageStack.list2stack[0][1][0])
        self.newIMG = ImageRender(self.imageStack.list2stack[0][1][0])
        pic = self.newIMG
        pic.convertRGB()
        # pic.resizeNT(targetSize=self.tgtSizeV)
        pic.resizeLC(self.tgtSizeV)
        pic.sharpen(self.sharpnessV)
        strt = time()
        if adaptive:
            pic2 = pic
            self.palette = pic2.palette(self.colourV, self.shadeCountV, self.hueV)
            self.ADAFLAG = True
        elif not adaptive and self.ADAFLAG:
            ans = tk.messagebox.askyesno(title="halt", message="press [YES] to import palette to replace the adaptive palette.\nPress [NO] if you don't intend to change the palette")
            if ans:
                self.importPalette()
            self.ADAFLAG = False
        pic.convertPartPPM(self.palette)
        end = time()
        print(end - strt)
        pic.save(f"cache\\Saved({self.k}).png")
        pic = ImageRender(f"cache\\Saved({self.k}).png")
        pic.sharpen(self.sharpnessV)
        pic.enhanceBrightness(self.brightnessV)

        pic.scale(self.scaleV)
        self.imageStack.push(
            [pic, [f"cache\\Saved({self.k}).png", self.tgtSize.get(), self.colour.get(), self.shadeCount.get(),
                   self.hue.get(),
                   self.brightness.get(),
                   self.sharpness.get(), self.scale.get()]])

        picTK = pic.convertTK()
        self.newIMGDisp.config(image=picTK)
        self.newIMGDisp.Image = picTK
        self.newIMGLabel.config(text=pic.getSize())
        self.newIMG.Text = pic.getSize()
        self.newIMG = pic
        self.undoRedoChange()

    def scaleS(self):
        self.undoRedoChange()
        self.scaleV = float(self.scale.get())
        pic = ImageRender(self.newIMG.getfileName())
        # pic.medianFilter()
        # pic.sharpen(self.sharpnessV)
        pic.enhanceBrightness(self.brightnessV)
        pic.sharpen(self.sharpnessV)
        pic.scale(self.scaleV)

        self.imageStack.push([pic, [pic.getfileName(), self.tgtSize.get(), self.colour.get(), self.shadeCount.get(),
                                    self.hue.get(), self.brightness.get(),
                                    self.sharpness.get(), self.scale.get()]])
        # print(self.imageStack.list2stack)
        picTK = pic.convertTK()
        self.newIMGDisp.config(image=picTK)
        self.newIMGDisp.Image = picTK
        self.newIMGLabel.config(text=pic.getSize())
        self.newIMG.Text = pic.getSize()
        self.newIMG = pic

    def brightC(self):
        self.undoRedoChange()
        self.brightnessV = float(self.brightness.get())
        pic = ImageRender(self.newIMG.getfileName())
        # pic.medianFilter()
        # pic.sharpen(self.sharpnessV)
        pic.enhanceBrightness(self.brightnessV)
        pic.sharpen(self.sharpnessV)
        pic.scale(self.scaleV)

        self.imageStack.push([pic, [pic.getfileName(), self.tgtSize.get(), self.colour.get(), self.shadeCount.get(),
                                    self.hue.get(), self.brightness.get(),
                                    self.sharpness.get(), self.scale.get()]])
        # print(self.imageStack.list2stack)
        picTK = pic.convertTK()
        self.newIMGDisp.config(image=picTK)
        self.newIMGDisp.Image = picTK
        self.newIMGLabel.config(text=pic.getSize())
        self.newIMG.Text = pic.getSize()
        self.newIMG = pic

    def sharpC(self):
        self.undoRedoChange()
        self.sharpnessV = float(self.sharpness.get())
        pic = ImageRender(self.newIMG.getfileName())
        # pic.medianFilter()
        # pic.sharpen(self.sharpnessV)
        pic.enhanceBrightness(self.brightnessV)
        pic.sharpen(self.sharpnessV)
        pic.scale(self.scaleV)

        self.imageStack.push([pic, [pic.getfileName(), self.tgtSize.get(), self.colour.get(), self.shadeCount.get(),
                                    self.hue.get(), self.brightness.get(),
                                    self.sharpness.get(), self.scale.get()]])
        # print(self.imageStack.list2stack)
        picTK = pic.convertTK()
        self.newIMGDisp.config(image=picTK)
        self.newIMGDisp.Image = picTK
        self.newIMGLabel.config(text=pic.getSize())
        self.newIMG.Text = pic.getSize()
        self.newIMG = pic

    def undo(self):
        # print(self.imageStack)
        self.undoRedoChange()
        pic = self.imageStack.undo()
        self.undoRedoChange()
        # print(self.imageStack.getCurrent())

        self.tgtSizeV = int(pic[1][1])
        self.colourV = int(pic[1][2])
        self.shadeCountV = int(pic[1][3])
        self.hueV = float(pic[1][4])
        self.brightnessV = float(pic[1][5])
        self.sharpnessV = float(pic[1][6])
        self.scaleV = int(pic[1][7])
        self.newIMG = ImageRender(pic[1][0])
        newIMGTK = self.newIMG

        self.colour.delete(0, 'end')
        self.colour.insert(0, str(self.colourV))
        self.tgtSize.delete(0, 'end')
        self.tgtSize.insert(0, str(self.tgtSizeV))
        self.shadeCount.delete(0, 'end')
        self.shadeCount.insert(0, str(self.shadeCountV))
        self.hue.delete(0, "end")
        self.hue.insert(0, str(self.hueV))
        self.brightness.delete(0, 'end')
        self.brightness.insert(0, str(self.brightnessV))
        self.sharpness.delete(0, 'end')
        self.sharpness.insert(0, str(self.sharpnessV))
        self.scale.delete(0, 'end')
        self.scale.insert(0, str(self.scaleV))

        newIMGTK.scale(self.scaleV)
        newIMGTK.enhanceBrightness(self.brightnessV)
        newIMGTK.sharpen(self.sharpnessV)
        picTK = newIMGTK.convertTK()
        self.newIMGDisp.config(image=picTK)
        self.newIMGDisp.Image = picTK
        self.newIMGLabel.config(text=self.newIMG.getSize())
        self.newIMGLabel.Text = self.newIMG.getSize()

    def redo(self):
        self.undoRedoChange()
        pic = self.imageStack.redo()
        self.undoRedoChange()
        # print(self.imageStack.getCurrent())

        self.tgtSizeV = int(pic[1][1])
        self.colourV = int(pic[1][2])
        self.shadeCountV = int(pic[1][3])
        self.hueV = int(pic[1][4])
        self.brightnessV = float(pic[1][5])
        self.sharpnessV = float(pic[1][6])
        self.scaleV = int(pic[1][7])
        self.newIMG = ImageRender(pic[1][0])
        newIMGTK = self.newIMG

        self.colour.delete(0, 'end')
        self.colour.insert(0, str(self.colourV))
        self.tgtSize.delete(0, 'end')
        self.tgtSize.insert(0, str(self.tgtSizeV))
        self.shadeCount.delete(0, 'end')
        self.shadeCount.insert(0, str(self.shadeCountV))
        self.hue.delete(0, "end")
        self.hue.insert(0, str(self.hueV))
        self.brightness.delete(0, 'end')
        self.brightness.insert(0, str(self.brightnessV))
        self.sharpness.delete(0, 'end')
        self.sharpness.insert(0, str(self.sharpnessV))
        self.scale.delete(0, 'end')
        self.scale.insert(0, str(self.scaleV))

        newIMGTK.scale(self.scaleV)
        newIMGTK.enhanceBrightness(self.brightnessV)
        newIMGTK.sharpen(self.sharpnessV)
        picTK = newIMGTK.convertTK()
        self.newIMGDisp.config(image=picTK)
        self.newIMGDisp.Image = picTK
        self.newIMGLabel.config(text=self.newIMG.getSize())
        self.newIMGLabel.Text = self.newIMG.getSize()

    def default(self):
        self.colour.delete(0, 'end')
        self.colour.insert(0, "8")
        self.tgtSize.delete(0, 'end')
        self.tgtSize.insert(0, "128")
        self.shadeCount.delete(0, 'end')
        self.shadeCount.insert(0, "8")
        self.hue.delete(0, "end")
        self.hue.insert(0, "0")
        self.brightness.delete(0, 'end')
        self.brightness.insert(0, "1")
        self.sharpness.delete(0, 'end')
        self.sharpness.insert(0, "1")
        self.scale.delete(0, 'end')
        self.scale.insert(0, "4")
        self.palette = ImageRender("asset\\testPremadePalette.png").convertNP()

    def undoRedoChange(self):
        # print("U", self.imageStack.last, self.imageStack.getSize())
        if self.imageStack.getSize() == 0 or self.imageStack.last == 1:
            self.undoB.config(state=tk.DISABLED)
        else:
            self.undoB.config(state=tk.NORMAL)
        # print("R", self.imageStack.last, self.imageStack.getSize())
        if self.imageStack.getSize() == 0 or self.imageStack.last == self.imageStack.getSize() - 1:
            self.redoB.config(state=tk.DISABLED)
        else:
            self.redoB.config(state=tk.NORMAL)


def main():
    try:
        os.makedirs("cache")
    except FileExistsError:
        pass
    finally:
        warmUP()
        rootTK = tk.Tk()
        rootTK.minsize(600, 600)
        # rootTK.resizable(False, False)
        rootTK.iconbitmap("asset\\STR_Logo_PA.ico")
        TKGUI(rootTK)
        rootTK.mainloop()


if __name__ == "__main__": main()

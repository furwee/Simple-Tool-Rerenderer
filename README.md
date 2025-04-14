# Simple Tool Rerenderer

## Current release: v0.0.62

This program is made to simulate pixel art without simply resizing/pixelating images.  
Therefore a palette is used to convert each pixels in the image to the closest colour on the palette.  
This program is made collaboratively by furwee and someone0s.

## Make sure you have these on your computer:
- Python >3.9
## How to use this program:
1: **clone the repository to the specified locations in your computer**  
find ```<> code``` at the top right of the repository, download zip to [folder location]<br><br>
2: use ```Win + R```, type cmd and do the following:  
```cd [folder location]```<br><br>
3: use **pip** to do the following command:  
```pip install -r requirements.txt``` <- installs modules  <br><br>
```pip list``` <- makes sure the modules are imported correctly <br><br>
4: once you made sure the modules are installed, do the following:  
```python main.py```  <br><br>
and there you go :) happy using the program!

## What image file formats does it support?

**.png, .jpg, .jpeg, .webp, .ico**

## Why is the exe version removed?
Mainly due to pyinstaller installing a bunch of useless dependencies.  
With the additional modules being downloaded separately, the program is lighter.

## To import palette, you may:  

### 1: draw your own array of pixels
Maxium area must be below 300 to prevent accidentally using images as array.  

### 2: download palette (1x) from lospec
lospec: https://lospec.com/palette-list or choose websites that you prefer

## Notes regarding this program:

### loading the program can take a while
The program needs to warm up using jit to speed up the processing speed on first user-imported image.
### First time processsing an image is slightly slower than normal
The program will run much faster in the next processes.

### It is ideal that the processed image's size is not larger than 512px for the following reasons:  
- interpolation may occur as optimisation is done to reduce processing time.
- most pixel art programs' canvas does not like to handle pixel arts bigger than 1024px.
- 512px processing time is still acceptably "instant"
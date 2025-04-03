# Simple Tool Rerenderer

## Current release: v0.0.61

This program is made to simulate pixel art without simply resizing/pixelating images.  
Therefore a palette is used to convert each pixels in the image to the closest colour on the palette.  
This program is made collaboratively by furwee and someone0s.

## What image file formats does it support?

**.png, .jpg, .jpeg, .webp**
## Why is V0.0.61 so large in file size?

Unfortunately the usage of numba (used to speed up pixel processing) requires llvmlite and it occupies almost half of the program's size...  
I will try to make it as lightweight as possible and maintaining its speed in future updates qwq


## To import palette, you may:  

### 1: draw your own array of pixels
Maxium area must be below 300 to prevent accidentally using images as array.  

### 2: download palette (1x) from lospec
lospec: https://lospec.com/palette-list or choose websites that you prefer

## Notes regarding this program:

### First time processsing an image is slightly slower than normal
The program will run much faster in the next processes.

### It is ideal that the processed image's size is not larger than 512px for the following reasons:  
- interpolation may occur as optimisation is done to reduce processing time.
- most pixel art programs' canvas does not like to handle pixel arts bigger than 1024px.
- 512px processing time is still acceptably "instant"
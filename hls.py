# Required imports
import numpy as np
import scipy.misc as smp
import matplotlib.pyplot as plt
import math
import colorsys

# A MagicaVoxel palette is organised as 32 rows of 8 columns
data = np.zeros( (32,8,3), dtype=np.float )

# Uses the provided (x,y) position to calculate an offset from the (cx, cy)
# centre of the disk and converts this to an angle which is treated as the
# hue. Saturation is then the distance from the centre of the disk, and the
#Lightness is explicitly provided rather than being computed.
def get_colour(x, y, cx, cy, lightness):

    # Calculate x and y distance to cetre of disk
    x_diff = x - cx
    y_diff = y - cy

    # Our dsk is six pixels high but eight wide. We compensate for
    # that here to make sure we cover the whole colour gamut.
    y_diff = y_diff * 1.3333
    
    # Compute the total distance
    dist = math.sqrt(x_diff*x_diff+y_diff*y_diff)

    # If the current pixel is in the disk then compute its colour
    if dist <= 4.0:
        theta = math.atan2(y_diff, x_diff) # Range from -pi to pi
        theta = theta + math.pi # Range from 0 to 2*pi
        theta = theta / (math.pi * 2.0) # Range from zero to one

        # Rotate our disk through 120 degrees to put green on the left.
        # This gives the full eight pixels to cover the range of green
        # (rather than only six pixels) which is ueful as the eye is more
        # sensitive to green than blue or red.
        theta, whole = math.modf(theta + 0.3333) # Still from zero to one
        
        # Build the RGB colour from the HLS colour and return
        hue = theta
        saturation = dist / 4.0
        rgb = colorsys.hls_to_rgb(hue, lightness, saturation)
        return [rgb[0], rgb[1], rgb[2]]

    # Otherwise just make it black.
    else:
        return [0.0,0.0,0.0]


# Generate each of the five disks
for x in range(0,8):
    for y in range(0,6):
        data[y,x] = get_colour(x, y, 3.5, 2.5, 5.0 / 6.0)
        
for x in range(0,8):
    for y in range(6,12):
        data[y,x] = get_colour(x, y, 3.5, 8.5, 4.0/6.0)
        
for x in range(0,8):
    for y in range(12,18):
        data[y,x] = get_colour(x, y, 3.5, 14.5, 3.0/6.0)
        
for x in range(0,8):
    for y in range(18,24):
        data[y,x] = get_colour(x, y, 3.5, 20.5, 2.0/6.0)
        
for x in range(0,8):
    for y in range(24,30):
        data[y,x] = get_colour(x, y, 3.5, 26.5, 1.0/6.0)


# MagicaVoxel palettes are actually stored as pngs of size 265x1 pixels
data = np.reshape(data, (1,256,3))

# The disks don't include pure grey values so write some out here
grey_start_pixel = 240
for i in range(1,17):
    grey = i / 16.0
    data[0, grey_start_pixel - 1 + i] = [grey, grey, grey]

# There's some messy jumping between 1D and 2D array's because I finished the
# code and then realised the palette was upside down. So it's back to 2D, flip
# it, and then back to 1D again to save.
data = np.reshape(data, (32,8,3))
data = np.flipud(data)
data = np.reshape(data, (1,256,3))
  
data = np.clip(data, 0, 1.0)
img = smp.toimage( data )

#plt.imshow(img, interpolation="nearest") # For debugging
smp.imsave('hls.png', img)
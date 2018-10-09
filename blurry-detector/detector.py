#!/usr/bin/python

import sys
import cv2
import numpy as np

def image_rescale(image, scale):
    """
    Rescale a given image using a given scale
    """
    # Input image size
    (H, W) = image.shape[:2]

    # Rescale height and width
    outH = round(H * scale, 0)      
    outW = round(W * scale, 0)

    # Output dimension
    dim = int(outW), int(outH)

    # Rescale and return
    rescaled = cv2.resize(image, dim, cv2.INTER_AREA)
    return rescaled

# Not enough input arguments, exit
if len(sys.argv) == 1:
    print "Not enough input arguments. Please input an image"
    sys.exit()

# Too many input arguments, exit
if len(sys.argv) > 2:
    print "Too many input arguments. Please input only the image"
    sys.exit()

image = cv2.imread(sys.argv[1])
#image = cv2.imread('../blurry-data/b1.JPG')

# Check image has been loaded
if image is None:
    print ('Error in opening image')
    sys.exit()

# Rescale the image to 20% of original size
resImage = image_rescale(image, 0.2)

# Convert to grayscale
grayImage = cv2.cvtColor(resImage, cv2.COLOR_BGR2GRAY)

# Compute the laplacian with default 3x3 kernel
lapImage = cv2.Laplacian(grayImage, cv2.CV_64F)

# Compute the variance of the laplacian
imVar = lapImage.var()
print(imVar)

# Decide if faulty or not - need to tune threshold
if imVar > 500:
    print(0)
else:
    print(1)

cv2.imshow("Image", grayImage)
cv2.waitKey(0)

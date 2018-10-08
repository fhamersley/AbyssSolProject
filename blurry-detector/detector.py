#!/usr/bin/python

import sys
import cv2
import numpy as np

def image_rescale(image, scale):
    """
    Rescale a given image using a given scale
    """
    (h, w) = image.shape[:2]    # Input image size

    outh = round(h * scale, 0)  # Rescale height and width
    outw = round(w * scale, 0)
    dim = int(outw), int(outh)       # Output dimension

    rescaled = cv2.resize(image, dim, cv2.INTER_AREA) # Rescale

    return rescaled


if len(sys.argv) == 1:
    print "Not enough input arguments. Please input an image"
    sys.exit()

if len(sys.argv) > 2:
    print "Too many input arguments. Please input only the image"
    sys.exit()

image = cv2.imread(sys.argv[1])
#image = cv2.imread('../blurry-data/b1.JPG')

resImage = image_rescale(image, 0.2)
cv2.imshow("Image", resImage)
cv2.waitKey(0)

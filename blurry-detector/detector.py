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

def image_segment(image, gridElementsX, gridElementsY):
    """
    Break given greyscale image into a grid of smaller segments of
    original image given by the grid elements passed in
    Return the image in single array of layers
    """    
    # Image size
    (H, W) = image.shape[:2]

    # Grid segment size
    gridH = H / float(gridElementsY)
    gridW = W / float(gridElementsX)

    # Exit early if the elements size does not fit into image
    if(not gridH.is_integer()):
        print('gridElementsY in image_segment() not compatible with image size')
        sys.exit()
    if (not gridW.is_integer()):
        print('gridElementsX in image_segment() not compatible with image size')
        sys.exit()

    # Track current position
    currGH = 0
    currGW = 0

    # Total number of grid elements
    gridElements = gridElementsX * gridElementsY

    # Prepare the image array
    cropImg = np.ndarray((gridH, gridW, gridElements), np.uint8)

    # Create the image array
    for i in range(0, gridElements):
        cropImg[:,:,i] = image[currGH:currGH+gridH, currGW:currGW+gridW]
        im = cropImg[:,:,i]
        # cv2.imshow("Image", im)
        # cv2.waitKey(0)
        currGH += gridH
        # If we reach the end of the col, reset to next row
        if (currGH == H):
            currGH = 0
            currGW += gridW

    return cropImg

def main(argv):
    """
    Detemine if an image is blurry using a threshold on the variance of the laplacian
    """
    # Not enough input arguments, exit
    if len(argv) == 1:
        print('Not enough input arguments. Please input an image')
        sys.exit()

    # Too many input arguments, exit
    if len(argv) > 2:
        print('Too many input arguments. Please input only the image')
        sys.exit()

    image = cv2.imread(argv[1])

    # Check image has been loaded
    if image is None:
        print('Error in opening image')
        sys.exit()

    # Rescale the image to 20% of original size
    #resImage = image_rescale(image, 1)

    # Convert to grayscale
    grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Blur with a median filter to remove static/noise
    blurImage = cv2.medianBlur(grayImage, 11)

    # Grid elements in X
    gridElementsX = 10

    # Grid elements in Y
    gridElementsY = 10

    # Segment the image down into a grid
    imageGrid = image_segment(blurImage, gridElementsX, gridElementsY)

    # Total number of grid elements
    gridElements = gridElementsX * gridElementsY

    # Init the sum
    totalVar = 0

    # Init the average total elements
    avgTotalElements = gridElements

    # Loop through images
    for i in range(0, gridElements):
        # Compute the variance of the laplacian of the image with default 3x3 kernel
        imVar = cv2.Laplacian(imageGrid[:,:,i], cv2.CV_64F).var()
        # If there is zero variance in this grid element discard it
        if (imVar == 0):
            avgTotalElements -= 1
            continue
        # Sum all the variance
        totalVar += imVar

    # Compute the average
    avgVar = totalVar / avgTotalElements
    #print(avgVar)

    # Decide if blurry or not.
    # Low variance of laplacian means low detail therefore blurry.
    # Threshold of 5 chosen by through analysis of training set.
    # This value classifies the two sets quite well.
    if avgVar > 5:
        print(0)
    else:
        print(1)

    # lapImage = cv2.Laplacian(blurImage, cv2.CV_64F)
    # cv2.imshow("Image", lapImage)
    # cv2.waitKey(0)

if __name__ == "__main__":
    main(sys.argv)

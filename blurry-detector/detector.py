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

def image_segment(image):
    """
    Break given image into a grid (4x3) of smaller segments of original image 
    Return the image in single array of 12 layers
    """    
    # Image size
    (H, W) = image.shape[:2]

    # Grid segment size
    gridH = H / 3
    gridW = W / 4

    # Track current position
    currGH = 0
    currGW = 0

    # Prepare the image array
    cropImg = np.ndarray((gridH, gridH, 12), np.uint8)

    # Create the image array
    for i in range(0,12):
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

    # Break the image down into a grid
    imageGrid = image_segment(grayImage)

    sum = 0
    for i in range(0,12):
        lapImage = cv2.Laplacian(imageGrid[:,:,i], cv2.CV_64F).var()
        imVar = lapImage
        sum = sum + imVar
        print(imVar)
    # avg = sum/12
    # print(avg)
    # Compute the laplacian with default 3x3 kernel
    lapImage = cv2.Laplacian(grayImage, cv2.CV_64F)

    # Compute the variance of the laplacian
    imVar = lapImage.var()
    print(imVar)

    # Decide if blurry or not.
    # Low variance of laplacian means low detail therefore blurry.
    # Threshold of 100 chosen by through analysis of training set.
    # This value classifies the two sets quite well.
    if imVar > 110:
        print(0)
    else:
        print(1)

    #cv2.imshow("Image", grayImage)
    #cv2.waitKey(0)    

if __name__ == "__main__":
    main(sys.argv)

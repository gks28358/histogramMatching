
import cv2
import numpy as np
import matplotlib.pyplot as plt


def RGB2Gray(s):
    # input image name
    img = cv2.imread(s)#s
    I = np.array(img)
    global row
    global col
    row, col = img.shape[:2]
    I_prime = np.zeros([row, col], dtype=np.uint8)

    # convert to greyscale

    for i in range(row):
        for j in range(col):
            I_prime[i, j] = (I[i, j, 2] + 2 * (I[i, j, 1]) + I[i, j, 0]) / 4

    return I_prime;


# Greyscale histogram
def greyscaleImageHist(I_prime):
   # row, col = I_prime.shape[:2]
    H = np.empty(256, dtype=np.uint8)
    for i in range(H.size):
        H[i] = 0

    for i in range(row):
        for j in range(col):
            H[I_prime[i, j]] = H[I_prime[i, j]] + 1

    return H;


# Normalized GreyScale Image Hist

def normalizedGreyScaleImageHist(I_prime):
    #row, col = I_prime.shape[:2]
    numPixels = row * col
    H_prime = np.empty(256, dtype=np.float32)
    H = greyscaleImageHist(I_prime)
    for i in range(H_prime.size):
        H_prime[i] = 0

    for i in range(H_prime.size):
        H_prime[i]=(H[i] / numPixels)

    return H_prime;


    # Cumulative Sum

def cumulativeSum(H_prime):
    cdf = np.empty(256, dtype=np.float32)
    cdf[0] = H_prime[0]

    for i in range(1, 255):
        cdf[i] = cdf[i - 1] + H_prime[i]

    return cdf;

    # Eualize Hist
def equalizeHist(I_prime):
    #row, col = I_prime.shape[:2]
    I_equalize = np.zeros([row, col], dtype=np.uint8)
    H_prime = normalizedGreyScaleImageHist(I_prime)
    cdf = cumulativeSum(H_prime)
    for i in range(row):
        for j in range(col):
            I_equalize[i, j] = round(255 * cdf[I_prime[i, j]])


    return I_equalize;

    # Histogram Matching
def histMatching(I_prime, H_prime):
    H = normalizedGreyScaleImageHist(I_prime)
    cdf = cumulativeSum(H)
    cdf_ref = cumulativeSum(H_prime)
    row, col = I_prime.shape[:2]
    lt = np.zeros(256, dtype=np.uint8)
    I_matched = np.zeros([row, col], dtype=np.uint8)
    for i in range(0, 256):
        levels_prime = 255
        while (levels_prime >= 0 and cdf_ref[levels_prime] > cdf[i]):
            lt[i] = levels_prime
            levels_prime = levels_prime - 1

    for i in range(row):
        for j in range(col):
            I_matched[i, j] = lt[I_prime[i, j]]

    return I_matched;


def main():
    I_prime=RGB2Gray("light-image.tif")
    I_ref=RGB2Gray("low-contrast.tif")
    H=greyscaleImageHist(I_prime)
    H_normalized=normalizedGreyScaleImageHist(I_ref)
    H_matching=histMatching(I_prime,H_normalized)
    cv2.imshow('Original Image',I_prime)
    cv2.waitKey(0)
    cv2.imshow('Matching Image',H_matching)
    cv2.waitKey(0)

if __name__ == "__main__": main()
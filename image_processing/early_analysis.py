import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

def plotintensitydistribution(image, title="Pixel Intensity Distribution over Image"):
    graphfont = {'fontname':'Consolas'}
    plt.figure(figsize=(6,2), dpi =100) #dpi =
    n, bins, patches = plt.hist(image.ravel(), bins=np.linspace(0,1.0,256))
    plt.title(title, **graphfont)
    plt.xlabel("Pixel Value (grayscale)", **graphfont)
    plt.ylabel("Number of Pixels", **graphfont)
    plt.xticks(**graphfont)
    plt.yticks(**graphfont)
    plt.xlim(0,1.0)
    for b, p in zip(bins, patches):
        plt.setp(p, 'facecolor', plt.cm.get_cmap('Greys_r')(b))
    ax = plt.gca()
    ax.set_facecolor("#91B2C7")
    plt.show()
    # print(bins)

def nearestneighborimage(image):
    dims = np.shape(image)
    height = dims[0]
    width = dims[1]
    neighbor_difference_image = np.copy(image)
    for row in range(height):
        for col in range(width):
            current_pixel_value = image[row, col]
            sum_difference = 0.0
            if row != 0 and col != 0:
                sum_difference += np.abs(current_pixel_value - image[row-1][col-1])
            if row != 0:
                sum_difference += np.abs(current_pixel_value - image[row-1][col])
            if row != 0 and col != (width-1):
                sum_difference += np.abs(current_pixel_value - image[row-1][col+1])
            if col != 0:
                sum_difference += np.abs(current_pixel_value - image[row][col-1])
            if col != (width-1):
                sum_difference += np.abs(current_pixel_value - image[row][col+1])
            if row != (height-1) and col != 0:
                sum_difference += np.abs(current_pixel_value - image[row+1][col-1])
            if row != (height-1):
                sum_difference += np.abs(current_pixel_value - image[row+1][col])
            if row != (height-1) and col != (width-1):
                sum_difference += np.abs(current_pixel_value - image[row+1][col+1])
            neighbor_difference_image[row, col] = sum_difference
    return neighbor_difference_image 

def normalize(image, torange=(0.0,1.0)):
    # takes range of monotone image and brings it back to [0.0, 1.0]
    normalized_image = np.copy(image)
    min_intensity = np.min(image)
    max_intensity = np.max(image)
    dims = np.shape(image)
    height = dims[0]
    width = dims[1]
    for row in range(height):
        for col in range(width):
            normalized_image[row, col] = (image[row, col]-min_intensity)/(max_intensity-min_intensity)
            normalized_image[row, col] = (normalized_image[row, col]+torange[0]) * (torange[1]-torange[0])
    return normalized_image
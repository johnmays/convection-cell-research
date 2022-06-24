import cv2 as cv
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import os
# from mpl_toolkits import mplot3d

def getbackgroundareas(image):
    # takes in a monochrome, binary image matrix
    # generates a list of black areas in an image:
    areas = []
    area_locations = []
    visited = np.zeros(np.shape(image), dtype=bool)
    for row in range(np.shape(image)[0]):
        for col in range(np.shape(image)[1]):
            if visited[row][col] == False:
                area_coords = expandarea((row, col), image, visited)
                if area_coords != []:
                    area_locations.append(area_coords)
                    areas.append(len(area_coords))
    return areas, area_locations

def expandarea(coord, image, visited):
    if coord[0] < 0 or coord[0] >= np.shape(image)[0]:
        return []
    if coord[1] < 0 or coord[1] >= np.shape(image)[1]:
        return []
    if visited[coord[0]][coord[1]] == False:
        visited[coord[0]][coord[1]] = True
        current_pixel = image[coord[0]][coord[1]]
        if current_pixel == 0:
            return [coord] \
                + expandarea((coord[0]+1, coord[1]), image, visited) \
                    + expandarea((coord[0]-1, coord[1]), image, visited) \
                        + expandarea((coord[0], coord[1]+1), image, visited) \
                            + expandarea((coord[0], coord[1]-1), image, visited)
        else:
            return []
    else:
        return []

def colorareas(image, thresh):
    # takes in a monochrome, thresholded image
    image_3channel = np.stack((image,image,image), axis=-1)
    areas, area_locations = getbackgroundareas(image)
    for i in range(len(areas)):
        area = areas[i]
        if area < thresh:
            for coord in area_locations[i]:
                image_3channel[coord[0]][coord[1]] = [255,0,0]
    return image_3channel

def purgesmallareas(image, thresh):
    # takes in a monochrome, thresholded image
    final_image = np.copy(image)
    areas, area_locations = getbackgroundareas(image)
    for i in range(len(areas)):
        area = areas[i]
        if area < thresh:
            for coord in area_locations[i]:
                final_image[coord[0]][coord[1]] = 255
    return final_image

def invert(image):
    newimage = np.copy(image)
    for row in range(np.shape(image)[0]):
        for col in range(np.shape(image)[1]):
            newimage[row,col] = 255 - newimage[row,col]
    return newimage

def borderirregularity(P_set):
    # P_set is set of pixels that form an area
    A = len(P_set) # area
    B_set = [] # B_set is set of pixels that could be considered as belonging to the border of the area
    N_set = []
    for pixel in P_set:
        if (pixel[0], pixel[1]+1) in P_set and (pixel[0], pixel[1]-1) in P_set and \
            (pixel[0]+1, pixel[1]) in P_set and (pixel[0]-1, pixel[1]) in P_set:
            pass # then this pixel is within the body of the area
        else:
            B_set.append(pixel)
            neighbors = 0
            if (pixel[0]+1, pixel[1]+1) in P_set:
                neighbors += 1
            if (pixel[0]+1, pixel[1]) in P_set:
                neighbors += 1
            if (pixel[0]+1, pixel[1]-1) in P_set:
                neighbors += 1
            if (pixel[0], pixel[1]+1) in P_set:
                neighbors += 1
            if (pixel[0], pixel[1]-1) in P_set:
                neighbors += 1
            if (pixel[0]-1, pixel[1]+1) in P_set:
                neighbors += 1
            if (pixel[0]-1, pixel[1]) in P_set:
                neighbors += 1
            if (pixel[0]-1, pixel[1]-1) in P_set:
                neighbors += 1
            N_set.append(neighbors) # count how many neighbors this pixel has in the area
    N = np.sum(N_set)
    B = len(B_set)
    if B == 0:
        return 0
    else:
        return N/B # average number of neighbors per pixel considered to be on the border

def irregularityplot(image):
    final_image = np.copy(image)
    areas, area_locations = getbackgroundareas(image)
    irregularity_measures = []
    # finding irregularity measures for each area
    for i in range(len(areas)):
        irregularity_measures.append(borderirregularity(area_locations[i]))
    
    # normalizing irregularity measures
    irregularity_measures = irregularity_measures - np.min(irregularity_measures)
    irregularity_measures = irregularity_measures/np.max(irregularity_measures) 

    # plotting measures
    for i in range(len(areas)):
        plt.text(area_locations[i][0][1], area_locations[i][0][0], str(round(irregularity_measures[i],2)), c="#ff0000")
    plt.imshow(image, cmap='Greys_r', vmin=0, vmax=255);
import numpy as np
from skimage import exposure, morphology

def get_unwalked_coords(image):
    coords = np.where(image == 1)
    zipped_coords = np.dstack(coords)
    return zipped_coords.reshape(zipped_coords.shape[1], zipped_coords.shape[2])

def get_neighbours(currentPixel, centrePoint):
    neighbours = np.array([[currentPixel[0]+1, currentPixel[1]+1],
            [currentPixel[0]+1, currentPixel[1]],
            [currentPixel[0]+1, currentPixel[1]-1],
            [currentPixel[0], currentPixel[1]+1],
            [currentPixel[0], currentPixel[1]-1],
            [currentPixel[0]-1, currentPixel[1]+1],
            [currentPixel[0]-1, currentPixel[1]],
            [currentPixel[0]-1, currentPixel[1]-1],
           ])

    neighbours_dist = map(lambda x: np.linalg.norm(x-centrePoint), neighbours)
    neighbours = neighbours[np.argsort(np.array(list(neighbours_dist)))]
    return neighbours

def next_neighbour(currentPixel, thinned_image, centrePoint):
    neighbours = get_neighbours(currentPixel, centrePoint)
    for n in neighbours:
        n = np.array(n).astype(int)

        if n[0] < 0 or n[1] < 0:
            return np.array([-1,-1])

        try:
            if thinned_image[n[0], n[1]] == 1:
                return n
        except:
            next
    return np.array([-1,-1])

def walk_neighbourhood(image):
    thinned_image = morphology.thin(np.where(image<0.1, 0, 1))
    thinned_image = np.where(thinned_image<0.1, 0, 1)
    centre = get_centre(thinned_image)

    try:
        totalPixels = exposure.histogram(thinned_image, nbins=2)[0][1]
    except IndexError:
        return []

    currentPixel = np.array([-1, -1])
    walkingOrder = []
    index=-1
    while totalPixels > 0:

        if np.array_equal(currentPixel, np.array([-1, -1])):
            currentPixel = get_unwalked_coords(thinned_image)[0]
            walkingOrder.append([])
            index += 1
        else:
            thinned_image[currentPixel[0], currentPixel[1]] = 0
            walkingOrder[index].append(currentPixel)
            currentPixel = next_neighbour(currentPixel, thinned_image, centre)
            totalPixels -= 1

    return walkingOrder

#idea from https://www.geeksforgeeks.org/program-check-three-points-collinear/
def check_colinear(p1, p2, p3):
    return (p1[1] * (p2[0]-p3[0]) + p2[1] * (p3[0]-p1[0]) + p3[1] * (p1[0]-p2[0])) == 0

def get_centre(image):
    return np.mean(np.where(image==1), axis=1)

#Checking colinearity should probably be used here (maybe a recursive solution??)
def find_major_anchors(points_list):
    for feature in points_list:
        changed = True
        #if the point set wasn't reduced then go to the next point set
        while changed:
            changed = False
            i = 0
            while True:

                if len(feature) < 3:
                    changed = False
                    break

                if len(feature)-2 <= i:
                    break

                if check_colinear(feature[i],feature[i+1],feature[i+2]):
                    feature.pop(i+1)
                    changed = True

                i += 1
    return points_list

import numpy as np
from skimage import morphology
try:
    from .SketchFeatures import findMajorAnchors
except:
    from SketchFeatures import findMajorAnchors

def getShadedArea(original_image, edge_detected, ao_im, threshold=24):
    original_shade = morphology.erosion(np.copy(original_image)[:,:,0] - edge_detected)
    shade = np.where(original_shade < threshold, 0, 256)
    ao_image = np.where(ao_im[:,:,0]>0)
    shaded_area = ao_im[:,:,0]-shade
    shaded_area = np.where(shaded_area > 0, 256, 0)
    return shaded_area

def getAllShadeBands(original_image, ao_image, edge_detected, bands=3, interval=30):
    previous_shade = np.zeros_like(edge_detected)
    shade_bands = []
    for band in range(1, bands+1):
        shade = getShadedArea(original_image, edge_detected, ao_image, band*interval) - previous_shade
        shade_bands.append(shade)
        previous_shade = previous_shade + shade

    return shade_bands

def applyHorizontalEffect(shaded_area, edge_detected, k=2):
    mask = np.zeros_like(edge_detected)
    mask[::k] = 256
    shaded_area = shaded_area+mask-256
    shaded_area = np.where(shaded_area > 0, 256, 0)
    return shaded_area

def applyDiagonalEffect(shaded_area, edge_detected, k=2):
    mask = np.zeros_like(edge_detected)
    changed_row = mask[0]
    changed_row[::k] = 256
    for i in range(0, len(mask)):
        mask[i] = changed_row
        changed_row = np.roll(changed_row, -1)
    shaded_area = shaded_area+mask-256
    shaded_area = np.where(shaded_area > 0, 256, 0)
    return shaded_area

def findShadeAnchors(pointsList):
    newPointsList = findMajorAnchors(pointsList[:])
    for feature in pointsList:
        newPointsList.append([np.max(feature, axis=0), np.min(feature, axis=0)])

    return newPointsList

def drawShadeGreyBackground(canvas, original_monkey, ao_monkey, edge_monkey, bands=3, interval=30):
    currentShade = np.zeros_like(edge_monkey)
    for i in range(1, bands+1):
        shade = testShading(original_monkey, edge_monkey, 2**i, i*interval) - currentShade
        currentShade = currentShade + shade
        for feature in findShadeAnchors(walkNeighbourhood(np.flip(np.rot90(shade), axis=0))):
            canvas = guided_sketch(canvas, np.array(feature), 0.5)

    return canvas

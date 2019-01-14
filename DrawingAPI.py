import numpy as np
from skimage import filters
from .SketchShading import *
from .SketchFeatures import *
from .SketchCanvas import *

def drawShadeHorizontal(canvas, original_image, ao_image, edge_detected, bands=3, interval=30):
    current_band = 1
    for shade in getAllShadeBands(original_image, ao_image, edge_detected, bands, interval):
        shade = applyHorizontalEffect(shade, edge_detected, 2**current_band)
        current_band += 1
        for feature in findShadeAnchors(walkNeighbourhood(np.flip(np.rot90(shade), axis=0))):
            canvas = guided_sketch(canvas, np.array(feature), 0.5)

    return canvas

def drawShadeVertical(canvas, original_image, ao_image, edge_detected, bands=3, interval=30):
    current_band = 1
    for shade in getAllShadeBands(original_image, ao_image, edge_detected, bands, interval):
        shade = applyVerticalEffect(shade, edge_detected, 2**current_band)
        current_band += 1
        for feature in walkNeighbourhood(np.flip(np.rot90(shade), axis=0)):
            canvas = guided_sketch(canvas, np.array(feature), 0.5)

    return canvas

def drawShadeDiagonal(canvas, original_image, ao_image, edge_detected, bands=3, interval=30):
    current_band = 2
    for shade in getAllShadeBands(original_image, ao_image, edge_detected, bands, interval):
        shade = applyDiagonalEffect(shade, edge_detected, 2**current_band)
        current_band += 1
        for feature in walkNeighbourhood(np.flip(np.rot90(shade), axis=0)):
            #needed to get rid of noise(?)
            if len(feature) > 2:
                canvas = guided_sketch(canvas, np.array(feature), 0.5)

    return canvas

def drawFeatures(name, edge_detected, ao_image):
    pointToDraw = walkNeighbourhood(np.flip(np.rot90(edge_detected), axis=0))
    canvas = initCanvas(name)
    pointToDraw = findMajorAnchors(pointToDraw)
    for feature in pointToDraw:
        canvas = guided_sketch(canvas, np.array(feature))

    outline =  findMajorAnchors(walkNeighbourhood(np.flip(np.rot90(filters.sobel(ao_image[:,:,0])), axis=0)))
    canvas = guided_sketch(canvas, np.array(outline[0]), 1.5)

    return canvas

import numpy as np
from skimage import filters
from .SketchShading import *
from .SketchFeatures import *
from .SketchCanvas import *

def drawShadeHorizontal(canvas, views, bands=3, interval=30):
    current_band = 1
    for shade in getAllShadeBands(views, bands, interval):
        shade = applyHorizontalEffect(shade, views['edge'], 2**current_band)
        current_band += 1
        for feature in walkNeighbourhood(np.flip(np.rot90(shade), axis=0)):
            canvas = guided_sketch(canvas, np.array(feature), 0.5)

    return canvas

def drawShadeVertical(canvas, views, bands=3, interval=30):
    current_band = 1
    for shade in getAllShadeBands(views, bands, interval):
        shade = applyVerticalEffect(shade, views['edge'], 2**current_band)
        current_band += 1
        for feature in walkNeighbourhood(np.flip(np.rot90(shade), axis=0)):
            canvas = guided_sketch(canvas, np.array(feature), 0.5)

    return canvas

def drawShadeDiagonal(canvas, views, bands=3, interval=30):
    current_band = 2
    for shade in getAllShadeBands(views, interval):
        shade = applyDiagonalEffect(shade, views['edge'], 2**current_band)
        current_band += 1
        for feature in walkNeighbourhood(np.flip(np.rot90(shade), axis=0)):
            #needed to get rid of noise
            if len(feature) > 2:
                canvas = guided_sketch(canvas, np.array(feature), 0.5)

    return canvas

def drawShadeDotted(canvas, views, bands=3, interval=30):
    current_band = 1
    for shade in getAllShadeBands(views, bands, interval):
        shade = applyDottedEffect(shade, views['edge'], current_band-1)
        current_band += 1
        for feature in walkNeighbourhood(np.flip(np.rot90(shade), axis=0)):
            canvas = dotted_shade_sketch(canvas, np.array(feature), 0.35)

    return canvas

def drawFeatures(name, views):
    pointToDraw = walkNeighbourhood(np.flip(np.rot90(views['edge']), axis=0))
    canvas = initCanvas(name)
    pointToDraw = findMajorAnchors(pointToDraw)
    for feature in pointToDraw:
        canvas = guided_sketch(canvas, np.array(feature))

    outline =  findMajorAnchors(walkNeighbourhood(np.flip(np.rot90(filters.sobel(views['ao'][:,:,0])), axis=0)))
    canvas = guided_sketch(canvas, np.array(outline[0]), 1.5)

    return canvas

def drawShadeStream(canvas, views, uv_component, bands=3, interval=30):
    if np.all(uv_component==0):
        return canvas

    current_band = 1
    shades = getAllShadeBands(views, bands, interval)
    contours = findMajorAnchors(applySmoothing(applyStreamEffect(uv_component, 1)))

    for shade in shades:
        segmented_contours = shadeSegmentedContours(shade, contours)[::current_band]
        for feature in segmented_contours:
            feature = np.array(feature)
            if np.linalg.norm(feature[0]-feature[-1]) > 3:
                guided_sketch(canvas, np.array(feature), 0.3)
        current_band += 1

    return canvas

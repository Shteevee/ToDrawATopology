import numpy as np
from skimage import morphology, util
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
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

def applyVerticalEffect(shaded_area, edge_detected, k=2):
    mask = np.zeros_like(edge_detected)
    mask[:,::k] = 256
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

def applyDottedEffect(shaded_area, edge_detected, k=0):
    mask = np.zeros_like(edge_detected)
    mask = util.random_noise(mask, mode='gaussian', mean=0.01)
    mask = np.where(mask > 0.07*k, 256, 0)
    shaded_area = shaded_area+mask-256
    shaded_area = np.where(shaded_area > 0, 256, 0)
    return shaded_area

def findShadeAnchors(pointsList):
    newPointsList = []
    for feature in pointsList:
        newPointsList.append([feature[0], feature[-1]])
        newPointsList.append([feature[-1], feature[0]])
    return newPointsList

def applyStreamEffect(component, k=2):
    filtered_uv = np.copy(component.astype(np.float64))
    component_grad_X, component_grad_Y = np.gradient(makeContinuous(filtered_uv))

    w, h = component_grad_X.shape
    y, x = np.mgrid[0:w, 0:h]

    fig, ax = plt.subplots()
    ax.imshow(component, cmap=plt.cm.Greys)
    stream = plt.streamplot(x, y, component_grad_X, component_grad_Y, density=25, linewidth=0.5, arrowsize=0.00000000001)
    lines = stitch_paths(clean_paths(stream.lines.get_paths()))

    return lines

def makeContinuous(component):
    component = component/np.max(component)
    component = np.sin(component*2*np.pi)

    return component

def clean_paths(paths):
    cleaned_paths = list()
    for path in paths:
        if len(cleaned_paths) == 0 or not np.array_equal(cleaned_paths[-1].vertices, path.vertices):
            if not np.allclose(path.vertices[0], path.vertices[1]):
                cleaned_paths.append(path)

    return cleaned_paths

def stitch_paths(paths):
    stitched_paths = list()
    for path in paths:
        if len(stitched_paths) == 0:
            stitched_paths.append(path.vertices)

        if np.allclose(stitched_paths[-1][-1], path.vertices[0]):
            joined = np.concatenate((stitched_paths[-1], np.array([path.vertices[1]])), axis=0)
            stitched_paths[-1] = joined
        else:
            stitched_paths.append(path.vertices)

    return stitched_paths

def shadeSegmentedContours(shade, contours):
    new_contours = list()
    prev_in_shade = False
    in_shade = False
    for contour in contours:

        for point in contour:
            if shade[int(point[1]), int(point[0])] == 256.0:
                in_shade = True
            else:
                in_shade = False

            if not prev_in_shade and in_shade:
                new_contour = list()
                new_contour.append(point)
            elif prev_in_shade and in_shade:
                new_contour.append(point)
            elif prev_in_shade and not in_shade:
                new_contours.append(new_contour)

            prev_in_shade = in_shade

        if in_shade:
            new_contours.append(new_contour)
            in_shade = False
            prev_in_shade = False

    return new_contours

def applySmoothing(lines):
    return list(map(lambda x: x.tolist()[::3], lines))

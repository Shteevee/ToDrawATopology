import numpy as np
from skimage import filters
from .sketch_features import *
from .sketch_shading import *
from .sketch_canvas import *

def draw_shade_horizontal(canvas, views, bands=3, interval=30):
    current_band = 1
    for shade in get_all_shade_bands(views, bands, interval):
        shade = apply_horizontal_effect(shade, views['edge'], 2**current_band)
        current_band += 1
        for feature in walk_neighbourhood(np.flip(np.rot90(shade), axis=0)):
            canvas = guided_sketch(canvas, np.array(feature), 0.5)

    return canvas

def draw_shade_vertical(canvas, views, bands=3, interval=30):
    current_band = 1
    for shade in get_all_shade_bands(views, bands, interval):
        shade = apply_vertical_effect(shade, views['edge'], 2**current_band)
        current_band += 1
        for feature in walk_neighbourhood(np.flip(np.rot90(shade), axis=0)):
            canvas = guided_sketch(canvas, np.array(feature), 0.5)

    return canvas

def draw_shade_diagonal(canvas, views, bands=3, interval=30):
    current_band = 2
    for shade in get_all_shade_bands(views, interval):
        shade = apply_diagonal_effect(shade, views['edge'], 2**current_band)
        current_band += 1
        for feature in walk_neighbourhood(np.flip(np.rot90(shade), axis=0)):
            #needed to get rid of noise
            if len(feature) > 2:
                canvas = guided_sketch(canvas, np.array(feature), 0.5)

    return canvas

def draw_shade_dotted(canvas, views, bands=3, interval=30):
    current_band = 1
    for shade in get_all_shade_bands(views, bands, interval):
        shade = apply_dotted_effect(shade, views['edge'], current_band-1)
        current_band += 1
        for feature in walk_neighbourhood(np.flip(np.rot90(shade), axis=0)):
            canvas = dotted_shade_sketch(canvas, np.array(feature), 0.35)

    return canvas

def draw_features(name, views):
    pointToDraw = walk_neighbourhood(np.flip(np.rot90(views['edge']), axis=0))
    canvas = init_canvas(name)
    pointToDraw = find_major_anchors(pointToDraw)
    for feature in pointToDraw:
        canvas = guided_sketch(canvas, np.array(feature))

    outline =  find_major_anchors(walk_neighbourhood(np.flip(np.rot90(filters.sobel(views['ao'][:,:,0])), axis=0)))
    canvas = guided_sketch(canvas, np.array(outline[0]), 1.5)

    return canvas

def draw_shade_stream(canvas, views, uv_component, bands=3, interval=30):
    if np.all(uv_component==0):
        return canvas

    current_band = 1
    shades = get_all_shade_bands(views, bands, interval)
    contours = find_major_anchors(apply_smoothing(apply_stream_effect(uv_component, 1)))

    for shade in shades:
        segmented_contours = shade_segmented_contours(shade, contours)[::current_band]
        for feature in segmented_contours:
            feature = np.array(feature)
            if np.linalg.norm(feature[0]-feature[-1]) > 3:
                guided_sketch(canvas, np.array(feature), 0.3)
        current_band += 1

    return canvas

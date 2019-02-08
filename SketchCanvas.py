import numpy as np
import svgwrite

def guided_sketch(dwg, points, thickness=1):
    velocity_base = 0.1
    acceleration = 0.4
    turn_rate = 2

    path = dwg.path(('M', points[0,0], points[0,1]), fill='none', stroke="black", stroke_linecap='round', stroke_width=thickness)
    for i in range(1, len(points)):
        currentPos = np.copy(points[i-1])
        difference_vector = points[i]-points[i-1]

        if i < len(points)-1:
            next_difference_vector = points[i+1]-points[i]
        else:
            next_difference_vector = difference_vector

        angle = dotProductAngle(difference_vector, next_difference_vector)
        for j in range(1, turn_rate):
            nextPos = [(currentPos[0] + (difference_vector[0]*(j/turn_rate)) * np.cos(angle)), currentPos[1] + (difference_vector[1]*(j/turn_rate) * np.sin(angle))]
            path.push(('L', nextPos[0], nextPos[1]))

    dwg.add(path)

    return dwg

def dotted_shade_sketch(dwg, points, radius=0.5):
    for point in points:
        dwg.add(dwg.circle(center=(float(point[0])+np.random.uniform(-0.5,0.5),float(point[1])+np.random.uniform(-0.5,0.5)), r=radius))

    return dwg

def lessThan(startPos, currentPos, endPos):
    return np.linalg.norm(currentPos-startPos) < np.linalg.norm(endPos-startPos)

def dotProductAngle(v1, v2):
    #re-arranged dot product for theta
    theta = np.arccos( np.dot(v1,v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)) )
    if np.isnan(theta):
        return 0
    else:
        return np.arccos( np.dot(v1,v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)) )

def rotMatrix(theta):
    return [[np.cos(theta), -np.sin(theta)],
            [np.sin(theta), np.cos(theta)]]

def initCanvas(name):
    dwg = svgwrite.Drawing(name)

    dwg.add(dwg.rect(insert=(0, 0), size=('100%', '100%'), rx=None, ry=None, fill='white'))

    gradline = dwg.linearGradient((0, 0), (0, 0), id="grad")
    gradline.add_stop_color(0.1, 'white')
    gradline.add_stop_color(1, 'black')

    dwg.defs.add(gradline)

    return dwg

import numpy
import CalculatePointLocations as cp
import getlocation as gl


def calc_slope(x1, y1, x2, y2):
    if x2 == x1:
        return
    return (y2 - y1) / (x2 - x1)


def dir(front, back, left, right):
    alpha = 40
    if front and left and back:
        return 180.0
    if left and back and right:
        return 90.0
    if back and right and front:
        return 0.0
    if right and front and left:
        return -90.0
    slope = 0
    theta = 0
    if front and left:
        lx = left[0] - front[0]
        ly = left[1] - front[1]
        fx = 0
        fy = 0
        slope = calc_slope(fx, fy, lx, ly)
        if slope:
            theta = numpy.degrees(numpy.arctan(slope * -1))
        elif ly > fy:
            theta = 90.0
        else:
            theta = -90.0

        if lx > fx:
            return 180 + theta + alpha
        else:
            return theta + alpha

    if front and right:
        rx = right[0] - front[0]
        ry = right[1] - front[1]
        fx = 0
        fy = 0
        slope = calc_slope(fx, fy, rx, ry)
        if slope:
            theta = numpy.degrees(numpy.arctan(slope * -1))
        elif ry > fy:
            theta = 90.0
        else:
            theta = -90.0

        if rx > fx:
            return 180 + theta + alpha
        else:
            return theta - alpha

    if back and left:
        lx = left[0] - back[0]
        ly = left[1] - back[1]
        bx = 0
        by = 0
        slope = calc_slope(bx, by, lx, ly)
        if slope:
            theta = numpy.degrees(numpy.arctan(slope * -1))
        elif ly > by:
            theta = 90.0
        else:
           theta = -90.0

        if lx > bx:
            return theta - alpha
        else:
            return 180.0 + theta - alpha

    if back and right:
        rx = right[0] - back[0]
        ry = right[1] - back[1]
        bx = 0
        by = 0
        slope = calc_slope(bx, by, rx, ry)
        if slope:
            theta = numpy.degrees(numpy.arctan(slope * -1))
        elif ry > by:
            theta = 90.0
        else:
            theta = -90.0

        print "slope ", slope
        print "theta ", theta
        if rx > bx:
            return theta + alpha
        else:
            return 180.0 + theta + alpha

    if left:
        return 180.0
    if back:
        return 90.0
    if right:
        return 0.0
    if front:
        return 270
    return None




def get_current_info():
    points, height, width = gl.getdotmatrix()
    px = None
    py = None
    if points[0]:
        points[0] = cp.get_real_coordinates(points[0][0], points[0][1], height, width)
        px = points[0][0]
        py = points[0][1]
    if points[1]:
        points[1] = cp.get_real_coordinates(points[1][0], points[1][1], height, width)
        if not px:
            px = points[1][0]
            py = points[1][1]
    if points[2]:
        points[2] = cp.get_real_coordinates(points[2][0], points[2][1], height, width)
        if not px:
            px = points[2][0]
            py = points[2][1]
    if points[3]:
        points[3] = cp.get_real_coordinates(points[3][0], points[3][1], height, width)
        if not px:
            px = points[3][0]
            py = points[3][1]


    direction = dir(points[0], points[1], points[2], points[3])
    return px, py, direction








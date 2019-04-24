import numpy
import CalculatePointLocations as cp


def calc_slope(x1, y1, x2, y2):
    if x2 == x1:
        return
    return (y2 - y1) / (x2 - x1)


def main(front, back, left, right):
    alpha = 45
    if front and left and back:
        return 180.0
    if left and back and right:
        return 90.0
    if back and right and front:
        return 0.0
    if right and front and left:
        return 270.0
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
            return theta + alpha
        else:
            return 180 + theta + alpha

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
        return 270.0


bx, by = cp.get_real_coordinates(636.0, 675.0)
print bx, by
rx, ry = cp.get_real_coordinates(746.0, 645.0)
print rx, ry
print(main(0, [bx, by], 0, [rx, ry]))


from scipy import stats

# gives y coordinate given x in y=mx+b equation
def solve_for_y(x, slope, yintercept):
    if slope is not None and yintercept is not None:
        return slope * x + yintercept
    else:
        raise Exception('Cannot solve on a vertical line')


# gives x coordinate given y in y=mx+b equation
def solve_for_x(y, slope, yintercept):
    if slope is not 0 and slope:
        return (y - yintercept) / slope
    else:
        raise Exception('Cannot solve on a horizontal line')


def get_real_coordinates(Px, Py):
    #fname = raw_input("calibration.txt")
    f = open("calibration.txt")
    fl = []
    for line in f:
        fl.append(float(line.strip()))
    ULx = fl[0]  # upper left x
    ULy = fl[1]  # upper left y
    URx = fl[2]  # upper right x
    URy = fl[3]  # upper right y
    OFLx = fl[4]  # one foot from top left x
    OFLy = fl[5]  # one foot from top left y
    WELx = fl[6]  # wall end left x
    WELy = fl[7]  # wall end left y
    WERx = fl[8]  # wall end right x
    WERy = fl[9]  # wall end right y
    OFMx = fl[10]  # one foot from bottom middle x
    OFMy = fl[11]  # one foot from bottom middle y
    UMx = (ULx + URx)/2.0  # upper middle x
    UMy = (ULy + URy)/2.0  # upper middle y
    BMx = 960.0  # bottom middle x
    BMy = 1080.0  # bottom middle y
    FFH = OFLy - ULy  # height of first foot in pixels
    LFH = BMy - OFMy  # height of the last foot in pixels
    TotH = BMy - UMy  # total height in pixels
    CPPx = (LFH - FFH) / TotH  # change in height per pixel
    MaxNumPx = FFH + ((Py - UMy) * CPPx) # Maximum number of pixels per foot at point
    APxPF = (FFH + MaxNumPx) / 2.0  # avg number of px per feet for point
    Ay = (Py - UMy) / APxPF  # actual y in feet

    # get line eqns for points. NOTE! to make math work and not infinite, x and y coords
    # are swapped for all math involving these lines
    LSlope, LIntercept, _, _, _ = stats.linregress([ULy, WELy], [ULx, WELx])
    RSlope, RIntercept, _, _, _ = stats.linregress([URy, WERy], [URx, WERx])

    if Px < 960:
        wallx = solve_for_y(Py, LSlope, LIntercept)  # wall x at given y point
    elif Px > 960:
        wallx = solve_for_y(Py, RSlope, RIntercept)  # wall x at given y point
    else:
        wallx = 960  # x is along middle line so "wall" is 960

    shiftedx = Px - 960  # make center of photo 0
    shiftedwallx = wallx - 960

    # get slope of line using ratio of x to wall x and slope to wall slope
    # shiftedx/shiftedwallx = point slope/LSlope or RSlope
    if shiftedx < 0:
        slope = shiftedx * LSlope / shiftedwallx
    elif shiftedx > 0:
        slope = shiftedx * RSlope /shiftedwallx
    else:
        slope = 0

    pointIntercept = Px - slope * Py  # get equation for line to point
    x_on_top_line = solve_for_y(ULy, slope, pointIntercept)

    # do what we just did for one foot from corner point to get
    # how many pixels one foot is on the top line
    if OFLx < 960:
        OFLwallx = solve_for_y(OFLy, LSlope, LIntercept)  # wall x at given y point
    elif OFLx > 960:
        OFLwallx = solve_for_y(OFLy, RSlope, RIntercept)  # wall x at given y point
    else:
        OFLwallx = 960  # x is along middle line so "wall" is 960

    OFLshiftedx = OFLx - 960  # make center of photo 0
    OFLshiftedwallx = OFLwallx - 960

    # get slope of line using ratio of x to wall x and slope to wall slope
    # shiftedx/shiftedwallx = point slope/LSlope or RSlope
    if OFLshiftedx < 0:
        OFLslope = OFLshiftedx * LSlope / OFLshiftedwallx
    elif shiftedx > 0:
        OFLslope = OFLshiftedx * RSlope / OFLshiftedwallx
    else:
        OFLslope = 0

    OFLIntercept = OFLx - OFLslope * OFLy  # get equation for line to point
    OFL_on_top_line = solve_for_y(ULy, OFLslope, OFLIntercept)


    OFPxTL = OFL_on_top_line - ULx # one foot in pixels on top line

    Ax = (x_on_top_line - ULx) / OFPxTL # actual x in feet

    Ax = Ax * .3048
    Ay = Ay * .3048

    return Ax, Ay













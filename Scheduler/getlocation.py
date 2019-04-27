import cv2
import imutils



def get_color_location(lower, upper, frame):

    # resize the frame, blur it, and convert it to the HSV
    # color space

    #frame = imutils.resize(frame, width=600)
    #blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    blurred = frame

    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # construct a mask for the color, then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv2.inRange(hsv, lower, upper)
    mask = cv2.erode(mask, None, iterations=1)
    mask = cv2.dilate(mask, None, iterations=1)

    #cv2.imshow("mask", mask)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None

    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        # # only proceed if the radius meets a minimum size
        # if radius > 0:
        #     # draw the circle and centroid on the frame,
        #     # then update the list of tracked points
        #     cv2.circle(frame, (int(x), int(y)), int(radius),
        #                (0, 255, 255), 2)
        #     cv2.circle(frame, center, 5, (0, 0, 255), -1)


    # update the points queue
    return center


def getdotmatrix():
    cap = cv2.VideoCapture(1)
    _, frame = cap.read()
    #frame = cv2.imread("miro.jpg")
    # cv2.imshow('image', frame)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    height, width = frame.shape[:2]
    #print(height, width)

    yellowlower = (22, 148, 63)
    yellowupper = (105, 255, 255)

    purplelower = (61, 105, 81)
    purpleupper = (153, 255, 255)

    orangelower = (0, 200, 128)
    orangeupper = (24, 255, 255)

    greenlower = (30, 72, 84)
    greenupper = (96, 255, 255)

    points = []

    #print("green")
    points.append(get_color_location(greenlower, greenupper, frame))
    #print("purple")
    points.append(get_color_location(purplelower, purpleupper, frame))
    #print("yellow")
    points.append(get_color_location(yellowlower, yellowupper, frame))
    #print("orange")
    points.append(get_color_location(orangelower, orangeupper, frame))


    return points, height, width



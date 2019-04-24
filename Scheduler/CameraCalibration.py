#-------------------------------------------------------------------------------------------
# This program calibrates the webcam camera to be used with the programs that
# calculate the position and direction of the robot. It works for a 1080x1920
# resolution webcam in the camera 1 slot on a computer, and REQUIRES that the
# camera be positioned with the top of the frame parallel to the line where
# the wall meets the floor and will work better the higher the camera is. It
# was tested using a camera ~3 feet off the ground.

import cv2

def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:

        if len(msglist) > 1:
            del msglist[0]
            print x, y
            pts.append(str(x))
            pts.append(str(y))
        print msglist[0]


pts = []
msglist = [
    "Click on the top left corner of the floor in the image ",
    "Click on the top right corner of the floor ",
    "Click on the point one foot away from the top and left of the wall ",
    "Click on the point where the left side of the wall ends ",
    "Click on the point where the right side of the wall ends ",
    "Click on the point one foot from the bottom of the image in the center ",
    "Press any key to close the image "
]
camera = cv2.VideoCapture(1)
# r, image = camera.read()
image = cv2.imread("room.jpg")
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.resizeWindow('image', 768, 432)
cv2.imshow('image', image)
print msglist[0]
cv2.setMouseCallback('image', click_event)
key = cv2.waitKey(0)
cv2.destroyAllWindows()
f = open("calibration.txt", "w")
f.write('\n'.join(pts))
f.close()


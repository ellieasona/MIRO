#############
# Allows for simple writing of code to be used with Consequential robotics MIRO robot
# UPDATE TO BE THE HANDLER FOR THE SCHEDULER!!!!


import math
import time

from interfaces import *



class SchedulerInterface:

    def __init__(self, robotname, linear, angular):
        self.default_linear = linear
        self.default_angular = angular
        self.pint = primary_interface(robotname)

    # takes initial_turn and final_turn in radians and distance in meters
    def movetoposition(self, initial_turn, distance, final_turn):
        initial = float(initial_turn)
        dist = float(distance)
        final = float(final_turn)
        # do initial turn
        if initial >= 0:
            self.pint.turn(2)
        else:
            self.pint.turn(-2)
            initial *= -1
        time.sleep(initial/2.0)
        self.pint.stop_moving()
        # move distance
        self.pint.drive_straight(.2)
        time.sleep(dist/.2)
        self.pint.stop_moving()
        # do final turn
        if final >= 0:
            self.pint.turn(2)
        else:
            self.pint.turn(-2)
            final *= -1
        time.sleep(final/2.0)
        self.pint.stop_moving()
        #
        #
        # while not rospy.is_shutdown():
        #     # create your if statement based sensor routine here
        #
        #     if 1 in self.pint.touch_body:
        #         self.pint.stop_moving()
        #         self.pint.tail_move()
        #         self.pint.head_move(1)
        #         time.sleep(.5)  # was .5
        #         while 1 in self.pint.touch_body:
        #             self.pint.tail_move()
        #             self.pint.ear_rotate = [0, 1]
        #             time.sleep(.75)
        #             self.pint.head_move(.9)
        #             self.pint.play_sound(2)
        #             self.pint.ear_rotate = [1, 0]
        #             time.sleep(.75)
        #             self.pint.head_move(1)
        #             self.pint.ear_rotate = [0, 1]
        #         self.pint.head_move()
        #     elif 1 in self.pint.touch_head:
        #         self.pint.stop_moving()
        #         self.pint.head_nod_sideways()
        #         time.sleep(.5)
        #
        #     else:
        #         self.pint.drive_straight(.1)

    def stop(self):
        self.pint.stop_moving()





#############
# Allows for simple writing of code to be used with Consequential robotics MIRO robot
# Created by Sidharth Babu  7/12/2018
# default behavior is to move around whilst avoiding any obstacles and reacting to touch

# Methods added from Jacob Gloudemans' work

import math
import rospy
from camera_stream import camera_stream

from interfaces import *



class SecondaryInterface:

    def __init__(self, robotname, linear, angular):
        self.default_linear = linear
        self.default_angular = angular
        self.pint = primary_interface(robotname)

    def defaultmovestate(self):
        # utilizes the sonar sensors so that
        # the robot can move around without hitting things
        self.pint.ear_rotate = [1, 0]  # move one ear
        self.pint.head_move(0, .2)  # turn to left side
        time.sleep(.2)
        x = self.pint.sonar_range  # left side turn range value
        time.sleep(.2)
        self.pint.head_move()  # set to middle
        self.pint.ear_rotate = [0, 0]  # set ears to normal
        time.sleep(.2)
        self.pint.head_move(0, -.2)  # turn to right side
        self.pint.ear_rotate = [0, 1]  # move other ear
        time.sleep(.2)
        y = self.pint.sonar_range  # right side turn range value
        time.sleep(.2)

        if x > 0 and y > 0:  # make sure its registering some value
            z = (x + y) / 2  # average distance from both sides
            self.pint.head_move()  # set back to middle
            print(str(x) + '| leftval')
            print(str(y) + '| rightval')


            if z < .3:  # its too close; get away
                print('straight back')
                self.pint.tail_move(-1)
                self.pint.drive_straight(-.1) # CHANGED TO .1
                time.sleep(2)
                self.pint.turn(math.pi/2.0)  # CHANGED TO /2.0
                time.sleep(1)
                self.pint.stop_moving()
                self.pint.tail_move(0)

            else:  # nothing too close

                if x > y:  # right side is closer than left; move left
                    print('left')
                    self.pint.turn(math.pi/2.0) # CHANGED TO /2.0
                    time.sleep(.25)
                    self.pint.drive_straight(.1) # CHANGED TO .1 FROM .2
                    time.sleep(1)
                    self.pint.stop_moving()

                elif y > x:  # left side is closer than right; move right
                    print('right')
                    self.pint.turn(-math.pi/2.0) # /2.0
                    time.sleep(.25)
                    self.pint.drive_straight(.1) # .1
                    time.sleep(1)
                    self.pint.stop_moving()

                elif y == x:  # both sides are equidistant
                    print('straight forward')
                    self.pint.drive_straight(.1) # .1
                    time.sleep(.5)
                    self.pint.stop_moving()

        else:  # if nothing registers, move until something does
            self.pint.drive_straight(.1) # .1 NOT ,2
            time.sleep(.5)
            self.pint.stop_moving()

    def sensorinterrupt(self):
        while not rospy.is_shutdown():
            # create your if statement based sensor routine here
            if 1 in self.pint.touch_body:
                self.pint.stop_moving()
                self.pint.tail_move()
                self.pint.head_move(1)
                time.sleep(.5)  # was .5
                while 1 in self.pint.touch_body:
                    self.pint.tail_move()
                    self.pint.ear_rotate = [0, 1]
                    time.sleep(.75)
                    self.pint.head_move(.9)
                    self.pint.ear_rotate = [1, 0]
                    time.sleep(.75)
                    self.pint.head_move(1)
                    self.pint.ear_rotate = [0, 1]
                self.pint.head_move()
            elif 1 in self.pint.touch_head:
                self.pint.stop_moving()
                self.pint.head_nod_sideways()
                time.sleep(.5)

            else:
                self.defaultmovestate()

    def stop(self):
        self.pint.stop_moving()





    # def loud_sound_move(self):
    #     self.mic = rospy.Subcriber("/miro/" + self.robot_name + "/platform/mics", platform_mics,
    #                                self.mic, queue_size=1)
    #
    # def mic(self, data):
    #
    #     left_mic = []
    #     right_mic = []
    #     even_cnt = 1
    #     linear = 0
    #     angular = 0
    #
    #     # reverse interleaving to seperate left and right ear data and store in individual lists
    #     for x in range(4000):
    #         if even_cnt == 1:
    #
    #             left_mic.append(data.data[x])
    #             even_cnt = 0
    #
    #         elif even_cnt == 0:
    #
    #             right_mic.append(data.data[x])
    #             even_cnt = 1
    #
    #     # find maximum cross correlation of mics
    #     if left_mic:
    #         max_mic = max(left_mic)
    #         max_mic_index = left_mic.index(max_mic)
    #         left_mic[max_mic_index - 50:max_mic_index + 50]
    #         right_mic[max_mic_index - 50:max_mic_index + 50]
    #         corr = numpy.ndarray.tolist(numpy.correlate(left_mic, right_mic, "same"))
    #         max_corr = max(corr[994:1006])
    #         max_index = corr.index(max_corr)
    #
    #     # if sound is sufficiently loud, move towards sound source
    #     if max_corr > 400000:
    #
    #         if max_index >= 994 and max_index <= 995:
    #             linear = .1
    #             angular = 1
    #             self.primary_int.update_body_vel(linear, angular)
    #             time.sleep(1.4)
    #         elif max_index >= 996 and max_index <= 997:
    #             linear = .1
    #             angular = 1
    #             self.primary_int.update_body_vel(linear, angular)
    #             time.sleep(1)
    #         elif max_index >= 998 and max_index <= 999:
    #             linear = .1
    #             angular = 1
    #             self.primary_int.update_body_vel(linear, angular)
    #             time.sleep(.6)
    #         elif max_index == 1000:
    #             linear = .1
    #             angular = 0
    #             self.primary_int.update_body_vel(linear, angular)
    #         elif max_index >= 1001 and max_index <= 1002:
    #             linear = .1
    #             angular = -1
    #             self.primary_int.update_body_vel(linear, angular)
    #             time.sleep(.6)
    #         elif max_index >= 1003 and max_index <= 1004:
    #             linear = .1
    #             angular = -1
    #             self.primary_int.update_body_vel(linear, angular)
    #             time.sleep(1)
    #         elif max_index >= 1005 and max_index <= 1006:
    #             linear = .1
    #             angular = -1
    #             self.primary_int.update_body_vel(linear, angular)
    #             time.sleep(1.4)
    #         angular = 0
    #         self.primary_int.update_body_vel(linear, angular)
    #
    #     if self.primary_int.sonar_range < .3 and self.primary_int.sonar_range != 0.0:
    #         linear = 0
    #
    # self.primary_int.update_body_vel(linear, angular)
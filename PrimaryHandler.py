#############
# Allows for simple writing of code to be used with Consequential robotics MIRO robot
# Created by Sidharth Babu  7/12/2018
# default behavior is to move around whilst avoiding any obstacles and reacting to touch


import math
import rospy
import time

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

        if x > 0 and y > 0 and not self.checkInterrupt():  # make sure its registering some value
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

        elif not self.checkInterrupt():  # if nothing registers, move until something does
            self.pint.drive_straight(.1) # .1 NOT ,2
            time.sleep(.5)
            self.pint.stop_moving()

    def sensorinterrupt(self):
        while not rospy.is_shutdown():
            # create your if statement based sensor routine here
            self.pint.move_to_sound()
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
                    #self.pint.play_sound(2)
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

    def checkInterrupt(self):
        if 1 in self.pint.touch_body:
            return True
        if 1 in self.pint.touch_head:
            return True



# Necessary imports

import sys

sys.path.append("/opt/ros/catkin_pkg/src")
sys.path.append("/home/root/mdk/share")
sys.path.append("/opt/ros/kinetic/lib/python2.7/dist-packages")

import rospy

from std_msgs.msg import String
from geometry_msgs.msg import Twist, Pose2D
from sensor_msgs.msg import Temperature, Imu, JointState, Range
from nav_msgs.msg import Odometry
from array import array
from miro_msgs.msg import platform_control, platform_sensors, platform_mics, bridge_stream, bridge_config
import numpy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import time
import operator


# -------------------------------------------------------------------------------------#
#
# An interface for reading / controlling most sensors / actuators of miro. Subscriber
# recieves sensor data messages from the robot at ~50hz and publishes a control command
# whenever a sensor message is recieved. To read current value of a sensor, simply
# read the platform_interface.[sensor of interest] to get the value. Similarly, to
# command the robot, modify the appropriate class variable. This effectively routes all
# publishing and subscribing to/from the primary robot interfaces through a
# single publisher and subscriber so that each class need not create its own
#
# This class is an 'extended singleton' so there can only be one instance of the class
# for a given robot name. This prevents useless duplication if multiple other programs
# want to access the camera stream from the same robot
#
# Created by Jacob Gloudemans and James Zhu
# 2/15/2018
#
# -------------------------------------------------------------------------------------#
# -------------------------------------------------------------------------------------#


class primary_interface:
    class __primary_interface:

        def __init__(self, robot_name):
            # Main publisher / subscriber
            root = "/miro/" + str(robot_name) + "/platform"
            self.cmd_out = rospy.Publisher(root + "/control", platform_control, queue_size=1)
            self.data_in = rospy.Subscriber(root + "/sensors", platform_sensors, self.data_in, queue_size=1)
            self.name = robot_name

            # List to track which flags to update after new data recieved
            self.relevant_flags = []

            # Sensors
            self.battery_voltage = 0.0
            self.temperature = None
            self.accel_head = None
            self.accel_body = None
            self.odometry = None
            self.joint_state = None
            self.eyelid_closure = None
            self.sonar_range = None
            self.light = None
            self.touch_head = [0,0,0,0]
            self.touch_body = [0,0,0,0]
            self.cliff = None

            # Actuators
            self.body_vel = Twist()
            self.body_config = [0.0, 0.0, 0.0, 0.0]
            self.body_config_speed = [0.0, 0.0, 0.0, 0.0]
            self.body_move = Pose2D()
            self.tail = 0.0
            self.ear_rotate = [0.0, 0.0]
            self.eyelid_closure_out = 0.0
            self.blink_time = 0
            self.lights_max_drive = 127
            self.lights_dphase = 0
            self.lights_phase = 0
            self.lights_amp = 0
            self.lights_off = 0
            self.lights_rgb = [0, 0, 0]
            self.sound_index_P1 = 0
            self.sound_index_P2 = 0

        def data_in(self, data):
            # Update sensor variables
            self.battery_voltage = data.battery_voltage
            self.temperature = data.temperature.temperature
            self.accel_head = data.accel_head  # Imu message type
            self.accel_body = data.accel_body  # Imu message type
            self.odometry = data.odometry  # Odometry message type
            self.joint_state = data.joint_state  # JointState message type
            self.eyelid_closure = data.eyelid_closure
            self.sonar_range = data.sonar_range.range
            self.light = list(array("B", data.light))
            self.touch_head = list(array("B", data.touch_head))
            self.touch_body = list(array("B", data.touch_body))
            self.cliff = list(array("B", data.cliff))

            # Output new control command
            cmd = platform_control()
            cmd.body_vel = self.body_vel
            cmd.body_config = self.body_config
            cmd.body_config_speed = self.body_config_speed
            cmd.body_move = self.body_move
            cmd.tail = self.tail
            cmd.ear_rotate = self.ear_rotate
            cmd.eyelid_closure = self.eyelid_closure_out
            cmd.blink_time = self.blink_time
            cmd.lights_max_drive = self.lights_max_drive
            cmd.lights_dphase = self.lights_dphase
            cmd.lights_phase = self.lights_phase
            cmd.lights_amp = self.lights_amp
            cmd.lights_off = self.lights_off
            cmd.lights_rgb = self.lights_rgb
            cmd.sound_index_P1 = self.sound_index_P1
            cmd.sound_index_P2 = self.sound_index_P2
            self.cmd_out.publish(cmd)

            # Update relevant flags
            for flag in self.relevant_flags:
                flag.update()

        ### Methods to simplify development ###

        # Updates the body_vel to the specified values (in m/s and rad/sec)
        def update_body_vel(self, linear, angular):
            twist = Twist()
            twist.linear.x = linear * 1000.0
            twist.angular.z = angular
            self.body_vel = twist

        # Sets individual wheels to given speeds in mm/s
        def set_wheel_speeds(self, speed_l, speed_r):
            dr = (speed_l + speed_r) / (2.0 / 1000)
            dtheta = (speed_r - speed_l) / (MIRO_WHEEL_TRACK_MM / 1000)
            self.update_body_vel(dr, dtheta)

        # Stops all robot movement
        def stop_moving(self):
            self.update_body_vel(0, 0)

        # Causes robot to drive straight at given speed in m/s
        def drive_straight(self, speed=0.1): #chaged from .2 to .1
            self.update_body_vel(speed, 0)

        # Turn at the given velocity in rad/sec
        def turn(self, speed):
            self.update_body_vel(0, speed)

        # Move head joints
        def head_move(self, lift=0.296705973, yaw=0, pitch=0.295833308, speed=-1):
            self.body_config = [0, lift, yaw, pitch]
            self.body_config_speed = [speed, speed, speed, speed]

        def tail_move(self, wag=1):
            self.tail = wag

        def head_nod_sideways(self,yaw=.2):
            self.body_config = [0, 0, yaw, 0]
            time.sleep(.25)
            self.body_config = [0, 0, -yaw, 0]
            time.sleep(.25)
            self.head_move()


        def play_sound(self, sound_num):
            sound_behavior = sound_interface(self.name)
            sound_behavior.data_in(sound_num)

        # def move_to_sound(self):
        #     mic_behavior = mic_interface(self.name)
        #     mic_behavior.data_in()

        def pet_pat(self):
            self.body_config_speed = [5, 5, 5, 5]
            if self.touch_body:

                # find average value of body touch
                try:
                    # avg body touch algorithm
                    self.value = 0.0
                    self.value = numpy.average(self.touch_body)
                    print (self.touch_body)
                    print(self.value)
                except ZeroDivisionError:
                    self.value = 0

                    if self.value > 0: # 0.5 >= self.value > 0: #governs behavior when PETTED
                        self.stop_moving()
                        self.tail_move(1)
                        self.body_config = [0, 0, 0, 1]
                        time.sleep(.5) # was .5
                        self.body_config = [0, 0, 0, 0]
                    elif self.value > 0.5: # governs behavior when PATTED
                        self.stop_moving()
                        self.tail_move(1)
                        self.body_config = [0, 0, .2, 0]
                        time.sleep(1) # was .25
                        self.body_config = [0, 0, -2, 0]
                        time.sleep(.25)
                        self.body_config = [0, 0, 0, 0]

    ##########################################################################################
    # Stuff below here ensures that only one instance of this class is created for any robot #
    ##########################################################################################

    instances = {}

    def __init__(self, name):

        # Keeps track of which __miro_robot instance this object cares about
        self.robot_name = name

        # if instance already exists for robot do nothing, otherwise make a new one
        if name in primary_interface.instances:
            pass
        else:
            primary_interface.instances[name] = primary_interface.__primary_interface(name)

    def __getattr__(self, attr):
        return getattr(primary_interface.instances[self.robot_name], attr)

    def __setattr__(self, attr, value):
        if attr == "robot_name":
            self.__dict__["robot_name"] = value
        else:
            setattr(primary_interface.instances[self.robot_name], attr, value)


# -------------------------------------------------------------------------------------#
#
# An interface for reading frames from the left and right cameras of the MIRO
# Two class instance variables are kept updated with the most recently recieved
# frame from each of the MIRO's cameras. Images are formatted as cv2 image objects
#
# This class is an 'extended singleton' so there can only be one instance of the class
# for a given robot name. This prevents useless duplication if multiple other programs
# want to access the camera stream from the same robot
#
# Created by Jacob Gloudemans and James Zhu
# 2/20/18
#
# -------------------------------------------------------------------------------------#
# -------------------------------------------------------------------------------------#


class camera_interface:
    class __camera_interface:

        def __init__(self, robot_name):
            root = "/miro/" + str(robot_name) + "/platform"
            self.left_stream = rospy.Subscriber(root + "/caml", Image, self.left_cam_callback, queue_size=1)
            self.right_stream = rospy.Subscriber(root + "/camr", Image, self.right_cam_callback, queue_size=1)
            self.bridge = CvBridge()
            self.cur_img_left = None
            self.cur_img_right = None
            self.cur_img_left_ID = None
            self.cur_img_right_ID = None

            # List to track which flags to update after new data recieved
            self.relevant_flags = []

        def left_cam_callback(self, data):
            new_img = self.bridge.imgmsg_to_cv2(data, "bgr8")
            self.cur_img_left = new_img
            self.cur_img_left_ID = "left_" + str(rospy.get_rostime())
            self.update_flags()

        def right_cam_callback(self, data):
            new_img = self.bridge.imgmsg_to_cv2(data, "bgr8")
            self.cur_img_right = new_img
            self.cur_img_left_ID = "right_" + str(rospy.get_rostime())
            self.update_flags()

        def update_flags(self):
            for flag in self.relevant_flags:
                flag.update()

    ##########################################################################################
    # Stuff below here ensures that only one instance of this class is created for any robot #
    ##########################################################################################

    instances = {}

    def __init__(self, name):

        # Keeps track of which __camera_interface instance this object cares about
        self.robot_name = name

        # if instance already exists for robot do nothing, otherwise make a new one
        if name in camera_interface.instances:
            pass
        else:
            camera_interface.instances[name] = camera_interface.__camera_interface(name)

    def __getattr__(self, attr):
        return getattr(camera_interface.instances[self.robot_name], attr)

    def __setattr__(self, attr, value):
        if attr == "robot_name":
            self.__dict__["robot_name"] = value
        else:
            setattr(camera_interface.instances[self.robot_name], attr, value)


# -------------------------------------------------------------------------------------#
#
# Plays different sounds uploaded onto P3 (SD card)
#
# This class is an 'extended singleton' so there can only be one instance of the class
# for a given robot name. This prevents useless duplication if multiple other programs
# want to access the sound stream from the same robot
#
# Created by James Zhu
# 2/20/18
#
# Adapted by Ellie Sona
# 10/5/18
#
# -------------------------------------------------------------------------------------#

class sound_interface:
    class __sound_interface:

        def __init__(self, robot_name):
            # Main publisher
            root = "/miro/" + robot_name + "/bridge"
            self.cmd_out = rospy.Publisher(root + "/stream", bridge_stream, queue_size=1)
            self.primary_int = primary_interface(robot_name)

        def data_in(self, sound_num):
            start_time = rospy.get_rostime()

            # output a sound with index between 1 and 3 (bark, pant, whimper)
            while (rospy.get_rostime() - start_time).to_sec() < .3:
                cmd = bridge_stream()
                cmd.sound_index_P3 = sound_num
                self.cmd_out.publish(cmd)
    ##########################################################################################
    # Stuff below here ensures that only one instance of this class is created for any robot #
    ##########################################################################################

    instances = {}

    def __init__(self, name):

        # Keeps track of which __camera_interface instance this object cares about
        self.robot_name = name

        # if instance already exists for robot do nothing, otherwise make a new one
        if name in sound_interface.instances:
            pass
        else:
            sound_interface.instances[name] = sound_interface.__sound_interface(name)

    def __getattr__(self, attr):
        return getattr(sound_interface.instances[self.robot_name], attr)

    def __setattr__(self, attr, value):
        if attr == "robot_name":
            self.__dict__["robot_name"] = value
        else:
            setattr(sound_interface.instances[self.robot_name], attr, value)


# -------------------------------------------------------------------------------------#
#
# Inputs microphone data for each ear and determines the direction of the sound source.
#
# This class is an 'extended singleton' so there can only be one instance of the class
# for a given robot name. This prevents useless duplication if multiple other programs
# want to access the sound stream from the same robot
#
# Created by James Zhu
# 2/20/18
#
# Adapted by Ellie Sona
# 10/5/18
#
# -------------------------------------------------------------------------------------#

# class mic_interface:
#     class __mic_interface:
#
#         def __init__(self, robot_name):
#             root = "/miro/" + str(robot_name) + "/platform"
#             self.data_in = rospy.Subscriber(root + "/mics", platform_mics, self.data_in, queue_size=1)
#             self.primary_int = primary_interface(robot_name)
#
#         def data_in(self, data):
#
#             left_mic = []
#             right_mic = []
#             even_cnt = 1
#             linear = 0
#             angular = 0
#
#             # reverse interleaving to seperate left and right ear data and store in individual lists
#             for x in range(4000):
#                 if even_cnt == 1:
#
#                     left_mic.append(data.data[x])
#                     even_cnt = 0
#
#                 elif even_cnt == 0:
#
#                     right_mic.append(data.data[x])
#                     even_cnt = 1
#
#             max_corr = 0
#             max_index = 0
#
#             # find maximum cross correlation of mics
#             if left_mic:
#                 max_mic = max(left_mic)
#                 max_mic_index = left_mic.index(max_mic)
#                 left_mic[max_mic_index - 50:max_mic_index + 50]
#                 right_mic[max_mic_index - 50:max_mic_index + 50]
#                 corr = numpy.ndarray.tolist(numpy.correlate(left_mic, right_mic, "same"))
#                 max_corr = max(corr[994:1006])
#                 max_index = corr.index(max_corr)
#
#             # if sound is sufficiently loud, move towards sound source
#             if max_corr > 400000:
#
#                 if max_index >= 994 and max_index <= 995:
#                     linear = .1
#                     angular = 1
#                     self.primary_int.update_body_vel(linear, angular)
#                     time.sleep(1.4)
#                 elif max_index >= 996 and max_index <= 997:
#                     linear = .1
#                     angular = 1
#                     self.primary_int.update_body_vel(linear, angular)
#                     time.sleep(1)
#                 elif max_index >= 998 and max_index <= 999:
#                     linear = .1
#                     angular = 1
#                     self.primary_int.update_body_vel(linear, angular)
#                     time.sleep(.6)
#                 elif max_index == 1000:
#                     linear = .1
#                     angular = 0
#                     self.primary_int.update_body_vel(linear, angular)
#                 elif max_index >= 1001 and max_index <= 1002:
#                     linear = .1
#                     angular = -1
#                     self.primary_int.update_body_vel(linear, angular)
#                     time.sleep(.6)
#                 elif max_index >= 1003 and max_index <= 1004:
#                     linear = .1
#                     angular = -1
#                     self.primary_int.update_body_vel(linear, angular)
#                     time.sleep(1)
#                 elif max_index >= 1005 and max_index <= 1006:
#                     linear = .1
#                     angular = -1
#                     self.primary_int.update_body_vel(linear, angular)
#                     time.sleep(1.4)
#                 angular = 0
#                 self.primary_int.update_body_vel(linear, angular)
#
#             if self.primary_int.sonar_range < .3 and self.primary_int.sonar_range != 0.0:
#                 linear = 0
#                 self.primary_int.update_body_vel(linear, angular)
#
#         ##########################################################################################
#         # Stuff below here ensures that only one instance of this class is created for any robot #
#         ##########################################################################################
#
#     instances = {}
#
#     def __init__(self, name):
#
#         # Keeps track of which __camera_interface instance this object cares about
#         self.robot_name = name
#
#         # if instance already exists for robot do nothing, otherwise make a new one
#         if name in mic_interface.instances:
#             pass
#         else:
#             mic_interface.instances[name] = mic_interface.__mic_interface(name)
#
#     def __getattr__(self, attr):
#         return getattr(mic_interface.instances[self.robot_name], attr)
#
#     def __setattr__(self, attr, value):
#         if attr == "robot_name":
#             self.__dict__["robot_name"] = value
#         else:
#             setattr(mic_interface.instances[self.robot_name], attr, value)

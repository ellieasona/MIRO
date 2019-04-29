
################################################################
# MIRO USER CONFIGURATION
#
# You may want to configure items in this section only, to begin
# with, as indicated in the documentation.

# uncomment these values to configure MIRO to run encapsulated
# "on-board", so the ROS master runs here as do ROS nodes.
ROS_IP=127.0.0.1
ROS_MASTER_IP=localhost

# if those values were not set, you can configure MIRO to use
# an off-board ROS master, in this section.
if [[ "$ROS_IP" == "" ]];
then

	# before ROS servers & clients are started, the value ROS_IP
	# must be set so that remote systems can find this node.
	#
	# if you leave ROS_IP blank, here, get_ROBOT_IP.sh can be
	# used to set it dynamically as ROS nodes are being started
	# (see run_bridge_ros.sh for an example).
	#
	# if you are using a static IP for your robot, you can as an
	# alternative set ROS_IP, here, to that IP and then you do
	# not need to run get_ROBOT_IP.sh when launching ROS nodes.
	ROS_IP=10.68.1.94

	# IP address of ROS master is needed so we can find it when
	# we start any ROS node locally. you should always set this
	# value if we are not running the ROS master locally.
	ROS_MASTER_IP=10.67.48.59

fi

# MIRO USER CONFIGURATION: END
################################################################



# MDK configuration
export MIRO_PATH_MDK=/home/root/mdk
export ROS_RELEASE=`cat $MIRO_PATH_MDK/config/ros_release`

# add a couple o' things to PATH
PATH=$PATH:/home/root/bin
PATH=$PATH:/usr/share/miro/bin
PATH=$PATH:$MIRO_PATH_MDK/bin/am335x
PATH=$PATH:$MIRO_PATH_MDK/bin/shared
PATH=$PATH:/opt/ros/$ROS_RELEASE/bin
PATH=$PATH:/opt/ros/catkin_pkg/bin

# provide ROS with its environment variables
export ROS_IP
export ROS_MASTER_URI=http://$ROS_MASTER_IP:11311

# usual ROS setup
source /opt/ros/kinetic/setup.bash

# add our bits of ROS setup
ROS_PACKAGE_PATH=$MIRO_PATH_MDK/share:$ROS_PACKAGE_PATH
PYTHONPATH=$MIRO_PATH_MDK/share:$PYTHONPATH
PYTHONPATH=/opt/ros/catkin_pkg/src:$PYTHONPATH

# needed for roswtf at jade, I think, because yocto is unknown
export ROS_OS_OVERRIDE=ubuntu


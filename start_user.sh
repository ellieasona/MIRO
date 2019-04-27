#!/bin/bash
source /home/root/.bashrc
source /home/root/.profile
source /opt/ros/kinetic/setup.bash                                  
                                                                    
# make sure all path's are set
ROS_PACKAGE_PATH=$MIRO_PATH_MDK/share:$ROS_PACKAGE_PATH
PYTHONPATH=$MIRO_PATH_MDK/share:$PYTHONPATH                         
PYTHONPATH=/opt/ros/catkin_pkg/src:$PYTHONPATH                      

export ROS_OS_OVERRIDE=ubuntu 


python /home/root/initiator.py &> /tmp/initiator.log

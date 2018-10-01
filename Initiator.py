import random
from PrimaryHandler import *
import multiprocessing
import threading
import time



def run(robot):
    robot.sensorinterrupt()
    return


def main():
    rospy.init_node('Demo', anonymous=True)
    miro1 = SecondaryInterface('rob01', 1, 6.283185307 / 2)
    miro2 = SecondaryInterface('rob02', 1, 6.283185307 / 2)

    threads = []
    t1 = threading.Thread(target=run, args=(miro1,))
    t1.setDaemon(True)
    threads.append(t1)
    print('is 1 daemon?', t1.isDaemon())
    t1.start()
    t2 = threading.Thread(target=run, args=(miro2,))
    t2.setDaemon(True)
    threads.append(t2)
    print ('is t2 daemmon?', t2.isDaemon())
    t2.start()
    while True:
        if t1.is_alive() is False or t2.is_alive() is False:
            break


if __name__ == "__main__":
    main()



# CHANGE TO PROCESSES
import random
from MIRO.PrimaryHandler import *
import multiprocessing


def run(robot):
    robot.sensorinterrupt()
    return


def main():
    rospy.init_node('Demo', anonymous=True)
    miro1 = SecondaryInterface('rob01', 1, 6.283185307 / 2)
    miro2 = SecondaryInterface('rob02', 1, 6.283185307 / 2)

    threads = []
    t1 = threading.Thread(target=run, args=(miro1,))
    #t1 = multiprocessing.Process(target=run, args=(miro1,))
    #t1.daemon = True
    threads.append(t1)
    t1.start()
    t2 = threading.Thread(target=run, args=(miro2,))
    #t2 = multiprocessing.Process(target=run, args=(miro2,))
    #t2.daemon = True
    threads.append(t2)
    t2.start()

    try:
        while 1:
            time.sleep(.1)
    except KeyboardInterrupt:
        print ("Attempting to close threads")
        #t1.terminate()
        #t2.terminate()


if __name__ == "__main__":
    main()

# CHANGE TO PROCESSES
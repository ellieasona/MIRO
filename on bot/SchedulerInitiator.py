from SchedulerHandler import *
import threading
import sys




def run(robot):
    robot.movetoposition(sys.argv[1], sys.argv[2], sys.argv[3])
    return


def main():
    rospy.init_node('Demo', anonymous=True)
    miro1 = SchedulerInterface('rob01', 1, 6.283185307 / 2)
    miro2 = SchedulerInterface('rob02', 1, 6.283185307 / 2)

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
        if not t1.is_alive() or not t2.is_alive():
            miro1.stop()
            miro2.stop()
            break


if __name__ == "__main__":
    main()
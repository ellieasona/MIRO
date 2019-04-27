#!/bin/python
import math
import paramiko
import CalculatePosAndDir as cpad



def main():

    cur_x, cur_y, cur_r = cpad.get_current_info()
    if cur_r > 180:
        cur_r -= 360.0
    print (cur_x, cur_y, cur_r)


    final_x = float(input("\nEnter the desired final x coordinate of the robot in meters with the back left corner "
                          "of the wall as the origin and all values positive: "))
    final_y = float(input("Enter the desired final y coordinate of the robot in meters with the back left corner "
                          "of the wall as the origin and all values positive: "))
    final_r = float(input("Enter the desired final rotation of the robot by the unit circle in degrees: "))

    cur_y *= -1  # address y coordinate flip
    final_y *= -1  # address y coordinate flip

    dist = math.hypot(final_x - cur_x, final_y - cur_y)
    angle_between = angleOfLine(cur_x, cur_y, final_x, final_y)
    initial_turn_angle = getDifference(cur_r, angle_between)
    final_turn_angle = getDifference(angle_between, final_r)
    print("dist: ", dist, "angle_between: ", angle_between, "initial_turn_angle: ", initial_turn_angle, "final_turn_angle: ", final_turn_angle)
    connection = False
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    while not connection:
        robot_user = "root" #raw_input("\nEnter the robot username (likely root): ")
        robot_ip = "10.68.1.92" #raw_input("Enter the robot IP address: ")
        robot_pass = "!amMIRO" #raw_input("Enter the robot password: ")
        statement = "Successfully connected to robot! Issuing commands..."
        connection = True
        try:
            print("\nAttempting to connect...ignore any warnings. ")
            ssh.connect(hostname=robot_ip, username=robot_user, password=robot_pass)
        except paramiko.BadHostKeyException:
            statement = "Host key could not be verified. Run command ssh-keygen -f \"/home/rasl/.ssh/known_hosts\" -R " + robot_ip + " and try again."
            connection = False
        except paramiko.AuthenticationException:
            statement = "Authentication error. Try again."
            connection = False
        except paramiko.SSHException:
            statement = "Issue connecting to robot over SSH. Check that robot is accessible " \
                        "via given SSH configuration and try again"
            connection = False
        except Exception as e:
            print(e)
            statement = " Try again"
            connection = False
        finally:
            print(statement)


    try:
        stdin, stdout, stderr = ssh.exec_command("~/bin/bridge_control.sh toggle_running")
        print("\nRunning bridge...")
    except paramiko.SSHException:
        print("Request rejected or channel closed")
    print(stdout.readlines())


    try:
        command = "/home/root/start_user.sh " + str(initial_turn_angle) + " " + str(dist) + " " + str(final_turn_angle)
        print("Sending move command: " + command + "\n This may take a few moments")
        stdin, stdout, stderr = ssh.exec_command(command)
    except paramiko.SSHException:
        print("Request rejected or channel closed")
    print(stdout.readlines())

    try:
        stdin, stdout, stderr = ssh.exec_command("~/bin/bridge_control.sh toggle_running")
        print("\nStopping bridge...")
    except paramiko.SSHException:
        print("Request rejected or channel closed")
    print(stdout.readlines())




def angleOfLine(x1, y1, x2, y2):
    xDiff = x2 - x1
    yDiff = y2 - y1
    return math.degrees(math.atan2(yDiff, xDiff))


def getDifference(b1, b2): #literally have never called this  method just copied and pasted look into it
    r = (b2 - b1) % 360.0
    # Python modulus has same sign as divisor, which is positive here,
    # so no need to consider negative case
    if r >= 180.0:
        r -= 360.0
    return math.radians(r)


if __name__ == "__main__":
    main()

#!/bin/python
import paramiko
import time
import math





connection = False
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
while not connection:
    robot_user = "root"  # raw_input("\nEnter the robot username (likely root): ")
    robot_ip = "10.68.1.92"  # raw_input("Enter the robot IP address: ")
    robot_pass = "!amMIRO"  # raw_input("Enter the robot password: ")
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


feet = 1.5

while feet <= 6:
    try:
        print ("feet: " + str(feet))
        command = "/home/root/start_user.sh 0 " + str(feet *.3048) + " 0"
        print (command)
        stdin, stdout, stderr = ssh.exec_command(command)

    except paramiko.SSHException:
        print("Request rejected or channel closed")
    print(stdout.readlines())

    cont = raw_input("continue")

    if cont == "quit":
        feet = 8
    else:
        feet += .5







try:
    stdin, stdout, stderr = ssh.exec_command("~/bin/bridge_control.sh toggle_running")
    print("\nStopping bridge...")
except paramiko.SSHException:
    print("Request rejected or channel closed")
print(stdout.readlines())
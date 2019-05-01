This repo contains the MIRO scheduler package. For more details, see the PDF operating manual located in this folder at https://github.com/ellieasona/MIRO/blob/master/MIRO%20Scheduler%20Manual.docx.
Code to be put on the robot itself is in the "on bot" folder, and code for your workstation
is in the "Scheduler" folder.


To run with current workstation and robot setup:
1. Turn robot on
2. Open new terminal on workstation
3. Change to correct directory with the following command:
```
cd ~/mdk/bin/shared/Scripts/MIRO/Scheduler
```
4. Run CameraCalibration or MovetoLocation:

```
python CameraCalibration.py
```
or
```
python MovetoLocation.py
```




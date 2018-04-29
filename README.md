# doorBot
Project for CIS 693
1- Download the freenect driver for kinect camera. <br/>
2- Clone this repositiory in the same workspace where localization package is (BWI in our case). <be/>

3- In a virtual environment, install Keras library(Only CPU is fine) and change the interpreter path on src/classify.py to the virtual environment.   <br/>

4- On the virtual environment, DO:
pip install catkin_pkg
pip install rospkg 

5- To start doing an experiment:

	roslaunch doorBot loc_camera.launch
	roslaunch doorBot background_people_detection.launch
	roslaunch doorBot savedata.launch


## [ MIRORI ]
The purpose of this project is to allow a connected mirror to serve as a personalized information point for trade fair/congress visitors.

To make this point of information personalized, we have chosen to deal with facial recognition (open source OpenCV project with facial_recognition lib) which allows us to automatically connect a visitor to our CMS solution. An acquisition module is also available on another repo, it allows to take the reference image/photo for facial recognition.

For a question of optimization, 2 ubuntu services were created on the raspberry of our project.

The flask server (<u>identification/server.py</u>) runs on the systemd/user because it must not be initiated by root & only by the main user (here it's `grav`), it is this service that will load most of the libraries.<br>
The detection program (<u>presence_detector.py</u>) runs in systemd/system since it needs to be initiated by root to have access to the GPIO.

All the links are absolute because of this services & because i don't use python environment for libs install
<hr>

## [ INSTALL ON RASPBERRY4 ]
`sudo apt install libopencv-dev python3-opencv`<br>
`python3 pip install`<br>
or
<br>
`wget https://bootstrap.pypa.io/get-pip.py`<br>
`sudo python3 get-pip.py && rm get-pip.py`<br>

`pip install face-recognition`<br>
`pip install python-dotenv`<br>
`pip install paramiko`<br>
`pip install scp`<br>
`pip install numpy`<br>
`sudo apt install -y cmake`<br>
`pip install dlib`  // Not the fastest way to install dlib<br> 
[Autopy need to read documentation for install](`https://pypi.org/project/autopy/`) // Autopy lib need small correction on MAKEFILE<br>
[Mediapipe compil for ARM64 - Instructions](https://github.com/jiuqiant/mediapipe_python_aarch64)

... & Maybe more

 ## [ PROJECT RESSOURCES ]<br>
<b>L42Project (Facial Recognition [FR]):</b> <br>
- [Facial Recognition - Video 1](https://www.youtube.com/watch?v=HHv_V2PkZGQ)
- [Facial Recognition - Repo (Video 1)](https://github.com/L42Project/Tutoriels/tree/master/Divers/tutoriel41)
- [Facial Recognition - Video 2](https://www.youtube.com/watch?v=tsiy3DgAKHk)

<b>Mohammadst99 repo:</b><br>
- [Virtual Mouse](https://github.com/mohammadst99/VirtualMouse_openCV)

<b>SR04 Instructions:</b><br>
- [TUTO FR](https://raspberry-lab.fr/Composants/Mesure-de-distance-avec-HC-SR04-Raspberry-Francais/)

 ### [ PROBLEMS ]
 OpenCV function imshow segfault. [GITHUB ISSUE](https://github.com/opencv/opencv-python/issues/572) <br>
 RESOLUTION: remove opencv installation with apt & install the github version.

  FOR OPENCV 4.5.5 version from github official repo you need to use cmake with a flag: <br>
  `` cmake ../ -D PYTHON3_PACKAGES_PATH=/usr/lib/python3/dist-packages ``

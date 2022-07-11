


[PROBLEMS]
 opencv function imshow segfault. FOUND HERE: https://github.com/opencv/opencv-python/issues/572 RESOLUTION: remove opencv installation with apt & install the github version.

[INSTALL on RASPBERRY4]
 FOR OPENCV 4.5.5 version from github official repo you need to use cmake with a flag
 ``` cmake ../ -D PYTHON3_PACKAGES_PATH=/usr/lib/python3/dist-packages ```

 Autopy lib need correction on MAKEFILE
 Mediapipe solution for Raspberry : https://github.com/jiuqiant/mediapipe_python_aarch64   

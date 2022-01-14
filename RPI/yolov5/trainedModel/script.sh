#!/bin/sh
cd ~
cd Documents
cd mdp
source mdp/bin/activate
cd /YOLOV5/yolov5-master
python detect.py --weights /Users/nicksonng/Documents/MDP/YOLOV5/yolov5-master/trainedModel/exp/weights/last.pt --img 640 --conf 0.25 --source '1'
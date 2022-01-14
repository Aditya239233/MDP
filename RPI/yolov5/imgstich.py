
from imutils import paths
import imutils
from PIL import Image
import cv2
import numpy as np

def concat_tile(im_list_2d):
    return cv2.vconcat([cv2.hconcat(im_list_h) for im_list_h in im_list_2d])



print("[INFO] loading images...")
imagePaths = sorted(list(paths.list_images("/Users/nicksonng/Documents/MDP/YOLOV5/yolov5-master/runs/detect/")))
images = []
for imagePath in imagePaths:
    image = cv2.imread(imagePath)
    images.append(image)
print("[INFO] stitching images...")
width,height,channel = images[0].shape

blank_image = np.zeros((width,height,channel), np.uint8)
extra = (len(images)%3)+1
for i in range(0,extra):
    images.append(blank_image)
    print("Extra")

tileImg= []
row = []
count = 1
for i in images:
    i = cv2.resize(i,(0,0),None,0.6,0.6)
    row.append(i)
    count = count +1
    if count == 3:
        tileImg.append(row)
        row=[]
        count = 1
im_tile = concat_tile(tileImg)
   
cv2.imshow('result',im_tile)
cv2.waitKey(0)
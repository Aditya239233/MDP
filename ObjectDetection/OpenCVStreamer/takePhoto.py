import os
import sys
import numpy as np
from datetime import datetime
import imagezmq
import cv2

IMG_ENCODING = '.png'
dir_path = os.path.dirname(os.path.realpath(__file__)) + "/raw_images"
SOURCE = dir_path
image_hub = imagezmq.ImageHub()

print('\nStarted Image Processing Server.\n')
while True:  # show streamed images until Ctrl-C
    print('Waiting for image from RPI...', flush=True)
    rpi_name, image = image_hub.recv_image()
    print('Connected and received frame at time: %s' % str(datetime.now()), flush=True)
    # form image file path for saving
    raw_image_name = rpi_name.replace(':', '') + ' ' + str(datetime.now().strftime('%d-%b_%H-%M-%S')) + IMG_ENCODING
    raw_image_path = os.path.join(SOURCE, raw_image_name)
    print(str(raw_image_path))
    save_success = cv2.imwrite(raw_image_path, image)
    print(raw_image_path)
    print('Successfully saved')
    cv2.waitKey(1)
    image_hub.send_reply(b'OK')

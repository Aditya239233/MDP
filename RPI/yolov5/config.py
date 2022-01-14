from pathlib import Path
FILELOCATION = Path.cwd()  # /home/skovorodkin/stack

#IMAGE DETECTION CONFIGS
WEIGHTSPATH = f"{FILELOCATION}/trainedModel/exp/weights/best.pt"
IMGCONF = 640
CONF = 0.55#0.25
SOURCE = '1'#0 FOR WEBCAM, 1 FOR RASPBERRY PI CAMERA, OR URL TO VIDEO
PORT = 1231
PI_IP= "192.168.26.1" # original pi ip

FONT_SIZE = 6


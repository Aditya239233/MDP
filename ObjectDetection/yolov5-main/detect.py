# YOLOv5 🚀 by Ultralytics, GPL-3.0 license
"""
Run inference on images, videos, directories, streams, etc.

Usage:
    $ python path/to/detect.py --source path/to/img.jpg --weights yolov5s.pt --img 640
"""

from config import WEIGHTSPATH, IMGCONF, CONF, SOURCE
import argparse
import sys
import time
from pathlib import Path
import os
from imutils import paths
import imutils
from PIL import Image
import socket

import cv2
import numpy as np
import torch
import torch.backends.cudnn as cudnn

from algorithm.planner.main import Runner

FILE = Path(__file__).absolute()
sys.path.append(FILE.parents[0].as_posix())  # add yolov5/ to path

from models.experimental import attempt_load
from utils.datasets import LoadStreams, LoadImages
from utils.general import check_img_size, check_requirements, check_imshow, colorstr, is_ascii, non_max_suppression, \
    apply_classifier, scale_coords, xyxy2xywh, strip_optimizer, set_logging, increment_path, save_one_box
from utils.plots import Annotator, colors
from utils.torch_utils import select_device, load_classifier, time_sync

def concat_tile(im_list_2d):
    return cv2.vconcat([cv2.hconcat(im_list_h) for im_list_h in im_list_2d])

def stichImg(imgpath):
    print("[INFO] loading images...")
    imagePaths = sorted(list(paths.list_images(imgpath)))
    images = []
    for imagePath in imagePaths:
        image = cv2.imread(imagePath)
        images.append(image)
    print("[INFO] stitching images...")
    width,height,channel = images[0].shape #get sample width and height

    #gen blank images to fill up space
    blank_image = np.zeros((width,height,channel), np.uint8)
    extra = (len(images)%3)+1
    for i in range(0,extra):
        images.append(blank_image)
        

    #arrange into tiles
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
        
    cv2.imwrite(f"{imgpath}/stiched.png", im_tile)
    cv2.imshow('results',im_tile)
    cv2.waitKey(0)

def stichandshow(img_map,save_path):
    for key in img_map:
        if len(img_map[key])>1:
            actualID = key +1
            res = cv2.imwrite(f"{save_path[:-1]}{actualID}.JPG", img_map[key])
        #print(img_stats)
        
        stichImg(save_path[:-1])
        #os._exit(0)
    

@torch.no_grad()
def run(weights='yolov5s.pt',  # model.pt path(s)
        source='data/images',  # file/dir/URL/glob, 0 for webcam
        imgsz=640,  # inference size (pixels)
        conf_thres=0.25,  # confidence threshold
        iou_thres=0.45,  # NMS IOU threshold
        max_det=1000,  # maximum detections per image
        device='',  # cuda device, i.e. 0 or 0,1,2,3 or cpu
        view_img=False,  # show results
        save_txt=False,  # save results to *.txt
        save_conf=False,  # save confidences in --save-txt labels
        save_crop=False,  # save cropped prediction boxes
        nosave=False,  # do not save images/videos
        classes=None,  # filter by class: --class 0, or --class 0 2 3
        agnostic_nms=False,  # class-agnostic NMS
        augment=False,  # augmented inference
        visualize=False,  # visualize features
        update=False,  # update all models
        project='runs/detect',  # save results to project/name
        name='exp',  # save results to project/name
        exist_ok=False,  # existing project/name ok, do not increment
        line_thickness=3,  # bounding box thickness (pixels)
        hide_labels=False,  # hide labels
        hide_conf=False,  # hide confidences
        half=False,  # use FP16 half-precision inference
        ):


    #ASSIGN CONFIGS
    weights = WEIGHTSPATH  # file/dir/URL/glob, 0 for webcam
    imgsz = IMGCONF  # inference size (pixels)
    conf_thres = CONF  # confidence threshold
    source = SOURCE  # file/dir/URL/glob, 0 for webcam
    #END OF ASSIGNING CONFIGS
    samplingFrames = 9

    img_stats_buffer = []
    img_stats = {}
    img_queue = []
    img_queue_path = []
    img_map = {}

    android_data={}
    obstacle_num = 1
    lastsentid = -1
    #img_map ={0 = '' , 1= '' , 2='', 3= '', 4 = '' , 5= '' , 6= '', 7 = '' , 8= '' , 9= '', 10 = '' , 11= '' , 12= '', 13='' , 14 = '' , 15= '' , 16= '', 17 = '' , 18= '' , 19= '',20 = '' , 21= '' , 22 ='', 23= '', 24 = '' , 25= '' , 26= '', 27 = '' , 28 = '' , 29 = '', 30 = ''}


    if(source=='1'):#rpi
        print("in rpi")
        from PiTransmitter import sendData,getAndroidData
        
        # while True:
        #     result = getAndroidData()
        #     if (result=="start"):
        #         android_data = getAndroidData()
        #         runner = Runner(android_data) # android_data is the raw string from android
        #         instructions, android_coor = runner.run()

        #         sendData(instructions, "stm")
        #         sendData(android_coor, "android")
                
        #         break

    android_data = getAndroidData()
    runner = Runner(android_data) # android_data is the raw string from android
    instructions, android_coor = runner.run()

    sendData(instructions, "stm")
    sendData(android_coor, "android")
            
    


    save_img = not nosave and not source.endswith('.txt')  # save inference images
    webcam = source.isnumeric() or source.endswith('.txt') or source.lower().startswith(
        ('rtsp://', 'rtmp://', 'http://', 'https://'))
    
    usePi = False
    if source=='1':
        usePi = True 

    # Directories
    save_dir = increment_path(Path(project) / name, exist_ok=exist_ok)  # increment run
    (save_dir / 'labels' if save_txt else save_dir).mkdir(parents=True, exist_ok=True)  # make dir

    # Initialize
    set_logging()
    device = select_device(device)
    half &= device.type != 'cpu'  # half precision only supported on CUDA

    # Load model
    w = weights[0] if isinstance(weights, list) else weights
    classify, suffix = False, Path(w).suffix.lower()
    pt, onnx, tflite, pb, saved_model = (suffix == x for x in ['.pt', '.onnx', '.tflite', '.pb', ''])  # backend
    stride, names = 64, [f'class{i}' for i in range(1000)]  # assign defaults
    if pt:
        model = attempt_load(weights, map_location=device)  # load FP32 model
        stride = int(model.stride.max())  # model stride
        names = model.module.names if hasattr(model, 'module') else model.names  # get class names
        if half:
            model.half()  # to FP16
        if classify:  # second-stage classifier
            modelc = load_classifier(name='resnet50', n=2)  # initialize
            modelc.load_state_dict(torch.load('resnet50.pt', map_location=device)['model']).to(device).eval()
    elif onnx:
        check_requirements(('onnx', 'onnxruntime'))
        import onnxruntime
        session = onnxruntime.InferenceSession(w, None)
    else:  # TensorFlow models
        check_requirements(('tensorflow>=2.4.1',))
        import tensorflow as tf
        if pb:  # https://www.tensorflow.org/guide/migrate#a_graphpb_or_graphpbtxt
            def wrap_frozen_graph(gd, inputs, outputs):
                x = tf.compat.v1.wrap_function(lambda: tf.compat.v1.import_graph_def(gd, name=""), [])  # wrapped import
                return x.prune(tf.nest.map_structure(x.graph.as_graph_element, inputs),
                               tf.nest.map_structure(x.graph.as_graph_element, outputs))

            graph_def = tf.Graph().as_graph_def()
            graph_def.ParseFromString(open(w, 'rb').read())
            frozen_func = wrap_frozen_graph(gd=graph_def, inputs="x:0", outputs="Identity:0")
        elif saved_model:
            model = tf.keras.models.load_model(w)
        elif tflite:
            interpreter = tf.lite.Interpreter(model_path=w)  # load TFLite model
            interpreter.allocate_tensors()  # allocate
            input_details = interpreter.get_input_details()  # inputs
            output_details = interpreter.get_output_details()  # outputs
            int8 = input_details[0]['dtype'] == np.uint8  # is TFLite quantized uint8 model
    imgsz = check_img_size(imgsz, s=stride)  # check image size
    

    ascii = is_ascii(names)  # names are ascii (use PIL for UTF-8)

    # Dataloader
    if usePi:
        
        print("Connecting to rpi....")
        #_,frame = image_hub.recv_image()
       
        #im = cv2.imread(frame)
        #print(frame.shape)
        view_img=True;
        dataset = LoadStreams(source, img_size=imgsz, stride=stride, auto=pt)
        bs = len(dataset)  # batch_size
        
        #image_hub.send_reply(b'OK')
        print("Done")
       


    elif webcam:
        view_img = check_imshow()
        print(f"View img is {view_img}")
        cudnn.benchmark = True  # set True to speed up constant image size inference
        print(f"Source is {source}")
        dataset = LoadStreams(source, img_size=imgsz, stride=stride, auto=pt)
        bs = len(dataset)  # batch_size
    else:
        dataset = LoadImages(source, img_size=imgsz, stride=stride, auto=pt)
        bs = 1  # batch_size
    vid_path, vid_writer = [None] * bs, [None] * bs

    # Run inference
    if pt and device.type != 'cpu':
        model(torch.zeros(1, 3, *imgsz).to(device).type_as(next(model.parameters())))  # run once
    t0 = time.time()
    

    for path, img, im0s, vid_cap in dataset:

        if onnx:
            img = img.astype('float32')
        else:
            img = torch.from_numpy(img).to(device)
            img = img.half() if half else img.float()  # uint8 to fp16/32
        img = img / 255.0  # 0 - 255 to 0.0 - 1.0
        if len(img.shape) == 3:
            img = img[None]  # expand for batch dim

        # Inference
        t1 = time_sync()
        if pt:
            visualize = increment_path(save_dir / Path(path).stem, mkdir=True) if visualize else False
            pred = model(img, augment=augment, visualize=visualize)[0]
        elif onnx:
            pred = torch.tensor(session.run([session.get_outputs()[0].name], {session.get_inputs()[0].name: img}))
        else:  # tensorflow model (tflite, pb, saved_model)
            imn = img.permute(0, 2, 3, 1).cpu().numpy()  # image in numpy
            if pb:
                pred = frozen_func(x=tf.constant(imn)).numpy()
            elif saved_model:
                pred = model(imn, training=False).numpy()
            elif tflite:
                if int8:
                    scale, zero_point = input_details[0]['quantization']
                    imn = (imn / scale + zero_point).astype(np.uint8)  # de-scale
                interpreter.set_tensor(input_details[0]['index'], imn)
                interpreter.invoke()
                pred = interpreter.get_tensor(output_details[0]['index'])
                if int8:
                    scale, zero_point = output_details[0]['quantization']
                    pred = (pred.astype(np.float32) - zero_point) * scale  # re-scale
            pred[..., 0] *= imgsz[1]  # x
            pred[..., 1] *= imgsz[0]  # y
            pred[..., 2] *= imgsz[1]  # w
            pred[..., 3] *= imgsz[0]  # h
            pred = torch.tensor(pred)

        # NMS
        pred = non_max_suppression(pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)
        t2 = time_sync()

        

        # Second-stage classifier (optional)
        if classify:
            print("runed classifier")
            pred = apply_classifier(pred, modelc, img, im0s)

        # Process predictions
        for i, det in enumerate(pred):  # detections per image
            if webcam:  # batch_size >= 1
                p, s, im0, frame = path[i], f'{i}: ', im0s[i].copy(), dataset.count
            else:
                p, s, im0, frame = path, '', im0s.copy(), getattr(dataset, 'frame', 0)

            p = Path(p)  # to Path
            save_path = str(save_dir / p.name)  # img.jpg
            txt_path = str(save_dir / 'labels' / p.stem) + ('' if dataset.mode == 'image' else f'_{frame}')  # img.txt
            s += '%gx%g ' % img.shape[2:]  # print string
            gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
            imc = im0.copy() if save_crop else im0  # for save_crop
            annotator = Annotator(im0, line_width=line_thickness, pil=not ascii)
            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

                # Print results
                for c in det[:, -1].unique():
                    n = (det[:, -1] == c).sum()  # detections per class
                    s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string

                # Write results
                for *xyxy, conf, cls in reversed(det):
                    if save_txt:  # Write to file
                        xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
                        line = (cls, *xywh, conf) if save_conf else (cls, *xywh)  # label format
                        with open(txt_path + '.txt', 'a') as f:
                            f.write(('%g ' * len(line)).rstrip() % line + '\n')

                    if save_img or save_crop or view_img:  # Add bbox to image
                        c = int(cls)  # integer class
                        label = None if hide_labels else (names[c] if hide_conf else f'{names[c]} {conf:.2f}')
                        annotator.box_label(xyxy, label, color=colors(c, True))
                        if save_crop:
                            save_one_box(xyxy, imc, file=save_dir / 'crops' / names[c] / f'{p.stem}.jpg', BGR=True)

            # Print time (inference + NMS)
            
            #if(len(pred[0])>1):
             #   print(f"{pred[0][5]}Confidence: {pred[0][4]}")
                #print(f"The 2D-Array is: {det[0]} ,")
                #variables for printing

            #print(f'{s}Done. ({t2 - t1:.3f}s)')

            # Stream results
            im0 = annotator.result()
            if view_img:
                cv2.imshow(str(p), im0)
                cv2.waitKey(1)  # 1 millisecond
            #print(f"{save_path}")

            detectedImage = False;
            for i, det in enumerate(pred):
                #print(f"i:{i},det{det}")
                for *xyxy, conf, cls in reversed(det):
                    xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
                    origin_x = xywh[0]
                    origin_y = xywh[1]
                    dwidth=xywh[2]
                    dheight=xywh[3]
                    c = int(cls)
                    label = None if hide_labels else (names[c] if hide_conf else f'{names[c]} {conf:.2f}')
                    if c+1==31:# if detected bulleye send over as 31 with obstacle ID as 100
                    	sendData(f"TARGET,100,31","android")
                	else:
	                    if conf >0:

	                        print(f"{c}-{label}:confidence:{conf},width:{dwidth},height:{dheight},origin x:{origin_x}, origin y:{origin_y}")
	                        img_stats_buffer.append({"id":c,"name":label,"confidence":conf,"width":dwidth,"height":dheight,"origin_x":origin_x,"origin_y":origin_y})
	                    img_queue.append(c)
	                    img_queue_path.append(im0)
	                    if conf>0:
	                        detectedImage = True;
                #if(len(pred[0])>0):
                    #print(f"Confidence: {det[:, :4]}")
                    #print(f"{pred[3]}Confidence: {pred[4]}")

            # if dataset.mode == 'image' and detectedImage:
            #     res = cv2.imwrite(save_path+".JPG", im0)
            #     print(f"{res} result")

            #Send the last img_stats_buffer over to algo here---------------
            
            
            elements_count = {}
            if(len(img_queue)>samplingFrames):#9 successful detection before saving
                for element in img_queue:
                    if element in elements_count:
                        elements_count[element] += 1
                    else:
                        elements_count[element] = 1
                max_key = max(elements_count, key=elements_count.get)
                
                if not element in img_map:# not assigned a image yet
                    for x in range(0,len(img_queue)):
                        if(img_queue[x]==max_key):
                            img_map[max_key] = img_queue_path[x]
                            img_stats[max_key]=img_stats_buffer[x]
                            #Send max_key+1 id over to android here --------------------------
                            break
           
                while (len(img_queue)>samplingFrames):# pop the oldest one
                    img_queue_path.pop(0)
                    img_queue.pop(0)
                    img_stats_buffer.pop(0)

            #android sending id to
            length = len(img_stats)
            if length>0:
                last_id = list(img_stats.keys())[-1] 
                if lastsentid!=last_id:
                    lastsentid = last_id
                    target_ID = last_id + 1
                    #android_data["status"] = True
                    #android_data["msg"] = f"TARGET,{obstacle_num},{target_ID}"
                    #print(f"{android_data['msg']}")
                    if source =="1":
                        sendData(f"TARGET,{obstacle_num},{target_ID}","android")
                    obstacle_num=obstacle_num+1
                    #stichandshow(img_map,save_path)

           
            k = cv2.waitKey(30) & 0xFF
           
            if k==27:    # Esc key to stop
                for key in img_map:
                    if len(img_map[key])>1:
                        actualID = key +1
                        res = cv2.imwrite(f"{save_path[:-1]}{actualID}.JPG", img_map[key])
                print(img_stats)
                
                stichImg(save_path[:-1])
                os._exit(0)
            elif k==-1:  # normally -1 returned,so don't print it
                continue

            # Save results (image with detections)
            # if save_img:
            #     if dataset.mode == 'image':
            #         cv2.imwrite(save_path, im0)
            #     else:  # 'video' or 'stream'
            #         if vid_path[i] != save_path:  # new video
            #             vid_path[i] = save_path
            #             if isinstance(vid_writer[i], cv2.VideoWriter):
            #                 vid_writer[i].release()  # release previous video writer
            #             if vid_cap:  # video
            #                 fps = vid_cap.get(cv2.CAP_PROP_FPS)
            #                 w = int(vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            #                 h = int(vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            #             else:  # stream
            #                 fps, w, h = 30, im0.shape[1], im0.shape[0]
            #                 save_path += '.mp4'
            #             vid_writer[i] = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))
            #         vid_writer[i].write(im0)

    if save_txt or save_img:
        s = f"\n{len(list(save_dir.glob('labels/*.txt')))} labels saved to {save_dir / 'labels'}" if save_txt else ''
        print(f"Results saved to {colorstr('bold', save_dir)}{s}")

    if update:
        strip_optimizer(weights)  # update model (to fix SourceChangeWarning)

   
    print(f'Done. ({time.time() - t0:.3f}s)')
    
    


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', nargs='+', type=str, default='yolov5s.pt', help='model.pt path(s)')
    parser.add_argument('--source', type=str, default='data/images', help='file/dir/URL/glob, 0 for webcam')
    parser.add_argument('--imgsz', '--img', '--img-size', nargs='+', type=int, default=[640], help='inference size h,w')
    parser.add_argument('--conf-thres', type=float, default=0.25, help='confidence threshold')
    parser.add_argument('--iou-thres', type=float, default=0.45, help='NMS IoU threshold')
    parser.add_argument('--max-det', type=int, default=1000, help='maximum detections per image')
    parser.add_argument('--device', default='', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
    parser.add_argument('--view-img', action='store_true', help='show results')
    parser.add_argument('--save-txt', action='store_true', help='save results to *.txt')
    parser.add_argument('--save-conf', action='store_true', help='save confidences in --save-txt labels')
    parser.add_argument('--save-crop', action='store_true', help='save cropped prediction boxes')
    parser.add_argument('--nosave', action='store_true', help='do not save images/videos')
    parser.add_argument('--classes', nargs='+', type=int, help='filter by class: --class 0, or --class 0 2 3')
    parser.add_argument('--agnostic-nms', action='store_true', help='class-agnostic NMS')
    parser.add_argument('--augment', action='store_true', help='augmented inference')
    parser.add_argument('--visualize', action='store_true', help='visualize features')
    parser.add_argument('--update', action='store_true', help='update all models')
    parser.add_argument('--project', default='runs/detect', help='save results to project/name')
    parser.add_argument('--name', default='exp', help='save results to project/name')
    parser.add_argument('--exist-ok', action='store_true', help='existing project/name ok, do not increment')
    parser.add_argument('--line-thickness', default=3, type=int, help='bounding box thickness (pixels)')
    parser.add_argument('--hide-labels', default=False, action='store_true', help='hide labels')
    parser.add_argument('--hide-conf', default=False, action='store_true', help='hide confidences')
    parser.add_argument('--half', action='store_true', help='use FP16 half-precision inference')
    opt = parser.parse_args()
    opt.imgsz *= 2 if len(opt.imgsz) == 1 else 1  # expand
    return opt


def main(opt):

    print(colorstr('detect: ') + ', '.join(f'{k}={v}' for k, v in vars(opt).items()))
    check_requirements(exclude=('tensorboard', 'thop'))
    run(**vars(opt))


if __name__ == "__main__":
   
    opt = parse_opt()
    main(opt)

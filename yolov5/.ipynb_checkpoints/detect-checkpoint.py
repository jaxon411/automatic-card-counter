import argparse
import time
from pathlib import Path

import cv2
import torch
import torch.backends.cudnn as cudnn
import numpy as np
from numpy import random

from models.experimental import attempt_load
from utils.datasets import LoadStreams, LoadImages
from utils.datasets import LoadStreams as LoadStreams2
from utils.general import check_img_size, check_requirements, non_max_suppression, apply_classifier, scale_coords, \
    xyxy2xywh, strip_optimizer, set_logging, increment_path
from utils.plots import plot_one_box
from utils.torch_utils import select_device, load_classifier, time_synchronized

from collections import Counter
from utils.plots import plot_blackjack
from utils.blackjack import cardcounting
from utils.blackjack import blackjack

def detect(save_img=False):
    source, weights, view_img, save_txt, imgsz = opt.source, opt.weights, opt.view_img, opt.save_txt, opt.img_size
    webcam = source.isnumeric() or source.endswith('.txt') or source.lower().startswith(
        ('rtsp://', 'rtmp://', 'http://'))

    # Directories
    save_dir = Path(increment_path(Path(opt.project) / opt.name, exist_ok=opt.exist_ok))  # increment run
    (save_dir / 'labels' if save_txt else save_dir).mkdir(parents=True, exist_ok=True)  # make dir

    # Initialize
    set_logging()
    device = select_device(opt.device)
    half = device.type != 'cpu'  # half precision only supported on CUDA

    # Load model
    model = attempt_load(weights, map_location=device)  # load FP32 model
    imgsz = check_img_size(imgsz, s=model.stride.max())  # check img_size
    if half:
        model.half()  # to FP16

    #Load card counter object
    counter = cardcounting.TheCount(shoesize=2)
        
    # Second-stage classifier
    classify = False
    if classify:
        modelc = load_classifier(name='resnet101', n=2)  # initialize
        modelc.load_state_dict(torch.load('weights/resnet101.pt', map_location=device)['model']).to(device).eval()

    # Set Dataloader
    vid_path, vid_writer = None, None
    if webcam:
        view_img = True
        cudnn.benchmark = True  # set True to speed up constant image size inference
        dataset = LoadStreams2(source, img_size=imgsz)
    else:
        save_img = True
        dataset = LoadImages(source, img_size=imgsz)

    # Get names and colors
    names = model.module.names if hasattr(model, 'module') else model.names
    colors = [[random.randint(0, 255) for _ in range(3)] for _ in names]

    # Run inference
    t0 = time.time()
    
    #########
    #counting variables
    #timer for counting
    timer=time.time()
    #frames for countin
    frames = 0
    newlst = []
    countedlst = []
    p_hand={'cards':[],
           'value':0}
    d_hand={'cards':[],
           'shown_value':0, #for dealers only
           'value':0}
    moves = {0:'',1:'Stand', 2:'Hit', 3:'Double', 4:'Split', 5:'Surr'}
    #########
    
    img = torch.zeros((1, 3, imgsz, imgsz), device=device)  # init img
    _ = model(img.half() if half else img) if device.type != 'cpu' else None  # run once
    for path, img, im0s, vid_cap in dataset:
        img = torch.from_numpy(img).to(device)
        img = img.half() if half else img.float()  # uint8 to fp16/32
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        # Inference
        t1 = time_synchronized()
        pred = model(img, augment=opt.augment)[0]

        # Apply NMS
        pred = non_max_suppression(pred, opt.conf_thres, opt.iou_thres, classes=opt.classes, agnostic=opt.agnostic_nms)
        t2 = time_synchronized()

        # Apply Classifier
        if classify:
            pred = apply_classifier(pred, modelc, img, im0s)

        # Process detections
        for i, det in enumerate(pred):  # detections per image
            if webcam:  # batch_size >= 1
                p, s, im0, frame = path[i], '%g: ' % i, im0s[i].copy(), dataset.count
            else:
                p, s, im0, frame = path, '', im0s, getattr(dataset, 'frame', 0)

            #moves copy of pred to cpu to preform numpy calculations on
            cpupred = np.array(pred.copy()[0].cpu())
            cpupred_top = [row[1] for row in cpupred]
            cpupred_bottom = [row[3] for row in cpupred]
            cpupred = [row[-1] for row in cpupred] #gets predicted class numbers
            
            p = Path(p)  # to Path
            save_path = str(save_dir / p.name)  # img.jpg
            txt_path = str(save_dir / 'labels' / p.stem) + ('' if dataset.mode == 'image' else f'_{frame}')  # img.txt
            s += '%gx%g ' % img.shape[2:]  # print string
            gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

                ###########
                #card counting update logic
                if sorted(cpupred) != sorted(newlst):
                    timer = time.time() #check time if its live video
                    frames = 0 #check frames if it's video file
                    newlst=cpupred.copy()
                
                if sorted(newlst)!=sorted(countedlst):
                    if time.time()-timer>1 or frames >= 8: #if timer > 1 second or 8+ frames have passed (8 ended up feeling the best)
                        #gets the difference of the arrays including duplicates
                        cards = list((Counter(newlst) - Counter(countedlst)).elements())
                        countedlst = newlst.copy()
                        timer = time.time()
                        frames = 0 #check frames if it's video file
                        d_cards = []
                        p_cards = []
                        for i,card in enumerate(countedlst):
                            if card != 2:
                                if ((cpupred_bottom[i]-cpupred_top[i])/2)+cpupred_bottom[i] > 288: #Dealer side of table
                                    d_cards.append(names[int(card)])
                                    if len(d_cards) == 1:
                                        d_hand['shown_value'] = blackjack.GetHandValue(d_cards)
                                elif ((cpupred_bottom[i]-cpupred_top[i])/2)+cpupred_bottom[i] <= 288: #Player side of table
                                    p_cards.append(names[int(card)])
                        
                        for i,card in enumerate(cards):
                            if card != 2:
                                counter.UpdateCount(names[int(card)])
                                
#                                 if ((cpupred_bottom[i]-cpupred_top[i])/2)+cpupred_bottom[i] > 288: #Dealer side of table
#                                 if cpupred_bottom[i] > 288:   
#                                     d_hand['cards'].append(names[int(card)])

# #                                 elif ((cpupred_bottom[i]-cpupred_top[i])/2)+cpupred_bottom[i] <= 288: #Player side of table
#                                 elif cpupred_bottom[i] <= 288:
#                                     p_hand['cards'].append(names[int(card)])
                                
#                         d_hand['shown_value']=blackjack.GetHandValue(d_hand['cards'][0])
                        d_hand['cards'] = d_cards
                        p_hand['cards'] = p_cards
                        d_hand['value']=blackjack.GetHandValue(d_hand['cards'])
                        p_hand['value']=blackjack.GetHandValue(p_hand['cards'])
                ###########
                
                # Print results
                for c in det[:, -1].unique():
                    n = (det[:, -1] == c).sum()  # detections per class
                    s += f'{n} {names[int(c)]}s, '  # add to string

                # Write results
                for *xyxy, conf, cls in reversed(det):
                    if save_txt:  # Write to file
                        xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
                        line = (cls, *xywh, conf) if opt.save_conf else (cls, *xywh)  # label format
                        with open(txt_path + '.txt', 'a') as f:
                            f.write(('%g ' * len(line)).rstrip() % line + '\n')

                    if save_img or view_img:  # Add bbox to image
                        label = f'{names[int(cls)]} {conf:.2f}'
                        
                        plot_one_box(xyxy, im0, label=label, color=colors[int(cls)], line_thickness=3)
            else:
                #if there have been no detections for > second, reset countedlst
                if time.time()-timer > 1 or frames >= 8: #if timer > 1 second or 8+ frames have passed (8 ended up feeling the best)
                    countedlst = []
                    p_hand={'cards':[],
                           'value':0}
                    d_hand={'cards':[],
                           'shown_value':0, #for dealers only
                           'value':0}
                    timer = time.time()
                    frames = 0
            
            if len(p_hand['cards']) == 2 and len(d_hand['cards']) == 1:
                move = blackjack.GetInput(p_hand,d_hand,maxsplit=False,count_obj=counter,counting=True)
            else:
                move = 0
            #always plot blackjack info box
            plot_blackjack(im0,count=counter.true_count,dealer=d_hand['value'],player=p_hand['value'],move=moves[move]) 
            
            #print info for debugging
#             print("Count = "+str(counter.true_count))
#             print(pred)
    
            # Print time (inference + NMS)
            print(f'{s}Done. ({t2 - t1:.3f}s) + Inference+NMS')

            # Stream results
            if view_img:
#                 print(im0)
                cv2.imshow(str(p), im0)

            # Save results (image with detections)
            if save_img:
                if dataset.mode == 'image':
                    cv2.imwrite(save_path, im0)
                else:  # 'video'
                    if vid_path != save_path:  # new video
                        vid_path = save_path
                        if isinstance(vid_writer, cv2.VideoWriter):
                            vid_writer.release()  # release previous video writer

                        fourcc = 'mp4v'  # output video codec
                        fps = vid_cap.get(cv2.CAP_PROP_FPS)
                        w = int(vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                        h = int(vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                        vid_writer = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*fourcc), fps, (w, h))
                    if frames < 50: #caps frame count at 50 to prevent overflow
                        frames += 1
                    vid_writer.write(im0)

    if save_txt or save_img:
        s = f"\n{len(list(save_dir.glob('labels/*.txt')))} labels saved to {save_dir / 'labels'}" if save_txt else ''
        print(f"Results saved to {save_dir}{s}")

    print(f'Done. ({time.time() - t0:.3f}s) OTHER')

    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', nargs='+', type=str, default='yolov5s.pt', help='model.pt path(s)')
    parser.add_argument('--source', type=str, default='data/images', help='source')  # file/folder, 0 for webcam
    parser.add_argument('--img-size', type=int, default=640, help='inference size (pixels)')
    parser.add_argument('--conf-thres', type=float, default=0.25, help='object confidence threshold')
    parser.add_argument('--iou-thres', type=float, default=0.45, help='IOU threshold for NMS')
    parser.add_argument('--device', default='', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
    parser.add_argument('--view-img', action='store_true', help='display results')
    parser.add_argument('--save-txt', action='store_true', help='save results to *.txt')
    parser.add_argument('--save-conf', action='store_true', help='save confidences in --save-txt labels')
    parser.add_argument('--classes', nargs='+', type=int, help='filter by class: --class 0, or --class 0 2 3')
    parser.add_argument('--agnostic-nms', action='store_true', help='class-agnostic NMS')
    parser.add_argument('--augment', action='store_true', help='augmented inference')
    parser.add_argument('--update', action='store_true', help='update all models')
    parser.add_argument('--project', default='runs/detect', help='save results to project/name')
    parser.add_argument('--name', default='exp', help='save results to project/name')
    parser.add_argument('--exist-ok', action='store_true', help='existing project/name ok, do not increment')
    opt = parser.parse_args()
    print(opt)
    check_requirements()

    with torch.no_grad():
        if opt.update:  # update all models (to fix SourceChangeWarning)
            for opt.weights in ['yolov5s.pt', 'yolov5m.pt', 'yolov5l.pt', 'yolov5x.pt']:
                detect()
                strip_optimizer(opt.weights)
        else:
            detect()

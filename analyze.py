import cv2
import datetime
import os
import numpy as np
import json

def video2Matrix(script_path, videofile, assetsfolder, dumpsfolder):
    print('video2Matrix', script_path, videofile, assetsfolder, dumpsfolder)

    vfname = '{}/{}/{}'.format(script_path,assetsfolder,videofile)
    tfname = '{}/{}/{}'.format(script_path,dumpsfolder,videofile+'.txt')

    cap = cv2.VideoCapture(vfname)
    frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    seconds = round(frames / fps)
    video_time = datetime.timedelta(seconds=seconds)
    print(f'duration in seconds: {seconds}')
    print(f'video time: {video_time}')

    f = open(tfname, 'w')

    counter = 0
    # frames = np.empty((1080, 1920, 3), np.uint8)
    frames = []

    while cap.isOpened():
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print('Can\'t receive frame (stream end?). Exiting ...')
            break
        # rows,cols,_ = frame.shape
        # f.write(str(frame))
        # f.write('####################### Frame #'+ str(counter) + '\n'+str(frame)+'\n')

        frames.append(frame)
        counter+=1
    print("ALL FRAMES", str(len(frames)), frames[0].shape)

    f.write(str(frames))
    f.close()

    cap.release()

script_path = os.path.dirname(os.path.abspath(__file__))

for f in os.listdir(script_path+'/assets'):
    if f.endswith('.mp4'):
        video2Matrix(script_path, f, '/assets', '/dumps')

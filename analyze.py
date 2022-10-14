import cv2
import datetime
import os
import numpy as np
import json

def get_square_image(frame):
    rows,cols,_ = frame.shape
    if (rows<cols):
        diff = cols-rows
        margin = int((diff)/2//1)
        return frame[:,margin:cols-margin]
    elif (cols<rows):
        diff = rows-cols
        margin = int((diff)/2//1)
        return frame[margin:rows-margin,:]
    else:
        return frame


def frame_to_fixed_shape(frame, targetRows, targetCols, tfname):
    frame = get_square_image(frame)
    rows,cols,_ = frame.shape

    rowFactor = int(rows/targetRows//1)
    colFactor = int(cols/targetCols//1)
    # TODO: interpolation
    if rowFactor<=0 or colFactor<=0:
        raise RuntimeError("assuming rowFactor and colFactor > 0. todo: interpolation.")
    
    fixedrowsframe = frame[::rowFactor]
    resizedFrame = np.empty((targetRows, targetCols, 3), np.uint8)

    for row in fixedrowsframe:
        # get every colFactor'th col from row and clip to a maximum number of targetCols
        fixedcolsrow = row[::colFactor][:targetCols]
        np.append(resizedFrame, fixedcolsrow)

    return resizedFrame    


def video_2_matrix(script_path, videofile, assetsfolder, dumpsfolder):
    print('video2Matrix', script_path, videofile, assetsfolder, dumpsfolder)

    vfname = '{}/{}/{}'.format(script_path,assetsfolder,videofile)
    tfname = '{}/{}/{}'.format(script_path,dumpsfolder,videofile+'.txt')

    cap = cv2.VideoCapture(vfname)
    framecount = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    seconds = round(framecount / fps)
    video_time = datetime.timedelta(seconds=seconds)
    print(f'framecount: {framecount}')
    print(f'duration in seconds: {seconds}')
    print(f'video time: {video_time}')

    # f = open(tfname, 'w')
    targetRows = 100
    targetCols = 100

    counter = 0
    frames = np.empty((int(framecount), targetRows, targetCols, 3), np.uint8)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print('Stream finished ...')
            break

        resizedFrame = frame_to_fixed_shape(frame, 100, 100, tfname)
        np.append(frames, resizedFrame)
        counter+=1
    print('all frames: {} | shape: {}'.format(str(len(frames)), frames[0].shape))

    # f.write(str(frames))
    # f.close()

    cap.release()

script_path = os.path.dirname(os.path.abspath(__file__))

for f in os.listdir(script_path+'/assets'):
    if f.endswith('.mp4'):
        video_2_matrix(script_path, f, '/assets', '/dumps')

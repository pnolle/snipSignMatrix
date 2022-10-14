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
    
    print (targetRows, targetCols, rows, cols, rowFactor, colFactor)

    sframe = frame[::rowFactor]
    print("frame", len(frame), len(sframe), rowFactor)

    # only for display
    row0 = frame[0]
    srow0 = row0[::colFactor]
    print("row0", len(row0), len(srow0), colFactor)

    resizedFrame = np.empty((targetRows, targetCols, 3), np.uint8)

    for row in sframe:
        # get every colFactor'th col from row and clip to a maximum number of targetCols
        srow = row[::colFactor][:targetCols]
        # print ("SROW", srow, len(srow))
        np.append(resizedFrame, srow)

    rows,cols,_ = resizedFrame.shape
    print("resizedFrame", rows,cols,_)
    

def video_2_matrix(script_path, videofile, assetsfolder, dumpsfolder):
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

    # f = open(tfname, 'w')

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

        if counter==0:
            frame_to_fixed_shape(frame, 100, 100, tfname)

        frames.append(frame)
        counter+=1
    print("ALL FRAMES", str(len(frames)), frames[0].shape)

    # f.write(str(frames))
    # f.close()

    cap.release()

script_path = os.path.dirname(os.path.abspath(__file__))

for f in os.listdir(script_path+'/assets'):
    if f.endswith('.mp4'):
        video_2_matrix(script_path, f, '/assets', '/dumps')

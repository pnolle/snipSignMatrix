import cv2
import datetime
import os
import json
from json import JSONEncoder
import numpy
import base64
import zlib

# ### SETTINGS ###
snipsignsize = [300, 300]


# ### HELPERS ###
class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)


def get_square_image(frame):
    rows, cols, _ = frame.shape
    if (rows < cols):
        diff = cols-rows
        margin = int((diff)/2//1)
        return frame[:, margin:cols-margin]
    elif (cols < rows):
        diff = rows-cols
        margin = int((diff)/2//1)
        return frame[margin:rows-margin, :]
    else:
        return frame


def frame_to_fixed_shape(frame, targetRows, targetCols):
    frame = get_square_image(frame)
    rows, cols, _ = frame.shape

    rowFactor = int(rows/targetRows//1)
    colFactor = int(cols/targetCols//1)
    # TODO: interpolation
    if rowFactor <= 0 or colFactor <= 0:
        raise RuntimeError(
            "assuming rowFactor and colFactor > 0. todo: interpolation.")

    fixedrowsframe = frame[::rowFactor]
    resizedFrame = numpy.empty((targetRows, targetCols, 3), numpy.uint8)

    for row in fixedrowsframe:
        # get every colFactor'th col from row and clip to a maximum number of targetCols
        fixedcolsrow = row[::colFactor][:targetCols]
        numpy.append(resizedFrame, fixedcolsrow)

    return resizedFrame


def video_2_matrix(script_path, videofile, assetsfolder, targetRows, targetCols):
    vfname = '{}/{}/{}'.format(script_path, assetsfolder, videofile)

    cap = cv2.VideoCapture(vfname)
    framecount = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = cap.get(cv2.CAP_PROP_FPS)

    seconds = round(framecount / fps)
    video_time = datetime.timedelta(seconds=seconds)
    print(f'framecount: {framecount}')
    print(f'duration in seconds: {seconds}')
    print(f'video time: {video_time}')

    frames = numpy.empty(
        (int(framecount), targetRows, targetCols, 3), numpy.uint8)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print('Stream finished ...')
            break

        resizedFrame = frame_to_fixed_shape(frame, targetRows, targetCols)
        numpy.append(frames, resizedFrame)

    print('all frames: {} | shape: {}'.format(
        str(len(frames)), frames[0].shape))

    cap.release()
    return frames


def storeData(numpyData, videofile, dumpsfolder):
    encodedNumpyData = json.dumps(numpyData, cls=NumpyArrayEncoder).replace(
        " ", "")  # use dump() to write array into file
    print('json len', len(numpyData), len(encodedNumpyData))

    bNumpyData = bytes(encodedNumpyData, 'utf-8')
    b64NumpyData = base64.b64encode(bNumpyData)
    zlibNumpyData = zlib.compress(b64NumpyData)
    print('zlib len', len(zlibNumpyData))

    dumpfilename = '{}/{}/{}'.format(script_path, dumpsfolder, videofile+'.b64.zlib')
    file1 = open(dumpfilename, 'wb')
    file1.write(zlibNumpyData)
    file1.close()


script_path = os.path.dirname(os.path.abspath(__file__))

for f in os.listdir(script_path+'/assets'):
    if f.endswith('.mp4'):
        numpyData = video_2_matrix(script_path, f, '/assets', snipsignsize[0], snipsignsize[1])
        storeData(numpyData, f, '/dumps')

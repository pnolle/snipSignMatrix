import cv2
import datetime
import os
import json
from json import JSONEncoder
import numpy
import base64
import zlib
import sys

# ### SETTINGS ###
snipsignsize = [300, 300]
debugRun = False


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


def rgbValuesToOneInt(fixedcolsrow):
    outputrow = numpy.empty((len(fixedcolsrow), 1), numpy.uint8)
    for pixel in fixedcolsrow:
        r = pixel[0] << 16
        g = pixel[1] << 8
        b = pixel[2]
        rgb = r+g+b
        numpy.append(outputrow, rgb)
    return outputrow


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
    
    # residedFrame filled with combined int value instead of separate r/g/b values - thus we have a depth of 1 for each column
    resizedFrame = numpy.empty((targetRows, targetCols, 1), numpy.uint8)

    for row in fixedrowsframe:
        # get every colFactor'th col from row and clip to a maximum number of targetCols
        fixedcolsrow = row[::colFactor][:targetCols]
        row = rgbValuesToOneInt(fixedcolsrow)
        numpy.append(resizedFrame, row)

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

    limit = 3

    # frames filled with combined int value instead of separate r/g/b values - thus we have a depth of 1 for each column
    frames = numpy.empty((limit, targetRows, targetCols, 1), numpy.uint8)

    framecounter = 0

    # while cap.isOpened():
    while framecounter < limit:
        print(framecounter)
        ret, frame = cap.read()
        if not ret:
            print('Stream finished ...')
            break

        resizedFrame = frame_to_fixed_shape(frame, targetRows, targetCols)
        numpy.append(frames, frame)
        framecounter = framecounter+1

    print('all frames: {} | shape: {}'.format(
        str(len(frames)), frames[0].shape))

    cap.release()
    return frames


def storeData(numpyData, videofile, dumpsfolder):
    encodedNumpyData = json.dumps(numpyData, cls=NumpyArrayEncoder).replace(
        " ", "")  # use dump() to write array into file
    print('json len', len(numpyData), len(encodedNumpyData))

    jsonFileName = '{}/{}/{}'.format(script_path,
                                     dumpsfolder, videofile+'.json')
    jsonFile = open(jsonFileName, 'w')
    jsonFile.write(encodedNumpyData)
    jsonFile.close()

    bNumpyData = bytes(encodedNumpyData, 'utf-8')
    b64NumpyData = base64.b64encode(bNumpyData)
    zlibNumpyData = zlib.compress(b64NumpyData)
    print('zlib len', len(zlibNumpyData))

    binaryFileName = '{}/{}/{}'.format(script_path,
                                       dumpsfolder, videofile+'.b64.zlib')
    binaryFile = open(binaryFileName, 'wb')
    binaryFile.write(zlibNumpyData)
    binaryFile.close()


script_path = os.path.dirname(os.path.abspath(__file__))

for f in os.listdir(script_path+'/assets'):
    if f.endswith('.mp4'):
        print('\nHandling video file \'%s\'.' % (f))
        numpyData = video_2_matrix(
            script_path, f, '/assets', snipsignsize[0], snipsignsize[1])
        storeData(numpyData, f, '/dumps')
    if debugRun == True:
        sys.exit('Aborting debug run.')

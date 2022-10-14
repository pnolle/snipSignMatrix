import cv2
import datetime
import os

def video2Matrix(script_path, videofile, assetsfolder, dumpsfolder):
    print('video2Matrix', script_path, videofile, assetsfolder, dumpsfolder)

    cap = cv2.VideoCapture('{}/{}/{}'.format(script_path,assetsfolder,videofile))
    frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    seconds = round(frames / fps)
    video_time = datetime.timedelta(seconds=seconds)
    print(f'duration in seconds: {seconds}')
    print(f'video time: {video_time}')

    f = open(script_path+'/dumps/' + videofile + '.txt', 'w')

    counter = 0
    while cap.isOpened():
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print('Can\'t receive frame (stream end?). Exiting ...')
            break
        rows,cols,_ = frame.shape
        print (counter, range(rows))
        f.write('####################### Frame #'+ str(counter) + '\n'+str(frame)+'\n')
        counter+=1

    f.close()
    cap.release()

script_path = os.path.dirname(os.path.abspath(__file__))

for f in os.listdir(script_path+'/assets'):
    if f.endswith('.mp4'):
        print(f)
        print(script_path)
        video2Matrix(script_path, f, '/assets', '/dumps')

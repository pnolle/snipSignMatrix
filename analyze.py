import cv2
import datetime
import os

# img = cv2.imread('2.png',1)
# rows,cols,_ = img.shape

# for i in range(rows):
#     for j in range(cols):
#         k = img[i,j]
#         print(k)


def video2Matrix(script_path, videofile, assetsfolder, dumpsfolder):
    print('video2Matrix', script_path, videofile, assetsfolder, dumpsfolder)

    # cap = cv2.VideoCapture('VerticalLineLoop.mp4')
    cap = cv2.VideoCapture('{}/{}/{}'.format(script_path,assetsfolder,videofile))
    # count the number of frames
    frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    # calculate duration of the video
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
    #     for i in range(rows):
    #         k = frame[i]
    #         print(i, k[0])
            # for j in range(cols):
            #     k = frame[i,j]
            #     print(k)
        # gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        # cv.imshow('frame', gray)
        # if cv.waitKey(1) == ord('q'):
        #     break
            
    #     # Press Q on keyboard to exit
    #         if cv2.waitKey(25) & 0xFF == ord('q'):
    #                 break

    f.close()
    cap.release()

script_path = os.path.dirname(os.path.abspath(__file__))

for f in os.listdir(script_path+'/assets'):
    if f.endswith('.mp4'):
        print(f)
        print(script_path)
        video2Matrix(script_path, f, '/assets', '/dumps')


# for file in os.listdir(os.path.join("/assets")):
#     print(file)
#     if file.endswith(".mp4"):
#         video2Matrix(os.path.join("/assets")+file)
#         # video2Matrix('mixkit-retro-80s-vhs-style-triangles-spin-over-neon-palm-tree-5391-medium.mp4')
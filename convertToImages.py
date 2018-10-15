#!/usr/bin/env python3
import cv2
import signal
import sys
import os

stopFlag = True
def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    stopFlag = False
    cap.release()
    out.release()
    sys.exit(0)

if __name__ == "__main__":

    if not sys.argv[1]:
        print("First Argument must be the input video filepath")
    else:
        inputVideofile = sys.argv[1]
    if not sys.argv[2]:
        print("Second Argument must be the output frame filepath")
    else:
        outputImageFolderName = sys.argv[2]
        # Create a folder if one does not exist
        if( not os.path.isdir('trainingImages/' + outputImageFolderName)):
            os.makedirs('trainingImages/' + outputImageFolderName)



    framerate = 25.0
    cap = cv2.VideoCapture('filesrc location=' + inputVideofile + ' ! decodebin ! videoconvert ! video/x-raw,width=720,height=480 ! appsink')
    out = cv2.VideoWriter('appsrc ! video/x-raw,format=BGR ! videoconvert !  autovideosink ', cv2.VideoWriter_fourcc('J','P','E','G'), framerate, (720, 480))


    if(not cap.isOpened()):
      print("VideoCapture not opened!")
    elif(not out.isOpened()):
      print("VideoWriter not opened!")



    i = 0
    while (cap.isOpened() and stopFlag):
        ret, frame = cap.read()
        if ret:

            out.write(frame)

            cv2.imwrite('trainingImages/' + outputImageFolderName + '/rawImage' + str('%05d' % i) + '.jpg' , frame, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
            # cv2.imwrite("RawUnlabelledImages/rawImage" + str(i) + ".png" , frame, [int(cv2.IMWRITE_JPEG_QUALITY), 100])

            i += 1
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    # Release everything if job is finished
    cap.release()
    out.release()

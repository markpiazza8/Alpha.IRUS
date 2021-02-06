import numpy as np
import cv2
import GUI_Jan30Rev


def camera(turn_off):
    cap = cv2.VideoCapture(1)

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Display the resulting frame
        x = cv2.imshow('frame',gray)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        #turn_off = gui_main_rev02.Main.getOnorOff()
        if turn_off:
            break
        
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


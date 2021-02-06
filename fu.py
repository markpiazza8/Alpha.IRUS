#from pymba import Vimba, VimbaException
#from pymba_examples.camera._display_frame import display_frame

'''
if __name__ == '__main__':

    with Vimba() as vimba:
        camera = vimba.camera(0)
        camera.open()

        camera.arm('SingleFrame')

        # capture a single frame, more than once if desired
        for i in range(1):
            try:
                frame = camera.acquire_frame()
                display_frame(frame, 0)
            except VimbaException as e:
                # rearm camera upon frame timeout
                if e.error_code == VimbaException.ERR_TIMEOUT:
                    print(e)
                    camera.disarm()
                    camera.arm('SingleFrame')
                else:
                    raise

        camera.disarm()

        camera.close()
'''




from time import sleep
from pymba import Vimba
from pymba_master.examples.camera._display_frame import display_frame

if __name__ == '__main__':

    with Vimba() as vimba:
        camera = vimba.camera(0)
        camera.open()

        # arm the camera and provide a function to be called upon frame ready
        camera.arm('Continuous', display_frame)
        camera.start_frame_acquisition()

        # stream images for a while...
        sleep(25)

        # stop frame acquisition
        # start_frame_acquisition can simply be called again if the camera is still armed
        camera.stop_frame_acquisition()
        camera.disarm()

        camera.close()

# Get our data for street signs
# Run with sudo python3 Train_Street_Signs.py

import io
import time
import picamera

# import the GoPiGo3 drivers
import easygopigo3 as easy

# Create an instance of the GoPiGo3 class.
# GPG will be the GoPiGo3 object.
gpg = easy.EasyGoPiGo3()

# Put a grove button in port AD1
my_button = gpg.init_button_sensor("AD1")

RELEASED = 0
PRESSED = 1
state = RELEASED

# Picamera Code From https://picamera.readthedocs.io/en/release-1.13/recipes2.html#rapid-capture-and-processing
# Slightly modified so we can take low resolution "bursts" of camera readings to gather data.
# Button tutorial from here:  http://gopigo3.readthedocs.io/en/master/tutorials-basic/button.html
# Starts when  you press the button.

class SplitFrames(object):
    def __init__(self):
        self.frame_num = 0
        self.output = None

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # Start of new frame; close the old one (if any) and
            # open a new output
            if self.output:
                self.output.close()
            self.frame_num += 1
            self.output = io.open('image%02d.jpg' % self.frame_num, 'wb')
        self.output.write(buf)

def drive_and_capture():
    with picamera.PiCamera(resolution='720p', framerate=30) as camera:
        camera.resolution = (300, 255)
        camera.start_preview()
        # Give the camera some warm-up time
        time.sleep(2)
        output = SplitFrames()

        while True:
            if state == RELEASED and my_button.read() == 1:
                gpg.forward()
                start = time.time()
                camera.start_recording(output, format='mjpeg')
                camera.wait_recording(1)
                camera.stop_recording()
                finish = time.time()
                gpg.stop()

drive_and_capture()

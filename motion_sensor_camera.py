import RPi.GPIO as GPIO
import picamera as PiCamera
import time
import argparse
import datetime

PROJECT_PATH = "/home/pi/Projekte/motion_sensor_camera/"
PHOTO_PATH   = PROJECT_PATH + "photos/"
VIDEO_PATH   = PROJECT_PATH + "videos/"

PIR_PIN_ONE = 23
PIR_PIN_TWO = 24

parser = argparse.ArgumentParser()
parser.add_argument("--mode", default="photo", type=str, help="Provide the operating mode (photo/video)")

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN_ONE, GPIO.IN)
GPIO.setup(PIR_PIN_TWO, GPIO.IN)

camera = PiCamera.PiCamera()
#camera.rotation = 180 # Uncomment when the taken photo/video is upside down 

def getCurrentDateTime():
    now = datetime.datetime.now()
    return now.strftime("%d.%m.%y-%X")

def takePhoto(): # When callback add channel to arguments
    camera.start_preview()
    time.sleep(2)
    camera.capture(PHOTO_PATH + getCurrentDateTime() + ".jpg")
    camera.stop_preview()
    print("Photo taken!")

def makeVideo(): # When callback add channel to arguments
    camera.start_preview()
    camera.start_recording(VIDEO_PATH + getCurrentDateTime() + ".h264")
    time.sleep(10)
    camera.stop_recording()
    camera.stop_preview()
    print("Video made!")

def observe(mode):
    if not (mode == "video" or mode == "photo"):
        print(mode + " not recognized. Falling back to photo mode.")
        mode = "photo"

    print("Operating in " + mode + " mode.")
    while True:
        if GPIO.input(PIR_PIN_ONE) == GPIO.HIGH and GPIO.input(PIR_PIN_TWO) == GPIO.HIGH:
            if mode == "video":
                makeVideo()
            else:
                takePhoto()
            time.sleep(5)

def main():
    args = parser.parse_args()
    
    try:
        observe(args.mode)
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("Existed.")

if __name__ == "__main__":
    main()

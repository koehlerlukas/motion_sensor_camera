import RPi.GPIO as GPIO
import picamera as PiCamera
import time
import argparse
import datetime
from pathlib import Path

PROJECT_PATH = "/home/pi/Projekte/motion_sensor_camera/" # Change to your project path
PHOTO_PATH   = PROJECT_PATH + "photos/"
VIDEO_PATH   = PROJECT_PATH + "videos/"

Path(PHOTO_PATH).mkdir(parents=True, exist_ok=True)
Path(VIDEO_PATH).mkdir(parents=True, exist_ok=True)

PIR_PIN_ONE = 23 # Change to the pin you use
PIR_PIN_TWO = 24 # Change to the pin you use

parser = argparse.ArgumentParser()
parser.add_argument("--mode", default="photo", type=str, help="Provide the operating mode (photo/video)")

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN_ONE, GPIO.IN)
GPIO.setup(PIR_PIN_TWO, GPIO.IN)

camera = PiCamera.PiCamera()
#camera.rotation = 180 # Uncomment when the taken photo/video is upside down 

def getCurrentDateTime():
    return datetime.datetime.now().strftime("%d.%m.%y-%X")

def takePhoto():
    camera.start_preview()
    time.sleep(2)
    camera.capture(PHOTO_PATH + getCurrentDateTime() + ".jpg")
    camera.stop_preview()
    print("Photo taken!")

def makeVideo():
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
        print("Exited.")

if __name__ == "__main__":
    main()

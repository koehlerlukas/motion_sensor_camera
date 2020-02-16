import RPi.GPIO as GPIO
import picamera as PiCamera
import time
import argparse
import datetime

# Format of shots.txt:
#
# x -> Number of photos taken
# y -> Number of videos made

PROJECT_PATH = "/home/pi/Projekte/motion_sensor_camera/" # Change to your project path
PHOTO_PATH   = PROJECT_PATH + "photos/" # May need to be created 
VIDEO_PATH   = PROJECT_PATH + "videos/" # May need to be created

PIR_PIN_ONE = 23 # Change to the pin you use
PIR_PIN_TWO = 24 # Change to the pin you use

parser = argparse.ArgumentParser()
parser.add_argument("--mode", default="photo", type=str, help="Provide the operating mode (photo/video)")

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN_ONE, GPIO.IN)
GPIO.setup(PIR_PIN_TWO, GPIO.IN)

camera = PiCamera.PiCamera()
#camera.rotation = 180 # Uncomment when the taken photo/video is upside down 

<<<<<<< HEAD
def getCurrentDateTime():
    return datetime.datetime.now().strftime("%d.%m.%y-%X")
=======
def readNumbers():
    with open("shots.txt", "r") as file:
        return [int(x) for x in file.readlines()]

def readNumber(photo):
    if photo:
        return readNumbers()[0]
    else:
        return readNumbers()[1]

def updateNumber(photo):
    numbers = readNumbers()
    with open("shots.txt", "w+") as file:
        if photo:
            file.write(str(numbers[0] + 1) + "\n")
            file.write(str(numbers[1]))
        else:
            file.write(str(numbers[0]) + "\n")
            file.write(str(numbers[1] + 1))

def readAndUpdateNumber(photo=True):
    number = readNumber(photo)
    updateNumber(photo)
    return number
>>>>>>> 232cabf4f1dcd7e5d1a5957747d07813f64e9bce

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
        print("Existed.")

if __name__ == "__main__":
    main()

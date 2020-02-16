import RPi.GPIO as GPIO
import picamera as PiCamera
import time
import argparse

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

# Format of shots.txt:
#
# x -> Number of photos taken
# y -> Number of videos made

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

def takePhoto(): # When callback add channel to arguments
    camera.start_preview()
    photo = readAndUpdateNumber()
    time.sleep(2)
    camera.capture(PHOTO_PATH + "photo" + str(photo) + ".jpg")
    camera.stop_preview()
    print("Photo #" + str(photo) + " taken!")

def makeVideo(): # When callback add channel to arguments
    camera.start_preview()
    video = readAndUpdateNumber(photo=False)
    camera.start_recording(VIDEO_PATH + "video" + str(video) + ".h264")
    time.sleep(10)
    camera.stop_recording()
    camera.stop_preview()
    print("Video #" + str(video) + " made!")

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

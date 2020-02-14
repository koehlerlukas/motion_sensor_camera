import RPi.GPIO as GPIO
import picamera as PiCamera
import time

PROJECT_PATH = "/home/pi/motion_sensor_camera/"
PHOTO_PATH   = PROJECT_PATH + "photos/"
VIDEO_PATH   = PROJECT_PATH + "videos/"

PIR_PIN_ONE = 23
PIR_PIN_TWO = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN_ONE, GPIO.IN)
GPIO.setup(PIR_PIN_TWO, GPIO.IN)

camera = PiCamera()
camera.rotation = 180

# Format of shots.txt:
# 
# x -> Number of photos taken
# y -> Number of videos made

def readNumbers():
    with open("shots.txt", "r") as file:
        return [int(x) for x in file.readlines()]

def readNmbr(photo):
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
    number = readNmbr(photo)
    updateNumber(photo)
    return number

def takePhoto(): # When callback add channel to arguments
    camera.start_preview()
    photo = readAndUpdateNumber()
    time.sleep(2)
    camera.capture(PHOTO_PATH + "photo_" + photo)
    camera.stop_preview()

def makeVideo(): # When callback add channel to arguments
    camera.start_preview()
    video = readAndUpdateNumber(photo=False)
    camera.start_recording(VIDEO_PATH + "video_" + video)
    time.sleep(10)
    camera.stop_recording()
    camera.stop_preview()

def observe():
    while True:
        first_pir  = GPIO.input(PIR_PIN_ONE)
        second_pir = GPIO.input(PIR_PIN_TWO)
        
        if first_pir and second_pir:
            takePhoto()
            time.sleep(5)

def main():
    observe()
    GPIO.cleanup()

if __name__ == "__main__":
    main()
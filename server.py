# Importing Library's
import RPi.GPIO as GPIO
import time
import cv2
import sys


from flask import Flask, render_template, Response
from flask_apscheduler import APScheduler

    
# GPIO Pin Setup
LeftBumper = 26
LeftFrontBumper = 19
RightBumper = 13
RightFrontBumper = 6


# Set raspberry GPIO pins to BCM mode
GPIO.setmode(GPIO.BCM)

# Setup GPIO pins
GPIO.setup(LeftBumper, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LeftFrontBumper, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(RightBumper, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(RightFrontBumper, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Set Global var
LeftMotorSpeed = 0
RightMotorSpeed = 0
BrushMotorSpeed = 0

# create flask and APSceduler object and
# point scheduler to the flask object
app = Flask(__name__)
scheduler = APScheduler()
scheduler.init_app(app)


# creating route to the index page
@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


# A function to generate the frames from the camera and make them a video
def gen():
    # get camera
    cap = cv2.VideoCapture(0)

    # horizontal/vertical resolution cap for a raspberry pi I suggest
    # 480p over 720p because the raspberry pi 3 b+ (The one I'm using)
    # doesn't have enough compute power to render frames at a steady
    # frame rate
    cap.set(3, 640) # vertical cap
    cap.set(4, 480) # horizontal cap

    # Read until frame is completed
    while (cap.isOpened()):

        # Capture frame-by-frame
        ret, img = cap.read()

        # this is where if you want to draw on frames you add that here
        if ret == True:
            img = cv2.resize(img, (0, 0), fx=1, fy=1)
        
            # detect if bumper is compressed then write which (if any) bumpers are compressed on the frames
            # Side Note: These buttons must be setup with the 3rd arg [pull_up_down=GPIO.PUD_UP] I've tried 
            # [GPIO.PUD_DOWN] but it doesn't work for some reason so 1 = decompressed 0 = compressed
            if (GPIO.input(LeftBumper) != 1):
                cv2.putText(img=img, text='Left!', org=(1, 465), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1,
                        color=(0, 0, 255), thickness=3)

            if (GPIO.input(RightBumper) != 1):
                cv2.putText(img=img, text='Right!', org=(550, 465), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1,
                        color=(0, 0, 255), thickness=3)

            if (GPIO.input(LeftFrontBumper) != 1):
                cv2.putText(img=img, text='Front Left!', org=(125, 465), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1,
                            color=(0, 0, 255), thickness=3)

            if (GPIO.input(RightFrontBumper) != 1):
                cv2.putText(img=img, text='Front Right!', org=(320, 465), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1,
                            color=(0, 0, 255), thickness=3)
                
            if (debug):
                cv2.putText(img=img, text='Debug Mode: ON', org=(1, 465), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1,
                            color=(0, 0, 255), thickness=3)

            # convert the frame to bianry and sends it 
            frame = cv2.imencode('.jpg', img)[1].tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        else:
            break


# responds with the generated frames
@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


# a function that is scheduled to run after a set
# amount of time You have to becarefull what you 
# put in here as it can completely screw the video
# feed everytime this runs the video stops untill 
# its finished
def scheduled_task():
    pass


if(__name__ == "__main__")
    # add a function to the scheduled task list
    # and start the scheduler
    scheduler.add_job(func=scheduled_task, trigger="interval", seconds=5, id="Gae")
    scheduler.start()

    # start the flask app object
    app.run(host="0.0.0.0", port=80)

# Importing Library's
import RPi.GPIO as GPIO
import time
import cv2


from flask import Flask, render_template, Response
from flask_apscheduler import APScheduler

# GPIO Pin int
LeftButtonPin = 17

# Global vars to control text prompts
LeftButton = 0

# Set raspberry GPIO pins to BCM mode
GPIO.setmode(GPIO.BCM)

# Setup GPIO pins
GPIO.setup(LeftButtonPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# create flask and APSceduler object
app = Flask(__name__)
scheduler = APScheduler()

# point scheduler to the flask object
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
    cap.set(3, 640)
    cap.set(4, 480)

    # Read until video is completed
    while (cap.isOpened()):

        # Capture frame-by-frame
        ret, img = cap.read()

        # this is where if you want to draw on frames you add that here
        if ret == True:
            img = cv2.resize(img, (0, 0), fx=1, fy=1)

            if (LeftButton != 0):
                cv2.putText(img=img, text='Left!', org=(1, 465), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1,
                        color=(0, 0, 255), thickness=3)

            cv2.putText(img=img, text='Right!', org=(550, 465), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1,
                        color=(0, 0, 255), thickness=3)
            cv2.putText(img=img, text='Front Left!', org=(125, 465), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1,
                        color=(0, 0, 255), thickness=3)
            cv2.putText(img=img, text='Front Right!', org=(320, 465), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1,
                        color=(0, 0, 255), thickness=3)
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


# a function that is scheduled to run
def scheduled_task():
    # Check Collision Button
    GPIO.input(LeftButtonPin)
    LeftButton = GPIO.input(LeftButtonPin)


# add a function to the scheduled task list
# and start the scheduler
scheduler.add_job(func=scheduled_task, trigger="interval", seconds=.50, id="TEST")
scheduler.start()


# start the app object
app.run(host="0.0.0.0", port=80)


#!/usr/bin/env python
import threading
import time

from flask import Flask, render_template, Response
from flask_basicauth import BasicAuth
from camera import VideoCamera
from mail import send_email

app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = 'student'
app.config['BASIC_AUTH_PASSWORD'] = 'student'
app.config['BASIC_AUTH_FORCE'] = True
basic_auth = BasicAuth(app)

email_update_interval = 600
video_camera = VideoCamera()
last_epoch = 0


def check_for_objects():
    global last_epoch
    while True:
        try:
            frame, found_obj = video_camera.get_object()
            if found_obj and (time.time() - last_epoch) > email_update_interval:
                last_epoch = time.time()
                print("Sending email...")
                send_email(frame)
                print("done!")
        except Exception as e:
            print("Error sending email: ", str(e))


@app.route('/')
@basic_auth.required
def index():
    return render_template('index.html')


def gen(camera):
    while True:
        frame = camera.get_image(filters=['background_subtractor_mog2'])
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(video_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    # t = threading.Thread(target=check_for_objects, args=())
    # t.daemon = True
    # t.start()
    app.run(host='0.0.0.0', debug=True)

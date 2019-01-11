#!/usr/bin/env python
from threading import Thread
import time

from flask import Flask, render_template, Response, request, redirect
from flask_basicauth import BasicAuth
from camera import VideoCamera
from mail import *

app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = 'student'
app.config['BASIC_AUTH_PASSWORD'] = 'student'
app.config['BASIC_AUTH_FORCE'] = True
basic_auth = BasicAuth(app)

email_update_interval = 600
video_camera = VideoCamera()
last_epoch = 0
selected_filter = None


class Mailing(Thread):

    def __init__(self):
        super().__init__()
        self.daemon = True
        self.running = False

    def stop(self):
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            self.check_for_objects()

    @staticmethod
    def check_for_objects():
        global last_epoch
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
    return render_template('index.html', Filters=video_camera.functions.keys())


@app.route('/mail/settings')
def mail_settings():
    return render_template('mailForm.html')


@app.route('/mail/settings/credentials', methods=['POST'])
def set_mail_credentials():
    global fromEmail
    global fromEmailPassword
    global toEmail
    fromEmail = request.form['fromEmail']
    fromEmailPassword = request.form['fromEmail']
    toEmail = request.form['fromEmail']
    return redirect('/')


@app.route('/camera.html')
def index_camera():
    global selected_filter
    selected_filter = request.args.get("choice")
    return render_template('camera.html')


def gen(camera):
    while True:
        frame = camera.get_image(filter=selected_filter)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(video_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    # mailing = Mailing()
    # mailing.start()
    app.run(host='0.0.0.0', debug=False)

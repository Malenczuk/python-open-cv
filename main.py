#!/usr/bin/env python
from flask import Flask, render_template, Response, request, redirect
from flask_basicauth import BasicAuth
from camera import VideoCamera
from security import Security


app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = 'student'
app.config['BASIC_AUTH_PASSWORD'] = 'student'
app.config['BASIC_AUTH_FORCE'] = True
basic_auth = BasicAuth(app)


video_camera = VideoCamera()
selected_filter = None


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
    security = Security(video_camera, 'haarcascades/haarcascade_upperbody.xml')
    security.start()
    app.run(host='0.0.0.0', debug=False)

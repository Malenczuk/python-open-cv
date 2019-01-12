#!/usr/bin/env python
from flask import Flask, render_template, Response, request, redirect, url_for
from flask_basicauth import BasicAuth
from camera import VideoCamera
from security import Security
import mail


app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = 'student'
app.config['BASIC_AUTH_PASSWORD'] = 'student'
app.config['BASIC_AUTH_FORCE'] = True
basic_auth = BasicAuth(app)


video_camera = VideoCamera()
selected_filter = None
selected_model = None


@app.route('/')
@basic_auth.required
def index():
    return render_template('index.html', Filters=video_camera.functions.keys())


@app.route('/models')
def model_settings():
    return render_template('models.html', Models=video_camera.models.keys())


@app.route('/settings/mail', methods=['GET', 'POST'])
def mail_settings():
    if request.method == "POST":
        mail.fromEmail = request.form['fromEmail']
        mail.fromEmailPassword = request.form['fromEmail']
        mail.toEmail = request.form['fromEmail']
        return "Settings changed"
    return render_template('mailForm.html', fromEmail=mail.fromEmail, toEmail=mail.toEmail)


@app.route('/camera')
def index_camera():
    global selected_filter, selected_model
    selected_filter = request.args.get("filter")
    selected_model = request.args.get("model")
    if selected_filter:
        if "Harr Cascades" in selected_filter and selected_model not in video_camera.models.keys():
            return redirect('/models')
    video_camera.set_model(selected_model)
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
    security = Security(video_camera)
    security.set_classifier('frontalface_default')
    # security.start()
    app.run(host='0.0.0.0', debug=False)

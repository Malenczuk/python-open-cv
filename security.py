from threading import Thread
from mail import send_email
import datetime
import time
import cv2


class Security(Thread):

    def __init__(self, video, classifier):
        super().__init__()
        self.video = video
        self.classifier = cv2.CascadeClassifier(classifier)
        self.flip = False

        self.save_video = True
        self.out = None
        self.recording = False
        self.record_time_after_found = 10.0

        self.email_update = True
        self.email_update_interval = 600.0

        self.running = False

    def stop(self):
        self.running = False

    def run(self):
        self.running = True
        last_epoch = 0
        last_found = 0

        while self.running:
            frame, jpeg, found_obj = self.video.get_object(self.classifier, self.flip)

            if self.save_video:
                if found_obj:
                    last_found = time.time()
                    if not self.recording:
                        self.start_recording(datetime.datetime.today().strftime('%Y-%m-%d-%H:%M:%S.avi'))
                elif self.recording and (time.time() - last_found) > self.record_time_after_found:
                    self.stop_recording()

                if self.recording:
                    self.record_frame(frame)

            if self.email_update:
                if found_obj and (time.time() - last_epoch) > self.email_update_interval:
                    last_epoch = time.time()
                    self.send_mail(jpeg)

    def change_classifier(self, classifier):
        self.classifier = cv2.CascadeClassifier(classifier)

    def record_frame(self, frame):
        if self.out:
            self.out.write(frame)

    def start_recording(self, file, frames=5, size=(640, 480)):
        self.recording = True
        self.out = cv2.VideoWriter(file, cv2.VideoWriter_fourcc(*"MJPG"), frames, size)
        print("Started recording to {} at {} frames with {} resolution".format(file, frames, size))

    def stop_recording(self):
        if self.recording and self.out:
            self.recording = False
            self.out.release()
            print("Stopped recording")

    def send_mail(self, frame):
        try:
            print("Sending email...")
            send_email(frame)
            print("done!")
        except Exception as e:
            print("Error sending email: ", str(e))

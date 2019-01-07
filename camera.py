import cv2
from functools import reduce
import numpy as np

_PATH = 'haarcascades/haarcascade_frontalface_default.xml'


class VideoCamera:

    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.face_haar_cascade = cv2.CascadeClassifier(_PATH)
        self.fgbg_mog = cv2.bgsegm.createBackgroundSubtractorMOG()
        self.fgbg_mog2 = cv2.createBackgroundSubtractorMOG2()
        self.fgbg_gmg = cv2.bgsegm.createBackgroundSubtractorGMG()
        self.fgbg_gmg_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

    def __del__(self):
        self.video.release()

    def background_subtractor_mog(self, image):
        return self.fgbg_mog.apply(image)

    def background_subtractor_mog2(self, image):
        return self.fgbg_mog2.apply(image)

    def background_subtractor_gmg(self, image):
        return cv2.morphologyEx(self.fgbg_gmg.apply(image), cv2.MORPH_OPEN, self.fgbg_gmg_kernel)

    def canny(self, image):
        return cv2.Canny(image, 100, 200)

    def face_detection(self, image):
        # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_haar_cascade.detectMultiScale(image, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
        return image

    functions = {'Background Subtractor MOG': background_subtractor_mog,
                 'Background Subtractor MOG2': background_subtractor_mog2,
                 'Background Subtractor GMG': background_subtractor_gmg,
                 'Face Detection': face_detection,
                 'Canny': canny,
                 }

    def get_frame(self, flip=False):
        success, frame = self.video.read()
        # if not success:
        #     self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)
        #     success, frame = self.video.read()
        return frame if not flip else np.flip(frame, 0)

    def get_image(self, filters=None):
        frame = self.get_frame().copy()
        image = reduce(lambda img, fun: self.functions.get(fun, lambda x, y: y)(self, img), [frame] + filters)
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def get_object(self):
        found_objects = False
        frame = self.get_frame().copy()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        objects = self.face_haar_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        if len(objects) > 0:
            found_objects = True

        # Draw a rectangle around the objects
        for (x, y, w, h) in objects:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        _, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes(), found_objects

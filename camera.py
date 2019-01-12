import glob
import os

import cv2
import numpy as np


def get_models():
    cur_path = os.curdir
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    files = glob.glob("haarcascades/*.xml")
    models = [f[25:-4] for f in files]
    os.chdir(cur_path)
    return dict(zip(models, files))


class VideoCamera:

    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.models = get_models()
        self.haar_cascade = None
        # self.fgbg_mog = cv2.bgsegm.createBackgroundSubtractorMOG()
        self.fgbg_mog2 = cv2.createBackgroundSubtractorMOG2()
        # self.fgbg_gmg = cv2.bgsegm.createBackgroundSubtractorGMG()
        self.fgbg_gmg_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

    def __del__(self):
        self.video.release()

    def set_model(self, name):
        if name in self.models.keys():
            self.haar_cascade = cv2.CascadeClassifier(self.models.get(name))

    def none(self, frame):
        return frame

    def background_subtractor_mog(self, image):
        return self.fgbg_mog.apply(image)

    def background_subtractor_mog2(self, image):
        return self.fgbg_mog2.apply(image)

    def background_subtractor_gmg(self, image):
        return cv2.morphologyEx(self.fgbg_gmg.apply(image), cv2.MORPH_OPEN, self.fgbg_gmg_kernel)

    def canny(self, image):
        return cv2.cvtColor(cv2.Canny(image, 100, 200), cv2.COLOR_GRAY2RGB)

    def laplacian(self, image):
        return cv2.Laplacian(image, cv2.CV_64F)

    def sobelx(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=5)
        return sobelx

    def sobely(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=5)
        return sobely

    def harr_cascades(self, image):
        if self.haar_cascade:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            faces = self.haar_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags=cv2.CASCADE_SCALE_IMAGE
            )
            for (x, y, w, h) in faces:
                cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
        return image

    functions = {'Background Subtractor MOG': background_subtractor_mog,
                 'Background Subtractor MOG2': background_subtractor_mog2,
                 'Background Subtractor GMG': background_subtractor_gmg,
                 'Harr Cascades': harr_cascades,
                 'Canny': canny,
                 'Laplacian': laplacian,
                 'Sobel X': sobelx,
                 'Sobel Y': sobely,
                 'None': none
                 }

    def get_frame(self, flip=False):
        success, frame = self.video.read()
        # if not success:
        #     self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)
        #     success, frame = self.video.read()

        return frame if not flip else np.flip(frame, 0)

    def get_image(self, filter=None, flip=False):
        frame = self.get_frame(flip).copy()
        image = self.functions.get(filter, lambda x, y: y)(self, frame)
        # image = np.hstack((frame, image))
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def get_object(self, classifier, flip=False):
        found_objects = False
        frame = self.get_frame(flip).copy()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        objects = classifier.detectMultiScale(
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
        return frame, jpeg.tobytes(), found_objects

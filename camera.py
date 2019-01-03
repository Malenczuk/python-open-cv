import cv2
from functools import reduce

_PATH = 'haarcascade_frontalface_default.xml'


class VideoCamera(object):

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
        return self.fgbg_mog.apply(image)

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

    functions = {'background_subtractor_mog': background_subtractor_mog,
                 'background_subtractor_mog2': background_subtractor_mog2,
                 'background_subtractor_gmg': background_subtractor_gmg,
                 'face_detection': face_detection,
                 'canny': canny,
                 }

    def get_frame(self, filters=None):
        success, image = self.video.read()
        image = reduce(lambda img, fun: self.functions.get(fun, lambda x, y: y)(self, img), [image] + filters)
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

from threading import Thread
import cv2
import platform
from constants import webcam_index


class Webcam:
    def __init__(self):
        self.stopped = False
        self.stream = None
        self.lastFrame = None
        self.os_name = platform.system()

    def start(self):
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        if self.stream is None:
            if self.os_name == "Windows":
                # self.stream = cv2.VideoCapture(0, cv2.CAP_DSHOW)
                self.stream = cv2.VideoCapture(webcam_index)
            elif self.os_name == "Darwin":  # macOS
                self.stream = cv2.VideoCapture(webcam_index, cv2.CAP_AVFOUNDATION)
            else:  # Linux
                self.stream = cv2.VideoCapture(webcam_index, cv2.CAP_V4L)
        while True:
            if self.stopped:
                return
            (result, image) = self.stream.read()
            if not result:
                self.stop()
                return
            self.lastFrame = cv2.flip(image, 1)

    def read(self):
        # Dividir el frame en dos mitades
        half_width = int(self.width() // 2)
        left_frame = self.lastFrame[:, :half_width, :]
        right_frame = self.lastFrame[:, half_width:, :]
        return right_frame, left_frame

    def stop(self):
        self.stream.release()
        self.stopped = True

    def width(self):
        return self.stream.get(cv2.CAP_PROP_FRAME_WIDTH)

    def height(self):
        return self.stream.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def ready(self):
        return self.lastFrame is not None


webcam = Webcam()

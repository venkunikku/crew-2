from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread
from multiprocessing import Process


class StreamThreaded:
    def __init__(self, resolution=(640, 480), framerate=32):
        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.camera.framerate = framerate
        self.rawCapture = PiRGBArray(self.camera, size=resolution)
        self.stream = self.camera.capture_continuous(self.rawCapture, format='bgr', use_video_port=True)
        self.frame = None
        self.stopped = False

    def start(self):
        print("Starting thread")
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        print("In Update method", self.stream)
        for f in self.stream:
            #print("in Update", f.array)
            self.frame = f.array
            self.rawCapture.truncate(0)

            if self.stopped:
                self.stream.close()
                self.rawCapture.close()
                self.camera.close()
                return

    def read(self):
        return self.frame

    def stop(self):
        self.stopped = True


class StreamMultiProcssing:
    def __init__(self, resolution=(640, 480), framerate=32):
        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.camera.framerate = framerate
        self.rawCapture = PiRGBArray(self.camera, size=resolution)
        self.stream = self.camera.capture_continuous(self.rawCapture, format='bgr', use_video_port=False)
        self.frame = None
        self.stopped = False

    def start(self):
        print("Starting thread")
        Process(target=self.update, args=()).start()
        return self

    def update(self):
        for f in self.stream:
            print("in Update", f.array)
            self.frame = f.array
            self.rawCapture.truncate(0)

            if self.stopped:
                self.stream.close()
                self.rawCapture.close()
                self.camera.close()
                return

    def read(self):
        return self.frame

    def stop(self):
        self.stopped = True

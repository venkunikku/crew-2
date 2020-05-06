from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread
import multiprocessing
import time


class StreamThreaded:
    def __init__(self, resolution=(640, 480), framerate=32):
        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.camera.framerate = framerate
        self.rawCapture = PiRGBArray(self.camera, size=resolution)
        self.stream = self.camera.capture_continuous(self.rawCapture, format='bgr', use_video_port=True)
        self.frame = None
        self.stopped = False
        self.t = None
        time.sleep(2)

    def start(self):
        print("Starting thread")
        self.t = Thread(target=self.update, args=())
        self.t.start()
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
                print("Video Cleanup")
                return

    def read(self):
        return self.frame

    def stop(self):
        self.stopped = True
        print("Stopping the camera")

    def stop_thread(self):
        self.t.join()
        print("Camera Thread joined")


class StreamMultiProcssing:
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
        p1 = multiprocessing.Process(target=self.update, args=(), name="Video")
        p1.start()
        print("Process p1:", p1)
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


class StreamMultiProcssing:
    def __init__(self, resolution=(640, 480), framerate=32):
        #         self.camera = None
        self.resolution = resolution
        self.framerate = framerate
        self.frame = None
        self.stopped = False
        self.q = multiprocessing.Queue()
        #         self.rawCapture = None
        #         self.stream = None
        print("Camera object")

    def start(self):
        print("Starting Multil Processing")

        p1 = multiprocessing.Process(target=self.update, args=(self.q, self.resolution, self.framerate), name="Video",
                                     daemon=False)
        p1.start()
        # p1.join()
        print("Process p1:", p1)
        return self

    def update(self, q, resolution, framerate):
        from picamera.array import PiRGBArray
        from picamera import PiCamera
        # from threading import Thread
        camera = PiCamera()
        camera.resolution = resolution
        camera.framerate = framerate
        rawCapture = PiRGBArray(camera, size=resolution)
        stream = camera.capture_continuous(rawCapture, format='bgr', use_video_port=True)
        for f in stream:
            # print("in Update", f.array)
            self.frame = f.array
            q.put(f.array)
            rawCapture.truncate(0)

            if self.stopped:
                print("[info] Stopping he stream")
                stream.close()
                rawCapture.close()
                camera.close()
                return

    def read(self):
        return self.q  # frame

    def read2(self):
        return self.frame

    def stop(self):
        self.stopped = True

    def take_picture(self):
        pass

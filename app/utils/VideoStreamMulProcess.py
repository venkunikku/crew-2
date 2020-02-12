import multiprocessing


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
        
        p1 = multiprocessing.Process(target=self.update, args=(self.q, self.resolution, self.framerate), name="Video", daemon=False)
        p1.start()
        #p1.join()
        print("Process p1:", p1)
        return self

    def update(self, q, resolution, framerate):
        from picamera.array import PiRGBArray
        from picamera import PiCamera
        #from threading import Thread
        camera = PiCamera()
        camera.resolution = resolution
        camera.framerate = framerate
        rawCapture = PiRGBArray(camera, size=resolution)
        stream = camera.capture_continuous(rawCapture, format='bgr', use_video_port=True)
        for f in stream:
            #print("in Update", f.array)
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
        return self.q #frame
    
    def read2(self):
        return self.frame

    def stop(self):
        self.stopped = True
        
    def take_picture(self):
        pass

if __name__ == '__main__':
    cam = StreamMultiProcssing().start()
    print(cam.read())

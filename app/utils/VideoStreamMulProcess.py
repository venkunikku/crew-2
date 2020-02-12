import multiprocessing
from picamera.array import PiRGBArray
from picamera import PiCamera

class StreamMultiProcssing:
    def __init__(self, resolution=(640, 480), framerate=32):
        self.p1 = None
        self.camera = None
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
        
        self.p1 = multiprocessing.Process(target=self.update, args=(self.q, self.resolution, self.framerate, self.camera), name="Video", daemon=False)
        self.p1.start()
        #p1.join()
        print("Process p1:", self.p1)
        return self

    def update(self, q, resolution, framerate, camera):
        #from threading import Thread
        # camera = PiCamera()
        camera = PiCamera()
        print('In update method', camera)
        camera.resolution = resolution
        camera.framerate = framerate
        rawCapture = PiRGBArray(camera, size=resolution)
        stream = camera.capture_continuous(rawCapture, format='bgr', use_video_port=True)
        for f in stream:
            #print("in Update", f.array)
            self.frame = f.array
            q.put(f.array)
            rawCapture.truncate(0)
            print("Stoped?:", self.stopped)
            if self.stopped:
                print("[info] Stopping he stream")
                self.p1.terminate()
                stream.close()
                rawCapture.close()
                camera.close()
                return

    def read(self):
        return self.q #frame
    
    def read2(self):
        return self.frame

    def stop(self):
        print("[info] stopping the Process")
        self.p1.join()
        self.stopped = True
        
    def take_picture(self):
        pass

class StreamMultiProcssing:
    def __init__(self, resolution=(640, 480), framerate=32, q_in, q_out):
        self.p1 = None
        self.camera = PiCamera()
        self.resolution = resolution
        self.framerate = framerate
        self.frame = None
        self.stopped = False
        self.q_in = q_in
        self.q_out = q_out
        self.rawCapture = PiRGBArray(camera, size=resolution)
        self.stream = camera.capture_continuous(rawCapture, format='bgr', use_video_port=True)
        print("Camera object")

    def update(self):
          for f in self.stream:
            #print("in Update", f.array)
            self.frame = f.array
            self.q_in.put(f.array)
            self.rawCapture.truncate(0)
            print("Stoped?:", self.stopped)
            
          while frame.empty() is False:
                  if self.stopped:
                          stream.close()
                          rawCapture.close()
                          camera.close()
                          return
                          
                        

    def read(self):
        return self.q #frame
    
    def read2(self):
        return self.frame

    def stop(self):
        print("[info] stopping the Process")
        self.p1.join()
        self.stopped = True
        
    def take_picture(self):
        pass

if __name__ == '__main__':
    cam = StreamMultiProcssing().start()
    print(cam.read())

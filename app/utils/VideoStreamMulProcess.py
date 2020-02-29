import multiprocessing
from picamera.array import PiRGBArray
from picamera import PiCamera
import os
import time

# class StreamMultiProcssing:
    # def __init__(self, resolution=(640, 480), framerate=32):
        # self.p1 = None
        # self.camera = None
        # self.resolution = resolution
        # self.framerate = framerate
        # self.frame = None
        # self.stopped = False
        # self.q = multiprocessing.Queue()
        # #         self.rawCapture = None
        # #         self.stream = None
        # print("Camera object")

    # def start(self):
        # print("Starting Multil Processing")

        # self.p1 = multiprocessing.Process(target=self.update,
                                          # args=(self.q, self.resolution, self.framerate, self.camera), name="Video",
                                          # daemon=False)
        # self.p1.start()
        # # p1.join()
        # print("Process p1:", self.p1)
        # return self

    # def update(self, q, resolution, framerate, camera):
        # # from threading import Thread
        # # camera = PiCamera()
        # camera = PiCamera()
        # print('In update method', camera)
        # camera.resolution = resolution
        # camera.framerate = framerate
        # rawCapture = PiRGBArray(camera, size=resolution)
        # stream = camera.capture_continuous(rawCapture, format='bgr', use_video_port=True)
        # for f in stream:
            # # print("in Update", f.array)
            # self.frame = f.array
            # q.put(f.array)
            # rawCapture.truncate(0)
            # print("Processs?:", os.getpid())
            # if self.stopped:
                # print("[info] Stopping he stream")
                # self.p1.terminate()
                # stream.close()
                # rawCapture.close()
                # camera.close()
                # return

    # def read(self):
        # return self.q  # frame

    # def read2(self):
        # return self.frame

    # def stop(self):
        # print("[info] stopping the Process")
        # self.p1.join()
        # self.stopped = True

    # def take_picture(self):
        # pass


# class MulPrc:
    # def __init__(self, resolution=(640, 480), framerate=32):
        # #self.p1 = None
        # self.camera = PiCamera()
        # self.resolution = resolution
        # self.framerate = framerate
        # self.frame = None
        # self.stopped = False
        # # self.q_in = q_in
        # # self.q_out = q_out
        # self.rawCapture = PiRGBArray(self.camera, size=resolution)
        # self.stream = self.camera.capture_continuous(self.rawCapture, format='bgr', use_video_port=True)
        # print("Camera object initiating")

    # def update(self, q_in, q_out):
        # print("Calling update Object", self.stream)
        # print("Processs?:", os.getpid())
        # for f in self.stream:
            # print("in Update", f.array)
            # self.frame = f.array
            # q_out.put(f.array)
            # q_in.put(f.array)
            # self.rawCapture.truncate(0)

        # # while q_in.empty() is False:
            # # in_object = q_in.get()
            # # print("Inside in queue", )
            # # if in_object == 'stop':
                # # self.stream.close()
                # # self.rawCapture.close()
                # # self.camera.close()
                # # return


# class MultiProcessInitiate:
    # def __init__(self):
        # self.q_in = multiprocessing.Queue()
        # self.q_out = multiprocessing.Queue()
        # self.p1 = None
        # print("[info] Starting MultiProcessing", self.p1)

    # def start(self):
        # print("[info] starting the process")
        # #cam_obj = MulPrc()
        # #print(cam_obj)
        
        # self.p1 = multiprocessing.Process(target=MulPrc().update, args=(self.q_in, self.q_out))
        # self.p1.start()
        # return self

    # def read(self):
        # return self.q_out

    # def stop(self):
        # print("Stopping cam")
        # self.q_in.put("stop")
        # self.p1.join()


def run_video(instance):
    with PiCamera() as camera:
            #with PiRGBArray(camera, size=(640, 480))
            camera.resolution=(640, 480)
            camera.framerate=32
                
            rawCapture = PiRGBArray(camera, size=(640, 480))
            stream = camera.capture_continuous(rawCapture, format='bgr', use_video_port=True)
            time.sleep(2.0)
            for f in stream:
                                       
                    #print("in Update", f.array)
                    frame = f.array
                    instance.put(frame)
                    #q_in.put(f.array)
                    rawCapture.truncate(0)
            
def run_process():
        q = multiprocessing.Queue()
        p1 = multiprocessing.Process(target=run_video, args=(q, ))
        p1.start()
        
        return q, p1
        

if __name__ == '__main__':
    cam = StreamMultiProcssing().start()
    print(cam.read())

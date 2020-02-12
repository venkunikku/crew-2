import time
import multiprocessing
from picamera.array import PiRGBArray
from picamera import PiCamera

square_results = []


def calc_square(numbers):
    print("Calculating sq")
    global square_results
    for n in numbers:
        time.sleep(0.2)
        print("square", n ** 2)
        square_results.append(n ** 2)
    print(f"Printing within the process: {square_results}")


def calc_cube(numbers):
    print("Calculatin Cube")
    for n in numbers:
        time.sleep(0.2)
        print("Cube", n ** 3)
#     resolution=(640, 480) 
#     framerate=32
#     camera = PiCamera()
#     camera.resolution = resolution
#     camera.framerate = framerate
#     rawCapture = PiRGBArray(camera, size=resolution)
#     stream = camera.capture_continuous(rawCapture, format='bgr', use_video_port=True)
#     frame = None
#     stopped = False
#     print("Stream:", stream)
#     for i,f in enumerate(stream):
#         print("in Update",i, f.array)
#         frame = f.array
#         rawCapture.truncate(0)
#         if i ==10:
#             break
#         
#     camera.close
#     stream.close()
#     rawCapture.close()
#     camera.close()


if __name__ == "__main__":
    arr = [2, 3, 8, 9]

    t = time.time()
    #p1 = multiprocessing.Process(target=calc_square, args=(arr,))
    p2 = multiprocessing.Process(target=calc_cube, args=(arr,), name="Cube Process", daemon= True)
    #p1.start()
    p2.start()

    #p1.join()
    #p2.join()
    print(time.time() - t)
    print(f"Printing results: {square_results}")
    
    resolution=(640, 480) 
    framerate=32
    
#     camera = PiCamera()
#     camera.resolution = resolution
#     camera.framerate = framerate
#     rawCapture = PiRGBArray(camera, size=resolution)
#     stream = camera.capture_continuous(rawCapture, format='bgr', use_video_port=True)
#     frame = None
#     stopped = False
#     for f in stream:
#         #print("in Update", f.array)
#         frame = f.array
#         rawCapture.truncate(0)
#         break
#     camera.close
#     stream.close()
#     rawCapture.close()
#     camera.close()
            
            
            

from app.utils import VideoStream
import cv2
import time

if __name__ == '__main__':
	cam = VideoStream.StreamMultiProcssing().start()
	time.sleep(5.0)
	try:     
		#cam.start()
		#print(cam.read())
		while True:
			frame = cam.read()
			#print(f"Frame: {frame}")
			if frame:
				cv2.imshow("inter", frame)
			k = cv2.waitKey(1) & 0xFF
			if k ==27:
				break
			
		cam.stop()
	except Exception as e:
		print("Error", e)
		cam.stop()

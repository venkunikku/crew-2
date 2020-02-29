from app.utils import video_stream, VideoStreamMulProcess
import cv2
import time
import traceback
import atexit
import os

process = True
cam = None

def clean_up():
	global cam
	print("Cleaning up using the hook", cam)
	cam.stop()


if __name__ == '__main__':
	#cam = VideoStreamMulProcess.StreamMultiProcssing().start()
	#cam = VideoStream.StreamThreaded().start()
	#cam = VideoStreamMulProcess.MultiProcessInitiate().start()
	cam = VideoStreamMulProcess.run_process()
	atexit.register(clean_up)
	time.sleep(2.0)
	try:     
		#cam.start()
		#print(cam.read())
		while True:
			frame = cam[0]#.read()
			#print("Main", os.getpid())
			#print(f"Frame: {type(frame)}")
			
# 			while frame.empty is False:
#                             print(frame.get())
			
			if process:
				while frame.empty() is False:
					cv2.imshow("inter", frame.get())
			else:
				cv2.imshow("inter", frame)
			  
			k = cv2.waitKey(1) & 0xFF
			if k ==27:
				print("Clicked on escape")
				break 
			#print(".", end=" ")
		cv2.destroyAllWindows()	
		#cam.stop()
		cam[1].join()
		cam[1].terminate()
	except (KeyboardInterrupt, Exception) as e:
		print("Error", e)
		cam.stop()
		print(traceback.print_exc())
	finally:
		cam.stop()
		
	



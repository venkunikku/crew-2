import cv2
import numpy as np
from app.utils import find_objects, raspberry_utils
import datetime
import argparse



def records_for_proofs(filename='output_with_cones.avi', w=640, h=480):
	fourcc = cv2.VideoWriter_fourcc(*"XVID")
	out = cv2.VideoWriter(filename, fourcc, 20.0, (w, h)) # 20 frams
	return out

ap = argparse.ArgumentParser()
ap.add_argument("-r", "--record", required=False, help="Path to the image")
args = vars(ap.parse_args())


cap = cv2.VideoCapture(0)

record = args["record"]
if record == "True":
	w=int(cap.get(cv2.CV_CAP_PROP_FRAME_WIDTH ))
	h=int(cap.get(cv2.CV_CAP_PROP_FRAME_HEIGHT ))
	out = records_for_proofs(w=w, h=h)




cone_obj = find_objects.FindCones()

while True:
	temperature = raspberry_utils.processor_temperature()
	
	
	res, frame = cap.read()
	flag, frame_back, total_cones, boxes = cone_obj.find_cone(frame)
    
	if total_cones > 0:
		dt = datetime.datetime.now()
		cv2.putText(frame_back, f"Total Cones Found: {total_cones}. ({dt})", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, .5, (0,255, 255), 1, cv2.LINE_AA)
	
	cv2.putText(frame_back, f"Temp:{temperature}", (50, 30), cv2.FONT_HERSHEY_SIMPLEX, .5, (0,255, 255), 1, cv2.LINE_AA)
	cv2.imshow("Cone", frame_back)
	
	if record == "True":
		out.write(frame_back)

	k = cv2.waitKey(1) & 0xFF
	if k == 27:
		break

cap.release()
cv2.destroyAllWindows()

if record == "True":
	out.release()



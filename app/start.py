import cv2
import numpy as np
from app.utils import find_objects, raspberry_utils
import datetime
import argparse
from easygopigo3 import EasyGoPiGo3
import math


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




cone_obj = find_objects.FindCones(color="red")
easy = EasyGoPiGo3()

while True:
	temperature = raspberry_utils.processor_temperature()
	
	
	res, frame = cap.read()
	flag, frame_back, total_cones, boxes, cones_data = cone_obj.find_cone(frame)
	
	if total_cones > 0:
		dt = datetime.datetime.now()
		cv2.putText(frame_back, f"Total Cones Found: {total_cones}. ({dt})", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, .5, (0,255, 255), 1, cv2.LINE_AA)
	
	
	cv2.putText(frame_back, f"Temp:{temperature}", (50, 30), cv2.FONT_HERSHEY_SIMPLEX, .5, (0,255, 255), 1, cv2.LINE_AA)
	
	he, wi, ch = frame.shape
	center_of_the_screen = (wi//2, he//2)
	cv2.circle(frame_back, center_of_the_screen, 5, [255, 0, 0], -1)
	cv2.line(frame_back, center_of_the_screen, (center_of_the_screen[0]+30, center_of_the_screen[1] ), [0, 255, 0], 3)

	
	if cones_data:
		b_box_rec = cones_data['cone-0']['bouding_box_center']
		print(f"Center of the rectangle-{b_box_rec}")
		print(f"Center of the screen-{center_of_the_screen}")
		cv2.line(frame_back, b_box_rec, center_of_the_screen, [0, 255, 0], 3)
		angle = int(math.atan((b_box_rec[1] - center_of_the_screen[1])/(b_box_rec[0] - center_of_the_screen[0])) * 180/math.pi )
		print(F"Angle is{angle}")
		cv2.putText(frame_back, f"Angle: {angle}", (center_of_the_screen[0]-10, center_of_the_screen[1]-10), cv2.FONT_HERSHEY_SIMPLEX, .5, (0,255, 255), 1, cv2.LINE_AA)
		
		#if b_box_rec[0] > center_of_the_screen[0]:
		#	print("Percentages", b_box_rec[0]/center_of_the_screen[0], center_of_the_screen[0]/b_box_rec[0])
		#	perc = round(center_of_the_screen[0]/b_box_rec[0], 2)
		#	#easy.right()
		#	easy.steer(perc, 0)
		#	#easy.stop()
		#	print("yes greated")
	
	
	
	
	cv2.imshow("Cone", frame_back)
	
	if record == "True":
		out.write(frame_back)

	k = cv2.waitKey(1) & 0xFF
	if k == 27:
		break

cap.release()
cv2.destroyAllWindows()
easy.reset_all()
if record == "True":
	out.release()



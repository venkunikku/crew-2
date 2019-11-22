import cv2
import numpy as np
from app.utils import find_objects, raspberry_utils, gopigo_controls
import datetime
import argparse
from easygopigo3 import EasyGoPiGo3
import math
import time

cap = None
easy = EasyGoPiGo3()

def center_cone():
	b_box_rec = cones_data['cone-0']['bouding_box_center']
	print(f"Center of the rectangle-{b_box_rec}")
	print(f"Center of the screen-{center_of_the_screen}")
	cv2.line(frame_back, b_box_rec, center_of_the_screen, [0, 255, 0], 3)
	if center_of_the_screen[0] != b_box_rec[0]: # if the angle is not equal to 90 only do thistohis else we are getting divde by 0 error
		angle = int(math.atan((b_box_rec[1] - center_of_the_screen[1])/(b_box_rec[0] - center_of_the_screen[0])) * 180/math.pi )
	else:
		angle = 90
	print(F"Angle is{angle}")
	cv2.putText(frame_back, f"Angle: {angle}", (center_of_the_screen[0]-10, center_of_the_screen[1]-10), cv2.FONT_HERSHEY_SIMPLEX, .5, (0,255, 255), 1, cv2.LINE_AA)
	
	#if b_box_rec[0] > center_of_the_screen[0]:
	#	print("Percentages", b_box_rec[0]/center_of_the_screen[0], center_of_the_screen[0]/b_box_rec[0])
	#	perc = round(center_of_the_screen[0]/b_box_rec[0], 2)
	#	#easy.right()
	#	easy.steer(perc, 0)
	#	#easy.stop()
	#	print("yes greated")
	#if angle >0:
		#easy.turn_degrees(angle/2)
		#import time
		#time.sleep(10)
		#break
		
def move_around_to_find_cone(cone_obj, raw_capture, obj, degress_area_to_scan=50, degress_to_move=15, loops_to_check = 100):
	raw_capture.truncate(0)


	
	#obj = camera.capture_continuous(raw_capture, format="bgr", use_video_port=True)
	#easy.turn_degrees(degrees_to_turn)
	#easy.stop()
	#time.sleep(.5)
	
	#for frm in obj:
	#iterator = iter(obj)
	#frame = (next(iterator)).array
	
	if degress_to_move > degress_area_to_scan:
		raise Exception(f"degress_to_move:{degress_to_move} should be lesser than degress_area_to_scan:{degress_area_to_scan}")
	

	
	
	# i = 0
	# for fram in obj:
		# frame = fram.array
		# i += 1
		# flag, frame_back, total_cones, boxes, cones_data = cone_obj.find_cone(frame)
		# if total_cones > 0:
			# print("Found cone no side side")
			# #return flag, frame_back, total_cones, boxes, cones_data
			# return True
		# if i == loops_to_check:
			# break
		# raw_capture.truncate(0)
	
	
	
	# no_of_turns =0
	# # steer to to right
	# for i in range(0, degress_area_to_scan, degress_to_move):
		# no_of_turns += 1
		# easy.turn_degrees(degress_to_move)
		# time.sleep(1)
		# print(f"For loop i: {i} and total Degrees turned: {no_of_turns}")
		# i = 0 
		# raw_capture.truncate(0)
		# for fram in obj:
			# frame = fram.array
			# i += 1
			# flag, frame_back, total_cones, boxes, cones_data = cone_obj.find_cone(frame)
			# if total_cones > 0:
				# print("Found cone on right side")
				# ##return flag, frame_back, total_cones, boxes, cones_data
				# return True
			# if i == loops_to_check:
				# break
			# raw_capture.truncate(0)
	# print(f"Final Degrees truning: {no_of_turns}")
	# rest_to_original_position(-no_of_turns, degress_to_move)
	
	# time.sleep(2)
	
	# # steer to to left
	# no_of_turns = 0
	# for i in range(0, degress_area_to_scan, degress_to_move):
		# no_of_turns += 1
		# easy.turn_degrees(-degress_to_move)
		# #easy.stop()
		# time.sleep(1)
		# i = 0 
		# raw_capture.truncate(0)
		# for fram in obj:
			# frame = fram.array
			# flag, frame_back, total_cones, boxes, cones_data = cone_obj.find_cone(frame)
			# if total_cones > 0:
				# print("Found cone on left side")
				# #return flag, frame_back, total_cones, boxes, cones_data
				# return True
			# if i == loops_to_check:
				# break
			# raw_capture.truncate(0)
	# print(f"Final Degrees truning: {no_of_turns}")
	# # rest_to_original_position(no_of_turns, degress_to_move)
	# # easy.reset_all()
	
	turn_deg_liste = [0, 15, -30, 45, -90]
	
	for d in turn_deg_liste:
		easy.turn_degrees(d)
		time.sleep(1)
		i = 0 
		print(f"Chekcing for Degress:{d}")
		
		for fram in obj:
			i += 1
			frame = fram.array
			flag, frame_back, total_cones, boxes, cones_data = cone_obj.find_cone(frame)
			if total_cones > 0:
				print("Found cone on left side")
				#return flag, frame_back, total_cones, boxes, cones_data
				return True
			if i == loops_to_check:
				raw_capture.truncate(0)
				break
			raw_capture.truncate(0)
	
	return False
	
		
		
	

def move_to_center_of_screen(cone_color="red", cap=None, height_range=(280, 360), cone_boudning_box=None):

				
	if cone_boudning_box[0] > height_range[1]:
		# move right
		print(F"Moving right")
		easy.steer(2, 0)
		time.sleep(2)
		easy.stop()



	if cone_boudning_box[0] < height_range[1]:
		# move left
		print(F"Moving left")
		easy.steer(0, 1)
		time.sleep(2)
		easy.stop()
			
			
		
		#print(F"Getting cone coordinate again")
		#flag, frame_back, total_cones, boxes, cones_data = cone_obj.find_cone(frame)
		#if total_cones > 0:
		#	print("Found cone")
		#	cone_boudning_box = cones_data['cone-0']['bouding_box_center']
		#print(f"Condition check: {height_range[0] <= cone_boudning_box[0] >= height_range[1]}. For cone height: {cone_boudning_box[0]}")
		
def move_forward_backward(cone_bottom_mid_points_y,boundary_range=None, drive_inches=0.5):
	if boundary_range:
		if boundary_range[0] > cone_bottom_mid_points_y:
			easy.drive_inches(drive_inches)
		else:
			easy.drive_inches(-drive_inches)
		
		
		
def get_new_cone_bounding_boxes(cone_obj, frame):
	time.sleep(1)
	flag, frame_back, total_cones, boxes, cones_data = cone_obj.find_cone(frame)
	
	if total_cones > 0:
		cone_boudning_box = cones_data['cone-0']['bouding_box_center']
		#print("Bouding box", cone_boudning_box)
		return cone_boudning_box
	else:
		print("Cone Not found returning None")
		return None
	
def get_center_boundaries(frame):
	he, wi, ch = frame.shape
	center_of_the_screen = (wi//2, he//2)
	left_top, left_bottom = (wi-center_of_the_screen[0]-40,0), (wi-center_of_the_screen[0]-40, he)
	rigth_top, right_bottom = (wi-center_of_the_screen[0]+40,0), (wi-center_of_the_screen[0]+40, he)
	return left_top[0], rigth_top[0]
		

def center_boundaries(frm):
	frame = frm.copy()
	he, wi, ch = frame.shape
	center_of_the_screen = (wi//2, he//2)
	cv2.circle(frame, center_of_the_screen, 5, [255, 0, 0], -1)
	cv2.line(frame_back, center_of_the_screen, (center_of_the_screen[0]+30, center_of_the_screen[1] ), [0, 255, 0], 3)
	
	left_top, left_bottom = (wi-center_of_the_screen[0]-40,0), (wi-center_of_the_screen[0]-40, he)
	rigth_top, right_bottom = (wi-center_of_the_screen[0]+40,0), (wi-center_of_the_screen[0]+40, he)
	
	#print(F"Left: {left_top},{left_bottom} and Right: {rigth_top}, {right_bottom}")
	
	cv2.line(frame,left_top, left_bottom , [232, 206, 190], 1)
	cv2.line(frame,rigth_top ,right_bottom , [232, 206, 190], 1)
	return frame


def rest_to_original_position(no_of_turns, degress_to_move):
	print(f"To set to original position. Turn: {no_of_turns} and Degress to move: {degress_to_move}")
	easy.turn_degrees((no_of_turns)*degress_to_move)
	easy.stop()	

def records_for_proofs(filename='output_with_cones.avi', w=640, h=480):
	fourcc = cv2.VideoWriter_fourcc(*"XVID")
	out = cv2.VideoWriter(filename, fourcc, 20.0, (w, h)) # 20 frams
	return out

def midpoint(ptA, ptB):
	return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)
	
import math
def euclidean_distance(pt1, pt2):
	p1 = (pt1[0]-pt2[0])**2
	p2 = (pt1[1]-pt2[1])**2
	return math.sqrt(p1+p2)

ap = argparse.ArgumentParser()
ap.add_argument("-r", "--record", required=False, help="Path to the image")
ap.add_argument("-flp", "--flip_imgae", required=False, help="Path to the image")
args = vars(ap.parse_args())




#cap = cv2.VideoCapture(0)


record = args["record"]
isflip = args["flip_imgae"]

from picamera.array import PiRGBArray
from picamera import PiCamera

camera = PiCamera()
camera.resolution = (640, 480)
#camera.vflip = True
raw_capture = PiRGBArray(camera, size=(640, 480))
time.sleep(1)

cone_color = "yellow"
cone_obj = find_objects.FindCones(color=cone_color)
aline_cone_to_the_center = False

found_required_cone = True
is_cone_centered = True
forwarded = True 
frame_obj = camera.capture_continuous(raw_capture, format="bgr", use_video_port=True)
for frm in frame_obj:
	temperature = raspberry_utils.processor_temperature()
	frame = frm.array
	#print(image.shape, type(image), image)
	
	flag, frame_back, total_cones, boxes, cones_data = cone_obj.find_cone(frame)
	
	if not found_required_cone:
		# finding Cone
		found_required_cone = move_around_to_find_cone(cone_obj,raw_capture, frame_obj)
		raw_capture.truncate(0)
		continue
	
	frame_back = center_boundaries(frame_back)
	
	he, wi, ch = frame_back.shape
	center_of_the_screen = (wi//2, he//2)
	cv2.circle(frame_back, center_of_the_screen, 5, [255, 0, 0], -1)
	cv2.line(frame_back, center_of_the_screen, (center_of_the_screen[0]+30, center_of_the_screen[1] ), [0, 255, 0], 3)
	
	# center boundaries
	left_top, left_bottom = (wi-center_of_the_screen[0]-20,0), (wi-center_of_the_screen[0]-20, he)
	rigth_top, right_bottom = (wi-center_of_the_screen[0]+20,0), (wi-center_of_the_screen[0]+20, he)
	
	#print(F"Left: {left_top},{left_bottom} and Right: {rigth_top}, {right_bottom}")
	
	cv2.line(frame_back,left_top, left_bottom , [232, 206, 190], 1)
	cv2.line(frame_back,rigth_top ,right_bottom , [232, 206, 190], 1)
	
	cv2.line(frame_back,rigth_top ,right_bottom , [232, 206, 190], 1)
	
	# Center vertical line
	cv2.line(frame_back, (center_of_the_screen[0], 0), (center_of_the_screen[0],wi ), [0, 255, 0], 1)
	
	# bottom boundaries
	upper_left, upper_right = (0,he-100), (wi,he-100)
	lower_left, lower_right = (0,he-50), (wi,he-50)
	cv2.line(frame_back, upper_left, upper_right, [200, 90, 60], 1)
	cv2.line(frame_back, lower_left, lower_right, [200, 90, 60], 1)
	
	cv2.putText(frame_back, f"Upper: {upper_left},{upper_right}", upper_left, cv2.FONT_HERSHEY_SIMPLEX, .5, (0,255, 255), 1, cv2.LINE_AA)
	cv2.putText(frame_back, f"Lower: {lower_left},{lower_right}", lower_left, cv2.FONT_HERSHEY_SIMPLEX, .5, (0,255, 255), 1, cv2.LINE_AA)
			
	
	cv2.putText(frame_back, f"Temp:{temperature}", (50, 30), cv2.FONT_HERSHEY_SIMPLEX, .5, (0,255, 255), 1, cv2.LINE_AA)
	
	if found_required_cone:
		
		if total_cones > 0:
			#dt = datetime.datetime.now()
			cone_boudning_box = cones_data['cone-0']['bouding_box_center']
			
			
			
			if not is_cone_centered:
				
				height_range=(left_top[0], rigth_top[0])
				print(f"Cone no centered moving for height rnage:{height_range} and cone bouding box:{cone_boudning_box}")
				#cone_boudning_box = cones_data['cone-0']['bouding_box_center']
				if not height_range[0] <= cone_boudning_box[0] <= height_range[1]:
					print("Inside IF")
					#flag, frame_back, total_cones, boxes, cones_data = cone_obj.find_cone(frame)
					#if total_cones > 0:
					move_to_center_of_screen(frame_back, height_range=height_range, cone_boudning_box = cone_boudning_box )
					cone_boudning_box = cones_data['cone-0']['bouding_box_center']
					print("Cone Bouding box after adjustment:", cone_boudning_box)
				else :
					is_cone_centered = True
			x,y,w,h = boxes[0]
			x1, y1, x4, y4 = (x, y, x+w, y+h)
			tl = (x1, y1)
			tr = (x4, y1)
			br = (x4, y4)
			bl = (x1, y4)
			#(tl, tr, br, bl) = boxes[0]
			(tlblX, tlblY) = midpoint(tl, bl)
			(trbrX, trbrY) = midpoint(tr, br)
			rect_bottom_mind_point = midpoint(bl, br)
			
			cv2.putText(frame_back, f"bottom: {rect_bottom_mind_point}", (int(rect_bottom_mind_point[0]), int(rect_bottom_mind_point[1])), cv2.FONT_HERSHEY_SIMPLEX, .5, (0,255, 255), 1, cv2.LINE_AA)
			
			
			if is_cone_centered:
				cone_bottom_mid_points_y = rect_bottom_mind_point[1]
				hieght_range_forward = (upper_left[1]+20, lower_left[1]+20)
				if not forwarded:
					if not hieght_range_forward[0] <= cone_bottom_mid_points_y <=hieght_range_forward[1]:
						print(f"Foward Range: {hieght_range_forward}, Cone Center: {cone_bottom_mid_points_y}")
						move_forward_backward( cone_bottom_mid_points_y, hieght_range_forward,)
					else:
						forwarded= True
						is_cone_centered = False
					
				
				
	
	cv2.imshow("PI", frame_back)
	key = cv2.waitKey(1) & 0xFF
	
	raw_capture.truncate(0)
	
	if key == ord("q"):
		break





while True:
	
	temperature = raspberry_utils.processor_temperature()
	
	
	res, frame = cap.read()
	#print(f"Fame Shape:{frame.shape}")
	#frame = cv2.flip(cap, -1)
	
	if isflip == 'True':
		frame = frame[::-1]
	frame_back = frame
	# check surronding
	# find required 
	## Move to the center
	
	flag, frame_back, total_cones, boxes, cones_data = cone_obj.find_cone(frame)
	
	if total_cones > 0:
		dt = datetime.datetime.now()
		cone_boudning_box = cones_data['cone-0']['bouding_box_center']
		#cv2.putText(frame_back, f"Total Cones Found: {total_cones}. ({dt})", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, .5, (0,255, 255), 1, cv2.LINE_AA)
		#cv2.putText(frame_back, f"coord: {cone_boudning_box}", cone_boudning_box, cv2.FONT_HERSHEY_SIMPLEX, .5, (0,255, 255), 1, cv2.LINE_AA)
		
	
	
	cv2.putText(frame_back, f"Temp:{temperature}", (50, 30), cv2.FONT_HERSHEY_SIMPLEX, .5, (0,255, 255), 1, cv2.LINE_AA)
	
	

	frame_back = center_boundaries(frame_back)
	
	he, wi, ch = frame.shape
	center_of_the_screen = (wi//2, he//2)
	cv2.circle(frame, center_of_the_screen, 5, [255, 0, 0], -1)
	cv2.line(frame_back, center_of_the_screen, (center_of_the_screen[0]+30, center_of_the_screen[1] ), [0, 255, 0], 3)
	
	# center boundaries
	left_top, left_bottom = (wi-center_of_the_screen[0]-40,0), (wi-center_of_the_screen[0]-40, he)
	rigth_top, right_bottom = (wi-center_of_the_screen[0]+40,0), (wi-center_of_the_screen[0]+40, he)
	
	#print(F"Left: {left_top},{left_bottom} and Right: {rigth_top}, {right_bottom}")
	
	cv2.line(frame,left_top, left_bottom , [232, 206, 190], 1)
	cv2.line(frame,rigth_top ,right_bottom , [232, 206, 190], 1)
	
	# Center vertical line
	cv2.line(frame_back, (center_of_the_screen[0], 0), (center_of_the_screen[0],wi ), [0, 255, 0], 1)
	
	#time.sleep(4)
	#print(f"Found Count:{found_required_cone}")
	if not found_required_cone:
		found_required_cone = move_around_to_find_cone(cone_color=cone_color, cap = cap)
		print(f"Return val:{found_required_cone}")
	
	if found_required_cone:
		if not is_cone_centered:
			cone_boudning_box = cones_data['cone-0']['bouding_box_center']
			for i in range(1, 3):
				cone_boudning_box = move_to_center_of_screen(cap=cap, height_range=(left_top[0], rigth_top[0]), cone_boudning_box = cone_boudning_box )
				print("Cone Bouding box after adjustment:", cone_boudning_box, f"For run: {i}")
			is_cone_centered = True
	
	b_box_rec = cone_boudning_box
	cv2.line(frame_back, b_box_rec, center_of_the_screen, [0, 255, 0], 3)
	
	# Center Horizontal line
	cv2.line(frame_back, (center_of_the_screen[0], b_box_rec[1]), b_box_rec, [0, 255, 0], 3)
	print(F"Length of the x-axis line from the cone: {abs(center_of_the_screen[0]-b_box_rec[0] )}")
	
	
	if center_of_the_screen[0] != b_box_rec[0]: # if the angle is not equal to 90 only do thistohis else we are getting divde by 0 error
		angle = int(math.atan((b_box_rec[1] - center_of_the_screen[1])/(b_box_rec[0] - center_of_the_screen[0])) * 180/math.pi )
	else:
		angle = 90
	print(F"Angle is{angle}")
	cv2.putText(frame_back, f"Angle: {angle}", (center_of_the_screen[0]-10, center_of_the_screen[1]-10), cv2.FONT_HERSHEY_SIMPLEX, .5, (0,255, 255), 1, cv2.LINE_AA)
	
	x4,y4,x1,y1 = boxes[0]
	tl = (x1, y1)
	tr = (x4, y1)
	br = (x4, y4)
	bl = (x1, y4)
	#(tl, tr, br, bl) = boxes[0]
	(tlblX, tlblY) = midpoint(tl, bl)
	(trbrX, trbrY) = midpoint(tr, br)
	 
	
	D = euclidean_distance((tlblX, tlblY), (trbrX, trbrY))
	ref = D/5
	
	distance_to_center =  euclidean_distance((center_of_the_screen[0], b_box_rec[1]), b_box_rec)/ref
	print(f"Distance of orginal: {ref} -- and to the object:{distance_to_center}")
	mi_points_of_line = midpoint((center_of_the_screen[0], b_box_rec[1]), b_box_rec)
	cv2.putText(frame_back, "{:.1f}in".format(distance_to_center), (int(mi_points_of_line[0]), int(mi_points_of_line[1]- 10)),
			cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0,255, 255), 2)
	
	
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


	
	
	
	

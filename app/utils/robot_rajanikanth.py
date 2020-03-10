from app.utils.video_stream import StreamThreaded
from app.utils.robot_custome_exception import ConeColorMissing
import cv2
from threading import Thread
from app.utils.find_objects import FindCones
import numpy as np
from easygopigo3 import EasyGoPiGo3
import time
import logging

'''
@newfield team: Venku Buragadda
'''


class NavigateRajani:
    '''
    Navigating the robot
    @author: Venku Buragadda
    '''

    def __init__(self, home_cone_color=None, destination_cone_color="red", show_video=False):
        self.log = logging.getLogger("main.navigation")
        self.camera = StreamThreaded()
        self.home_cone_color = home_cone_color
        self.camera.start()

        self.gopi_easy = EasyGoPiGo3()
        self.show_video = show_video
        self.cv2_window = None

        self.hard_stop = False

        self.cone_data = None
        self.find_cone_obj = FindCones(color=destination_cone_color)

        # This will open a new cv2 to show the video feed in a different thread.
        if self.show_video:
            self.cv2_window = Thread(target=self.show_video_feed, args=())
            print("thread-2", self.cv2_window)
            self.cv2_window.start()
            print("Starting thread-2")

    def find_cone(self, cone_color=None):
        turn_deg_list = [0, 20, -40, 60, -80, 100, -120, 140, -160, 180, -200, 220, -240, 260, -280, 300, -320, 340,
                         -360]

        if cone_color:
            while True:
                for turn_to_degree in turn_deg_list:
                    print("Checking Degree", turn_to_degree)
                    self.log.info(f"Moving to the following degree {turn_to_degree}")
                    self.gopi_easy.turn_degrees(turn_to_degree)
                    time.sleep(2)
                    frame = self.camera.read()
                    flag, frame_back, total_cones, boxes, cones_data = self.get_cone_coordinates(frame)
                    if total_cones > 0:
                        self.cone_data = cones_data
                        return self
                else:
                    break

        else:
            raise ConeColorMissing("Cone color is required here and is missing")

    def get_cone_coordinates(self, frame):
        flag, frame_back, total_cones, boxes, cones_data = self.find_cone_obj.find_cone(frame)
        #print("Find code class called: ", total_cones)
        return flag, frame_back, total_cones, boxes, cones_data

    def center_the_cone(self, height_range=(280, 360), precise=False):

        while True:
            time.sleep(2)
            frame = self.camera.read()
            flag, frame_back, total_cones, boxes, cones_data = self.get_cone_coordinates(frame)

            if total_cones > 0:
                cone_boudning_box = cones_data['cone-0']['bouding_box_center']
                center_of_screen_coord, horiztl_line_lower_left_coord, horiztl_line_lower_right_coord, horiztl_line_upper_left_coord, \
                horiztl_line_upper_right_coord, left_bottom_bound_line_coord, left_top_bound_line_coord, right_bottom_bound_line_coord, \
                rigth_top_bound_line_coord, width = NavigateRajani.screen_coordinates(frame)
                print(f"Cone data: {cone_boudning_box}")
                print(f"Coordinates: ", left_top_bound_line_coord, rigth_top_bound_line_coord)
                steer = 1
                if precise:
                    center_boundary_left_right_width = (left_top_bound_line_coord[0], rigth_top_bound_line_coord[0])
                    self.gopi_easy.set_eye_color((255,0,255))
                else:
                    center_boundary_left_right_width = (left_top_bound_line_coord[0]-40, rigth_top_bound_line_coord[0]+40)
                    steer = 3
                    self.gopi_easy.set_eye_color((0,255,127))
                print(f"Center Boundary", center_boundary_left_right_width)

                if not center_boundary_left_right_width[0] <= cone_boudning_box[0] <= center_boundary_left_right_width[1]:
                    print("Centring Cone")
                    if cone_boudning_box[0] > height_range[1]:
                        # move right
                        print(F"Moving right")
                        self.gopi_easy.open_left_eye()
                        self.gopi_easy.steer(steer, 0)
                        time.sleep(1)
                        self.gopi_easy.stop()
                        self.gopi_easy.close_left_eye()

                    if cone_boudning_box[0] < height_range[1]:
                        # move left
                        print(F"Moving left")
                        self.gopi_easy.open_right_eye()

                        self.gopi_easy.steer(0, steer)
                        time.sleep(1)
                        self.gopi_easy.close_right_eye()
                        self.gopi_easy.stop()
                else:
                    # getting update cone data after the robot is centered.
                    self.cone_data = cones_data
                    return self

    def move_towards_the_cone(self, drive_inches=4):

        while True:
            self.center_the_cone()
            frame = self.camera.read()
            flag, frame_back, total_cones, boxes, cones_data = self.get_cone_coordinates(frame)
            if total_cones:
                cone_bottom_mid_point = self.get_cone_bottom_mid_point(boxes)
                
                # Cone rectangel box bottom line mid point
                cone_lower_rec_boundary_mid_point_height = cone_bottom_mid_point[1]
                center_of_screen_coord, horiztl_line_lower_left_coord, horiztl_line_lower_right_coord, horiztl_line_upper_left_coord, horiztl_line_upper_right_coord, \
                left_bottom_bound_line_coord, left_top_bound_line_coord, right_bottom_bound_line_coord, rigth_top_bound_line_coord, width = NavigateRajani.screen_coordinates(
                    frame)
                
                # Screen bottom box line. top(upper) bottom(lower) left coordinates of Y

                bottom_boundary_upper_lower_height = (
                    horiztl_line_upper_left_coord[1] + 20, horiztl_line_lower_left_coord[1] + 20)

                if not bottom_boundary_upper_lower_height[0] <= cone_lower_rec_boundary_mid_point_height <= \
                       bottom_boundary_upper_lower_height[1]:
                    if bottom_boundary_upper_lower_height[0] > cone_lower_rec_boundary_mid_point_height:
                        self.gopi_easy.drive_inches(drive_inches)
                    else:
                        self.gopi_easy.drive_inches(-drive_inches)
                elif horiztl_line_lower_left_coord[1] <= cone_lower_rec_boundary_mid_point_height:
                    self.gopi_easy.drive_inches(-1)                
                else:
                    self.center_the_cone(precise=True)
                    return self
                self.center_the_cone(precise=False)
                
    def circle_the_cone(self, carpet=False):
        
        self.gopi_easy.turn_degrees(-90)
        if carpet:
            self.gopi_easy.orbit(480, 60)
        else:
            self.gopi_easy.orbit(90, 60)
            time.sleep(2)
            self.camera.camera.capture('foo.jpg')
            self.gopi_easy.orbit(90, 60)
            time.sleep(2)
            #self.camera.read().capture('/home/pi/foo.jpg', use_video_port=True)
            self.gopi_easy.orbit(90, 60)
            self.gopi_easy.orbit(90, 60)
        self.gopi_easy.turn_degrees(90)
        self.gopi_easy.turn_degrees(220)

    def get_cone_bottom_mid_point(self, boxes):
        x, y, w, h = boxes[0]
        x1, y1, x4, y4 = (x, y, x + w, y + h)
        # tl = (x1, y1)
        # tr = (x4, y1)
        br = (x4, y4)
        bl = (x1, y4)
        # # (tl, tr, br, bl) = boxes[0]
        # (tlblX, tlblY) = NavigateRajani.midpoint(tl, bl)
        # (trbrX, trbrY) = NavigateRajani.midpoint(tr, br)
        rect_bottom_mind_point = NavigateRajani.midpoint(bl, br)
        return rect_bottom_mind_point

    @staticmethod
    def midpoint(ptA, ptB):
        return (ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5

    def show_video_feed(self):
        while True:
            frame = self.camera.read()
            if not (frame is None):
                frame = NavigateRajani.center_boundaries(frame)
                center_of_screen_coord, horiztl_line_lower_left_coord, horiztl_line_lower_right_coord, horiztl_line_upper_left_coord, horiztl_line_upper_right_coord, \
                left_bottom_bound_line_coord, left_top_bound_line_coord, right_bottom_bound_line_coord, rigth_top_bound_line_coord, width = NavigateRajani.screen_coordinates(
                    frame)

                cv2.line(frame, left_top_bound_line_coord, left_bottom_bound_line_coord, [232, 206, 190], 1)
                cv2.line(frame, rigth_top_bound_line_coord, right_bottom_bound_line_coord, [232, 206, 190], 1)

                cv2.line(frame, rigth_top_bound_line_coord, right_bottom_bound_line_coord, [232, 206, 190], 1)

                # Center vertical line
                cv2.line(frame, (center_of_screen_coord[0], 0), (center_of_screen_coord[0], width), [0, 255, 0], 1)

                cv2.line(frame, horiztl_line_upper_left_coord, horiztl_line_upper_right_coord, [200, 90, 60], 1)
                cv2.line(frame, horiztl_line_lower_left_coord, horiztl_line_lower_right_coord, [200, 90, 60], 1)

                cv2.putText(frame, f"Upper: {horiztl_line_upper_left_coord},{horiztl_line_upper_right_coord}",
                            horiztl_line_upper_left_coord, cv2.FONT_HERSHEY_SIMPLEX, .5,
                            (0, 255, 255), 1, cv2.LINE_AA)
                cv2.putText(frame, f"Lower: {horiztl_line_lower_left_coord},{horiztl_line_lower_right_coord}",
                            horiztl_line_lower_left_coord, cv2.FONT_HERSHEY_SIMPLEX, .5,
                            (0, 255, 255), 1, cv2.LINE_AA)

                # cv2.putText(frame, f"Temp:{temperature}", (50, 30), cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 255, 255), 1,
                #             cv2.LINE_AA)
                flag, frame_back, total_cones, boxes, cones_data = self.get_cone_coordinates(frame)
                if total_cones:
                    rect_bottom_mind_point = self.get_cone_bottom_mid_point(boxes)
                    cv2.putText(frame_back, f"bottom: {rect_bottom_mind_point}",
                                (int(rect_bottom_mind_point[0]), int(rect_bottom_mind_point[1])), cv2.FONT_HERSHEY_SIMPLEX,
                                .5, (0, 255, 255), 1, cv2.LINE_AA)
                    frame = frame_back

                cv2.imshow("Video Feed", frame)
                if self.hard_stop:
                    break
                key = cv2.waitKey(1) & 0xFF

    @staticmethod
    def screen_coordinates(frame):
        height, width, ch = frame.shape
        center_of_screen_coord = (width // 2, height // 2)
        # center boundaries
        left_top_bound_line_coord, left_bottom_bound_line_coord = (width - center_of_screen_coord[0] - 20, 0), (
            width - center_of_screen_coord[0] - 20, height)
        rigth_top_bound_line_coord, right_bottom_bound_line_coord = (width - center_of_screen_coord[0] + 20, 0), (
            width - center_of_screen_coord[0] + 20, height)
        # bottom boundaries
        horiztl_line_upper_left_coord, horiztl_line_upper_right_coord = (0, height - 100), (width, height - 100)
        horiztl_line_lower_left_coord, horiztl_line_lower_right_coord = (0, height - 50), (width, height - 50)
        return center_of_screen_coord, horiztl_line_lower_left_coord, horiztl_line_lower_right_coord, \
               horiztl_line_upper_left_coord, horiztl_line_upper_right_coord, left_bottom_bound_line_coord, \
               left_top_bound_line_coord, right_bottom_bound_line_coord, rigth_top_bound_line_coord, width

    @staticmethod
    def center_boundaries(frame):

        he, wi, ch = frame.shape
        center_of_the_screen = (wi // 2, he // 2)
        cv2.circle(frame, center_of_the_screen, 5, [255, 0, 0], -1)
        cv2.line(frame, center_of_the_screen, (center_of_the_screen[0] + 30, center_of_the_screen[1]), [0, 255, 0], 3)

        left_top, left_bottom = (wi - center_of_the_screen[0] - 40, 0), (wi - center_of_the_screen[0] - 40, he)
        right_top, right_bottom = (wi - center_of_the_screen[0] + 40, 0), (wi - center_of_the_screen[0] + 40, he)

        # print(F"Left: {left_top},{left_bottom} and Right: {right_top}, {right_bottom}")

        cv2.line(frame, left_top, left_bottom, [232, 206, 190], 1)
        cv2.line(frame, right_top, right_bottom, [232, 206, 190], 1)
        return frame

    def __enter__(self):
        self.log.info("Context open")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.log.info("Destroying all the resources")
        self.hard_stop = True
        self.camera.stop()
        if self.show_video:
            self.cv2_window.join()
        cv2.destroyAllWindows()

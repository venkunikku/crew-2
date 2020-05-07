from app.utils import robot_rajanikanth  # video_stream, VideoStreamMulProcess,
import cv2
import time
import traceback
import atexit
import os
import logging
from app.post_results.robo_client import connection

import logging
import traceback

main_logger = logging.getLogger('gpg')
main_logger.setLevel(logging.DEBUG)
fname = 'gopigo.log'  # Any name for the log file

# Create the FileHandler object. This is required!
fh = logging.FileHandler(fname, mode='w')
fh.setLevel(logging.INFO)  # Will write to the log file the messages with level >= logging.INFO

# The following row is strongly recommended for the GoPiGo Test!
fh_formatter = logging.Formatter('%(relativeCreated)d,%(name)s,%(message)s')
fh.setFormatter(fh_formatter)
main_logger.addHandler(fh)

# The StreamHandler is optional for you. Use it just to debug your program code
sh = logging.StreamHandler()
sh_formatter = logging.Formatter('%(relativeCreated)8d %(name)s %(levelname)s %(message)s')
sh.setLevel(logging.DEBUG)
sh.setFormatter(sh_formatter)
main_logger.addHandler(sh)
main_logger.debug('Logger started')  # This debug message will be handled only by StreamHendler


def clean_up():
    global cam
    print("Cleaning up using the hook", cam)
    cam.stop()


def send_log_to_server():
    HOST, PORT = 'datastream.ilykei.com', 30078
    login = 'venku@uchicago.edu'
    password = 'Bne3SqJG'
    split_id = 19
    filename = 'gopigo.log'
    c = connection(HOST, PORT, login, password, split_id, filename)
    print(f"Logs Sent to the server: {c}")


if __name__ == '__main__':
    mic_logger = logging.getLogger('gpg.mic')
    mic_logger.info('Start')

    try:
        #with robot_rajanikanth.NavigateRajani(show_video=True, inference=True, destination_cone_color="purple") as test:
        # test = robot_rajanikanth.NavigateRajani(show_video=True, inference=True, destination_cone_color="purple")
        # test.find_cone(cone_color="red").center_the_cone().move_towards_the_cone(
        #        drive_inches=8).circle_the_cone().there_is_nothing_like_home()
        # with robot_rajanikanth.NavigateRajani(show_video=True, inference=True, destination_cone_color="green") as test:
        #     test.find_cone(cone_color="red").center_the_cone().move_towards_the_cone(
        #         drive_inches=8).circle_the_cone().there_is_nothing_like_home()
            #test.center_the_cone()
            # print(test.circle_the_cone())
            # print(test.infer_image(image_path='/home/pi/Desktop/botte.jpg'))
            # print(test.there_is_nothing_like_home())
        cones = ["green", "purple"]
        with robot_rajanikanth.NavigateRajani(show_video=True, inference=True) as nav:
            for c in cones:
                nav.create_objects(destination_cone_color=c).find_cone().center_the_cone().\
                    move_towards_the_cone(drive_inches=8).circle_the_cone().there_is_nothing_like_home()
                print(F"Completed circling {c} world!!")
            #input("press key to stop")

    except:
        print(traceback.print_exc())

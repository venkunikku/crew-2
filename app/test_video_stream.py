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
import pyaudio
import numpy as np
import numpy.fft as fft
import time

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
    CHUNK = 4096  # number of data points to read at a time
    RATE = 44100  # time resolution of the recording device (Hz)
    STREAM_SECONDS = 30

    p = pyaudio.PyAudio()  # start the PyAudio class
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True,
                    frames_per_buffer=CHUNK)  # uses default input device

    frequencies = []
    try:
        while True:
            # create a numpy array holding a single read of audio data
            for i in range(0, int(RATE / CHUNK * STREAM_SECONDS)):  # to it a few times just to see
                data = np.fromstring(stream.read(CHUNK), dtype=np.int16)
                spectrum = fft.fft(data)
                freqs = fft.fftfreq(len(spectrum))
                l = len(data)

                # imax = index of first peak in spectrum
                imax = np.argmax(np.abs(spectrum))
                fs = freqs[imax]

                freq = (imax * fs / l) * 1000000
                # frequencies.append(freq)
                # print(freq)
                if freq > 1500:

                    # import record_noise.py
                    #
                    stream.stop_stream()
                    stream.close()
                    p.terminate()
                    # cones = ["green", "purple", "red"]
                    cones = ["green", "purple", "yellow"]
                    print(f"Got Signal to explore the world!!!")
                    with robot_rajanikanth.NavigateRajani(show_video=False, inference=True, is_audio_inference=True) as nav:
                        # for c in cones:
                        #     nav.create_objects(destination_cone_color=c).find_cone().center_the_cone(). \
                        #         move_towards_the_cone(drive_inches=8).circle_the_cone().there_is_nothing_like_home()
                        c = cones[0]
                        nav.create_objects(destination_cone_color=c).find_cone().center_the_cone(). \
                                move_towards_the_cone(drive_inches=8).circle_the_cone().there_is_nothing_like_home()
                        # c = cones[1]
                        # nav.create_objects(destination_cone_color=c).find_cone().center_the_cone(). \
                        #     move_towards_the_cone(drive_inches=8).circle_the_cone().there_is_nothing_like_home()
                        # c = cones[2]
                        # nav.create_objects(destination_cone_color=c).find_cone().center_the_cone(). \
                        #     move_towards_the_cone(drive_inches=8).circle_the_cone(degrees=60, drive_inches_back_by=12).there_is_nothing_like_home()

                        print(F"Completed circling {c} world!!")
                        # input("press key to stop")
                    break
    except:
        print(F"Completed circling {c} world!!")
        print(traceback.print_exc())

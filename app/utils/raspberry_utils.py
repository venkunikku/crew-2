import os


def processor_temperature(self):
    temp = os.popen("/opt/vc/bin/vcgencmd measure_temp").readline()
    return temp.replace("temp=", "")

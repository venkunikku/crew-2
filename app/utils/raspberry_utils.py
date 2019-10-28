import os


def processor_temperature():
    temp = os.popen("/opt/vc/bin/vcgencmd measure_temp").readline()
    return float(temp.replace("temp=", "").replace("'C\n",""))

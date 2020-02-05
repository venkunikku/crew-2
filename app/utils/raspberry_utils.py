import os
from easygopigo3 import EasyGoPiGo3

def processor_temperature():
    temp = os.popen("/opt/vc/bin/vcgencmd measure_temp").readline()
    return float(temp.replace("temp=", "").replace("'C\n",""))


class Utils:
    
    def __init__(self):
        self.easy = EasyGoPiGo3()
    
    def get_temperature(self):
        temp = os.popen("/opt/vc/bin/vcgencmd measure_temp").readline()
        return float(temp.replace("temp=", "").replace("'C\n",""))
    def get_gopigo_details(self):
        volt = self.easy.volt()
        details = f"Volts:{volt}"
        return details
        
        

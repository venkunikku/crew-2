from easygopigo3 import EasyGoPiGo3

def turn_servo():
	easy = EasyGoPiGo3()
	servo = easy.init_servo("SERVO2")
	servo.rotate_servo(-90)
	print(servo)

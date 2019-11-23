import easygopigo3
import easypicamera
import time

GPG = easygopigo3.EasyGoPiGo3()
GPG.reset_all()

GPG.forward()
time.sleep(3)
GPG.stop()

# Square
length = 30
for i in range(4):
    GPG.drive_cm(length)
    GPG.turn_degrees(90)
    GPG.blinker_on(1)
GPG.blinker_off(1)

# Cricle
GPG.orbit(180,20)
print("Orbit completed")
GPG.turn_degrees(180)
print("180 degree turn completed")
GPG.orbit(-180, 20)
print("-180 Orbit completed")
GPG.turn_degrees(180)
print("180 degree turn completed")


GPG.turn_degrees(90)
GPG.orbit(360, 30)
GPG.turn_degrees(-90)


GPG.set_speed(200)
GPG.turn_degrees(90)
GPG.orbit(360,20)
GPG.turn_degrees(-90)
GPG.set_speed(300)
print(GPG.get_speed())
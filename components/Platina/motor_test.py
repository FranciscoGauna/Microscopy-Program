from motor import Motor, get_available_motors
from lantz.core.log import log_to_screen, DEBUG
from time import sleep

log_to_screen(DEBUG)
motor = Motor()
available_motors = get_available_motors()
motor.open_motor(list(available_motors.values())[0])
#motor.open_motor("virtual")
motor.log_info("Started")
for i in range(1):
    sleep(1)
motor.log_info("Finished")
motor.close_motor()

from motor import Motor

motor = Motor()
motor.open_motor("virtual")
motor.antiplay_enabled = False
motor.close_motor()

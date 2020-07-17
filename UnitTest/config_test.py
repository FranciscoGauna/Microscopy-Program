from Drivers.Motor.MotorDriver import Motor, get_available_motors

motor = Motor()

config_file = open("8MTF-75LS05.cfg")
motores = get_available_motors()
motor.open_motor(motores["b'8CMA06-25_15'"], config_file)
print(motor.move_to(1000))
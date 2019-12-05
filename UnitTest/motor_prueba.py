import os
import sys
import time
from ctypes import byref

cur_dir = os.path.abspath(os.path.dirname(__file__))
ximc_dir = os.path.join(cur_dir, "..", "ximc")
ximc_package_dir = os.path.join(ximc_dir, "crossplatform", "wrappers", "python")
sys.path.append(ximc_package_dir)  # add ximc.py wrapper to python path

arch_dir = "win64"
libdir = os.path.join(ximc_dir, arch_dir)
os.environ["Path"] = libdir + ";" + os.environ["Path"]  # add dll

from ximc.crossplatform.wrappers.python.pyximc import lib, feedback_settings_t, EnumerateFlags, controller_name_t, Result, move_settings_t, get_position_t, FeedbackType

lib.set_bindy_key(os.path.join(ximc_dir, "win32", "keyfile.sqlite").encode("utf-8"))

probe_flags = EnumerateFlags.ENUMERATE_PROBE + EnumerateFlags.ENUMERATE_NETWORK
enum_hints = b"addr=192.168.0.1,172.16.2.3"

# Set up device
motors = {}
dev_enum = lib.enumerate_devices(probe_flags, enum_hints)
dev_count = lib.get_device_count(dev_enum)
controller_name = controller_name_t()
for dev_ind in range(0, dev_count):
    enum_name = lib.get_device_name(dev_enum, dev_ind)
    result = lib.get_enumerate_device_controller_name(dev_enum, dev_ind, byref(controller_name))
    if result == Result.Ok:
        motors[str(controller_name.ControllerName)] = enum_name

device_id = lib.open_device(motors[list(motors.keys())[0]])

feedback_settings = feedback_settings_t()
result = lib.get_feedback_settings(device_id, byref(feedback_settings))
if result != Result.Ok:
    raise Exception
feedback_settings.FeedbackType = FeedbackType.FEEDBACK_ENCODER
result = lib.set_feedback_settings(device_id, byref(feedback_settings))
if result != Result.Ok:
    raise Exception
print("Setted feedback setting")

# Set device to zero
result = lib.command_zero(device_id)
if result != Result.Ok:
    raise Exception
x_pos = get_position_t()
result = lib.get_position(device_id, byref(x_pos))
if result != Result.Ok:
    raise Exception
print("Position: {0} steps, {1} microsteps".format(x_pos.Position, x_pos.uPosition))


# Move by 3 seconds
result = lib.command_move(device_id, 200, 0)
if result != Result.Ok:
    raise Exception
time.sleep(0.5)
result = lib.get_position(device_id, byref(x_pos))
if result != Result.Ok:
    raise Exception
print("Position: {0} steps, {1} microsteps".format(x_pos.Position, x_pos.uPosition))
time.sleep(2)

# Print position
result = lib.get_position(device_id, byref(x_pos))
if result != Result.Ok:
    raise Exception
print("Position: {0} steps, {1} microsteps".format(x_pos.Position, x_pos.uPosition))

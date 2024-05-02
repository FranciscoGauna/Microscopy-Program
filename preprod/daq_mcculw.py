from time import sleep

from mcculw import ul
from mcculw.enums import ULRange
from mcculw.ul import ULError
from mcculw.device_info import DaqDeviceInfo


board_num = 0
ai_range = ULRange.BIP5VOLTS
laser_channel = 2


try:
    devinfo = DaqDeviceInfo(board_num)
    on_value = ul.from_eng_units(0, ULRange.BIP10VOLTS, 2)
    ao_info = devinfo.get_ao_info()
    print(ao_info)
    print(ao_info.resolution)
    print(ao_info.supported_ranges)
    print(on_value)
    ul.a_out(board_num, laser_channel, ULRange.BIP10VOLTS, on_value)

    for i in range(60):
        suma = ul.a_in(board_num, 0, ai_range)
        v_suma = ul.to_eng_units(board_num, ai_range, suma)
        foco = ul.a_in(board_num, 0, ai_range)
        v_foco = ul.to_eng_units(board_num, ai_range, foco)
        refl = ul.a_in(board_num, 0, ai_range)
        v_ref = ul.to_eng_units(board_num, ai_range, refl)
        print(f"Suma: {v_suma}; EFoco: {v_foco}; Reflectancia: {v_ref}")
        sleep(0.1)
    on_value = ul.from_eng_units(0, ULRange.BIP10VOLTS, 0)
    print(on_value)
    ul.a_out(board_num, laser_channel, ULRange.BIP10VOLTS, on_value)
except ULError as e:
    # Display the error
    print("A UL error occurred. Code: " + str(e.errorcode)
          + " Message: " + e.message)
finally:
    pass
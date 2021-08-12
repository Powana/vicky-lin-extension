import time
import keyboard as newkb
import pynput as pynput
from ucanlintools import LUC, LINFrame
from ldfparser import parseLDF, LinFrame, LDF  # https://c4deszes.github.io/ldfparser/frames.html
from pynput.keyboard import Key, Listener
from serial.serialutil import SerialException
from win32gui import GetWindowText, GetForegroundWindow

import signal_handlers.ets2_sig_handlers
from signal_handlers import signal_callbacks

COM_PORT = "COM3"
# Disables ets2 check and print statements
DEBUG = True

# When adding a new lin bus to Vicky, add the LDF here. LDFs can be found at:
# http://esw-artifactory.got.volvo.net/list/esw-release/com/volvo/esw/com_matrix/lin/
ldfs = [
    parseLDF("LDFs/LIN23_VMCU-T2_1.3.0-postfix.ldf"),
    parseLDF("LDFs/LIN14_HMIIOM-T2_1.20.0-postfix.ldf")
]

merged_ldf = LDF()
for ldf in ldfs:
    merged_ldf.signals.extend(ldf.signals)
    merged_ldf.frames.extend(ldf.frames)

print([f for f in merged_ldf.frames])
quit()

# After adding the LDF, add the message containing the signals for the desired LIN nodes here.
request_messages = [
    merged_ldf.frame("SM1toVMCU_L23"),  # Stalk module
    merged_ldf.frame("GLU5toVMCU_L23"),  # Gearstick
    merged_ldf.frame("SWS6toHMIIOM_L14")  # Steering wheel buttons
]


def log(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


def handle_rx_data(frame):  # Unused
    # data attr is set on rx frames
    log("RX: ID=", frame.id, " DATA=", merged_ldf.frame(frame.id).parse_raw(frame.data), sep="")


def handle_new_rx_data(frame: LINFrame):
    if not DEBUG and "Euro Truck Simulator 2" not in GetWindowText(GetForegroundWindow()):
        return

    # data attr is set on rx frames, don't worry about any warnings
    ldf_frame = merged_ldf.frame(frame.id)
    if ldf_frame is None:
        log("! Frame with id:", str(frame.id), "could not be found in the ldf")
        return

    data = ldf_frame.parse_raw(frame.data)
    log("NEW RX: ID=", frame.id, " DATA=", data, " (NEW DATA)", sep="")

    for sig_name, sig_str_value in data.items():
        if sig_name in signal_callbacks:
            signal_callbacks[sig_name](sig_str_value)


if __name__ == '__main__':

    print("\n"
          "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n"
          "@@       DO NOT KILL THIS SCRIPT!      @@\n"
          "@@        PRESS ESC TO STOP IT!        @@\n"
          "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n")

    time.sleep(4)

    print("Press")

    signal_handlers.ets2_sig_handlers.hndl_sw_mute_btn(1)
    #signal_handlers.main_handler.keyb.press(pynput.keyboard.KeyCode().from_char("e"))

    time.sleep(0.2)


    # newkb.press()
    signal_handlers.ets2_sig_handlers.hndl_sw_mute_btn(0)
    #signal_handlers.main_handler.keyb.release(pynput.keyboard.KeyCode().from_char("e"))

    print("Released")

    while True:
        newkb.wait("ESC")
        if not DEBUG and "Euro Truck Simulator 2" not in GetWindowText(GetForegroundWindow()):
            print("ESCAPED")
            quit()



    # Collect events until released

#    with Listener(on_release=on_release) as listener:
 #       listener.join()
  #      log("Quitting")
   #     quit(0)

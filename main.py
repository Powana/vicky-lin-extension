# https://c4deszes.github.io/ldfparser/frames.html
# https://pyserial.readthedocs.io/en/latest/shortintro.html
from ucanlintools import LUC, LINFrame
from ldfparser import parseLDF, LinFrame
from pynput.keyboard import Key, Listener
from signal_handlers import signal_callbacks

from serial.serialutil import SerialException
from win32gui import GetWindowText, GetForegroundWindow

# Disables ets2 check and print statements
DEBUG = True

# When adding a new lin bus to Vicky, add the LDF here. LDFs can be found at:
# http://esw-artifactory.got.volvo.net/list/esw-release/com/volvo/esw/com_matrix/lin/
VMCU_ldf = parseLDF("LDFs/LIN23_VMCU-T2_1.3.0-postfix.ldf")
HMIIOM_ldf = parseLDF("LDFs/LIN14_HMIIOM-T2_1.20.0-postfix.ldf")
VMCU_ldf.frames += HMIIOM_ldf.frames
VMCU_ldf.signals += HMIIOM_ldf.signals
print([f.name for f in VMCU_ldf.frames])

# After adding the LDF, add the message containing the signals for the desired LIN nodes here.
request_messages = [
    VMCU_ldf.frame("SM1toVMCU_L23"),  # Stalk module
    HMIIOM_ldf.frame("SWS6toHMIIOM_L14")  # Steering wheel buttons
]


def log(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


def handle_rx_data(frame):  # Unused
    # data attr is set on rx frames
    log("RX: ID=", frame.id, " DATA=", VMCU_ldf.frame(frame.id).parse_raw(frame.data), sep="")


def handle_new_rx_data(frame: LINFrame):
    if not DEBUG and "Euro Truck Simulator 2" not in GetWindowText(GetForegroundWindow()):
        return
    print("NEW FRAME ID:", frame.id)
    # data attr is set on rx frames, donät worry about any warnings
    ldf_frame = HMIIOM_ldf.frame(frame.id)
    if ldf_frame is None:
        log("! Frame with id:", str(frame.id), "could not be found in the ldf")
        return

    data = ldf_frame.parse_raw(frame.data)
    log("RX: ID=", frame.id, " DATA=", data, " (NEW DATA)", sep="")

    for sig_name, sig_str_value in data.items():
        if sig_name in signal_callbacks:
            signal_callbacks[sig_name](sig_str_value)


def set_custom_timing(master: LUC, frame: LinFrame, delay):
    command = 'R0' + hex(frame.frame_id).replace("0x", "").rjust(2, "0") + \
              "00" + str(delay) + \
              "0" + str(frame.length) + '\r'  # Adding a zero before the length seemingly fixes stuff
    master.flushData(command.encode())
    ret = lin.ser.readline()
    log("Custom timing for frame with ID:", frame.frame_id, " returned:", ret, "\nCommand was", command)
    return ret == b"Z\r"


if __name__ == '__main__':

    # config_lines[2]: "device joy `di8.'{E7D4CFE0-D827-11EB-8004-444553540000}|{BEAD1234-0000-0000-0000-504944564944}'`"
    # Creates and opens a serial connection to the Lin USB Converter
    try:
        lin = LUC("COM3")
    except SerialException as e:
        print("Something went wrong:", e)
        print("Try reconnecting the LUC.")
        exit(-1)

    # Called every time a message with data differing from the previous data is recieved.
    lin.set_new_frame_rx_handler(handle_new_rx_data)

    # If killed improperly, LUC gets messed up, and the enxt time we try to open as master it fails.
    if lin.openAsMaster() is False:
        print("LUC was not properly disabled, try again.")
        print("Disabled LUC:", lin.disable())
        del lin
        exit(-1)

    print("\n"
          "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n"
          "@@       DO NOT KILL THIS SCRIPT!      @@\n"
          "@@        PRESS ESC TO STOP IT!        @@\n"
          "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n")

    for msg in request_messages:
        lin.addReceptionFrameToTable(msg.frame_id, msg.length)

    print("Low speed (9600) enabled:", lin.lowSpeed())
    print("Custom timing stalks:", set_custom_timing(lin, request_messages[0], 15))  # todo automize
    print("Custom timing buttons:", set_custom_timing(lin, request_messages[1], 30))  # todo automize
    print("LIN bus enabled:", lin.enable())

    # ----- Debug Stuff ------- #
    """
    lin.flushData(b'r00c4\r')
    log("add c to recption table:", lin.ser.readline().decode("utf-8") == 'z\r')

    lin.flushData(b'v\r')
    log("test:", lin.ser.readline().decode("utf-8"))

    log("lowSpeed:", lin.lowSpeed())
    log(lin.addReceptionFrameToTable(SWS6_to_HMIIOM.frame_id, SWS6_to_HMIIOM.length))
    # todo: look at custom timing with big T or big R command and lin.flushData

    lin.flushData(b'R00c00154\r')  # todo: sometimes this fucks up?
    log("timing:", lin.ser.readline())
    # todo: documentation, how to set up etc.
    # todo maybe: script for adding joy.b# to controls.sii
    # ----- End Debug Stuff ------- #
    """


    def del_lin(*args):
        global lin
        log("Deleting lin")
        lin.disable()
        del lin


    def on_release(key):
        if key == Key.esc:
            del_lin()
            return False


    # Collect events until released
    with Listener(on_release=on_release) as listener:
        listener.join()
        log("Quitting")
        quit(0)

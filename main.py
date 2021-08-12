import keyboard as keyboard
from ucanlintools import LUC, LINFrame
from ldfparser import parseLDF, LinFrame, LDF  # https://c4deszes.github.io/ldfparser/frames.html
from serial.serialutil import SerialException
from win32gui import GetWindowText, GetForegroundWindow

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

    for sig_name, sig_int_value in data.items():
        if sig_name in signal_callbacks:
            signal_callbacks[sig_name](sig_int_value)


def set_custom_timing(master: LUC, frame: LinFrame, delay):
    command = 'R0' + hex(frame.frame_id).replace("0x", "").rjust(2, "0") + \
              "00" + str(delay) + \
              "0" + str(frame.length) + '\r'  # Adding a zero before the length seemingly fixes stuff
    master.flushData(command.encode())
    ret = lin.ser.readline()
    log("Custom timing for frame with ID:", frame.frame_id, "returned:", ret, "Command was", command)
    return ret == b"Z\r"


if __name__ == '__main__':

    # config_lines[2]: "device joy `di8.'{E7D4CFE0-D827-11EB-8004-444553540000}|{BEAD1234-0000-0000-0000-504944564944}'`
    # Creates and opens a serial connection to the Lin USB Converter
    try:
        lin = LUC(COM_PORT)
    except SerialException as e:
        print("Something went wrong:", e)
        print("Make sure you're connecting to the correct COM port, or try reconnecting the LUC.")
        exit(-1)

    print(signal_callbacks)

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
        log("Added", hex(msg.frame_id), msg.name, "to reception table: ", lin.addReceptionFrameToTable(msg.frame_id, msg.length))

    print("Low speed (9600) enabled:", lin.lowSpeed())
    print("Custom timing stalks:", set_custom_timing(lin, request_messages[0], 15))  # todo automize
    print("Custom timing buttons:", set_custom_timing(lin, request_messages[1], 10))  # todo automize
    print("Custom timing gears:", set_custom_timing(lin, request_messages[2], 30))  # todo automize
    print("LIN bus enabled:", lin.enable())

    # ----- Debug Stuff ------- #
    """
    lin.flushData(b'r00c4\r')
    log("add c to reception table:", lin.ser.readline().decode("utf-8") == 'z\r')

    lin.flushData(b'v\r')
    log("test:", lin.ser.readline().decode("utf-8"))

    lin.flushData(b'R00c00154\r')  
    log("timing:", lin.ser.readline())
    # todo: documentation, how to set up etc.
    # todo maybe: script for adding joy.b# to controls.sii
    # ----- End Debug Stuff ------- #
    """

    while True:
        keyboard.wait("esc")  # Block until escape
        if DEBUG or "Euro Truck Simulator 2" not in GetWindowText(GetForegroundWindow()):
            log("De-init LUC")
            lin.disable()
            del lin
            exit()

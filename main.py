# https://c4deszes.github.io/ldfparser/frames.html
# https://pyserial.readthedocs.io/en/latest/shortintro.html
from ucanlintools import LUC, LINFrame
from ldfparser import parseLDF, LinFrame
import atexit
from pynput.keyboard import Key, Listener
from signal_handlers import signal_callbacks
# import signal_handlers as sh

from win32gui import GetWindowText, GetForegroundWindow


ldf = parseLDF("LDFs/LIN23_VMCU-T2_1.3.0-postfix.ldf")
request_frame = ldf.frame('VMCUtoSlaves_L23')
request_data = request_frame.raw({"BacklightCmd_ISig_31": 0,
                                  "FuncIndIlluminationLevel_ISig_31": 1,
                                  "LIN_Rainsensor_Indication": 1})
slave_frame = ldf.frame("SM1toVMCU_L23")

ldf2 = parseLDF("LDFs/LIN14_HMIIOM-T2_1.20.0-postfix.ldf")
btns_slave_frame = ldf2.frame("SWS6toHMIIOM_L14")


def handle_rx_data(frame):
    # data attr is set on rx frames
    print("RX: ID=", frame.id, " DATA=", ldf.frame(frame.id).parse_raw(frame.data), sep="")


def handle_new_rx_data(frame: LINFrame):
    print("poopo")
    #if "Euro Truck Simulator 2" not in GetWindowText(GetForegroundWindow()):
    #    return

    # data attr is set on rx frames
    data = ldf.frame(frame.id).parse_raw(frame.data)
    print("RX: ID=", frame.id, " DATA=", data, " (NEW DATA)", sep="")
    # todo: decide whether or not to use raw or str value, whichever is faster.
    for sig_name, sig_str_value in data.items():
        if sig_name in signal_callbacks:
            signal_callbacks[sig_name](sig_str_value)


if __name__ == '__main__':

    # config_lines[2]: "device joy `di8.'{E7D4CFE0-D827-11EB-8004-444553540000}|{BEAD1234-0000-0000-0000-504944564944}'`"
    lin = LUC("COM3")

    #lin.set_frame_rx_handler(handle_rx_data)
    lin.set_new_frame_rx_handler(handle_new_rx_data)

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

    # ----- Debug Stuff ------- #
    lin.flushData(b'r00c4\r')
    print("add c to recption table:", lin.ser.readline().decode("utf-8") == 'z\r')

    lin.flushData(b'v\r')
    print("test:", lin.ser.readline().decode("utf-8"))

    print("lowSpeed:", lin.lowSpeed())
    print(lin.addReceptionFrameToTable(btns_slave_frame.frame_id, btns_slave_frame.length))
    # todo: look at custom timing with big T or big R command and lin.flushData

    print("enable:", lin.enable())
    lin.flushData(b'R00c00154\r')  # todo: sometimes this fucks up?
    print("timing:", lin.ser.readline())
    # todo: documentation, how to set up etc.
    # todo maybe: script for adding joy.b# to controls.sii
    # ----- End Debug Stuff ------- #


    def del_lin(*args):
        global lin
        print("Deleting lin")
        lin.disable()
        del lin

    def on_release(key):
        if key == Key.esc:
            del_lin()
            return False

    # Collect events until released
    with Listener(on_release=on_release) as listener:
        listener.join()
        print("Quitting")
        quit(0)

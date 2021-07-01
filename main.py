# https://c4deszes.github.io/ldfparser/frames.html
# https://pyserial.readthedocs.io/en/latest/shortintro.html
from ucanlintools import LUC, LINFrame
from ldfparser import parseLDF, LinFrame
import atexit
from signal_handlers import signal_callbacks
# import signal_handlers as sh

from win32gui import GetWindowText, GetForegroundWindow


ldf = parseLDF("LDFs/LIN23_VMCU-T2_1.3.0-postfix.ldf")
request_frame = ldf.frame('VMCUtoSlaves_L23')
request_data = request_frame.raw({"BacklightCmd_ISig_31": 0,
                                  "FuncIndIlluminationLevel_ISig_31": 1,
                                  "LIN_Rainsensor_Indication": 1})
slave_frame = ldf.frame("SM1toVMCU_L23")



def handle_rx_data(frame: LINFrame):
    # data attr is set on rx frames
    print("RX: ID=", frame.id, " DATA=", ldf.frame(frame.id).parse_raw(frame.data), sep="")


def handle_new_rx_data(frame: LINFrame):
    print("poopo")
    if "Euro Truck Simulator 2" not in GetWindowText(GetForegroundWindow()):
        return

    # data attr is set on rx frames
    data = ldf.frame(frame.id).parse_raw(frame.data)
    print("RX: ID=", frame.id, " DATA=", data, " (NEW DATA)", sep="")
    # todo: decide whether or not to use raw or str value, whichever is faster.
    for sig_name, sig_str_value in data:
        signal_callbacks[sig_name](sig_str_value)


def exit_handler(lin_inst: LUC):
    print("Exiting")
    if isinstance(lin_inst, LUC):
        print("Deleting")
        del lin_inst  # Disables LUC and de-inits serial port



if __name__ == '__main__':

    # config_lines[2]: "device joy `di8.'{E7D4CFE0-D827-11EB-8004-444553540000}|{BEAD1234-0000-0000-0000-504944564944}'`"
    lin = LUC("COM3")
    atexit.register(exit_handler, lin)
    lin.disable()
    
    lin.set_frame_rx_handler(handle_rx_data)
    lin.set_new_frame_rx_handler(handle_new_rx_data)
    print(lin.lowSpeed())
    lin.flushData(b'C\r')
    print("1", lin.ser.readline())
    lin.flushData(b'O\r')
    print("2", lin.ser.readline())
    lin.flushData(b'r00c4\r')
    print("3", lin.ser.readline().decode("utf-8"))
    lin.flushData(b'x1\r')
    print("4", lin.ser.readline())
    lin.flushData(b'R00c15104\r')
    print("5", lin.ser.readline())

    # bob = lin.openAsMaster()

    # lin.addReceptionFrameToTable(slave_frame.frame_id, slave_frame.length)  # set up continuous request sending
    # lin.addTransmitFrameToTable(request_frame.frame_id, request_data)  # todo: not sure if this or the one above is correct, either or I think
    # todo: look at custom timing with big T or big R command and lin.flushData
    lin.enable()


    # todo: documentation, how to set up etc.
    # todo maybe: script for adding joy.b# to controls.sii




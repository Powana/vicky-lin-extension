# https://c4deszes.github.io/ldfparser/frames.html
# https://pyserial.readthedocs.io/en/latest/shortintro.html
from ucanlintools import LUC, LINFrame
from ldfparser import parseLDF, LinFrame
import atexit
from signal_handlers import signal_callbacks

ldf = parseLDF("LDFs/LIN23_VMCU-T2_1.3.0-postfix.ldf")
request_frame = ldf.frame('VMCUtoSlaves_L23')
request_data = request_frame.raw({"BacklightCmd_ISig_31": 0,
                                  "FuncIndIlluminationLevel_ISig_31": 1,
                                  "LIN_Rainsensor_Indication": 0})


def handle_rx_data(frame: LINFrame):
    # data attr is set on rx frames
    print("RX: ID=", frame.id, " DATA=", ldf.frame(frame.id).parse_raw(frame.data), sep="")


def handle_new_rx_data(frame: LINFrame):
    # data attr is set on rx frames
    data = ldf.frame(frame.id).parse_raw(frame.data)
    print("RX: ID=", frame.id, " DATA=", data, " (NEW DATA)", sep="")
    # todo: decide whether or not to use raw or str value, whichever is faster.
    for sig_name, sig_str_value in data:
        signal_callbacks[sig_name](sig_str_value)


def exit_handler(lin_inst: LUC):
    if isinstance(lin_inst, LUC):
        del lin_inst  # Disables LUC and de-inits serial port


if __name__ == '__main__':
    lin = LUC("COM1")
    lin.openAsMaster()
    lin.set_frame_rx_handler(handle_rx_data)
    lin.set_new_frame_rx_handler(handle_new_rx_data)
    lin.addReceptionFrameToTable(request_frame.frame_id, request_frame.length)  # set up continuous request sending
    lin.addTransmitFrameToTable(request_frame.frame_id, request_data)  # todo: not sure if this or the one above is correct, either or I think
    # todo: look at custom timing with big T or big R command and lin.flushData
    lin.enable()
    atexit.register(exit_handler, lin)

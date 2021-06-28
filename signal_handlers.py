import pyvjoy
from multiprocessing import Process, Queue
from threading import Thread
from time import sleep

j = pyvjoy.VJoyDevice(1)

signal_callbacks = {}


def handle_signal(signal_name):
    def decorator(function):
        signal_callbacks[signal_name] = function

        def wrapper(*args, **kwargs):
            return function(*args, **kwargs)

        return wrapper

    return decorator


def release_btn_after(btn, press_after, release_after):
    if press_after:
        sleep(press_after)
    j.set_button(btn, 1)
    sleep(release_after)
    j.set_button(btn, 0)
    return


def press_btn(btn, press_after=0.0, sec=0.03):
    t = Thread(target=release_btn_after, args=(btn, press_after, sec))
    t.start()


@handle_signal("LIN_DirInd_StalkStatus_1")
def hndl_dirind_stalk(signal_val):
    btn_dirind_l = 1
    btn_dirind_r = 2

    if signal_val == 0:
        j.set_button(btn_dirind_l, 0)
        j.set_button(btn_dirind_r, 0)
    elif signal_val in [1, 3]:
        j.set_button(btn_dirind_l, 1)
    elif signal_val in [2, 4]:
        j.set_button(btn_dirind_r, 1)


@handle_signal("LIN_MainBeamStalkStatus_1")
def hndl_mainbeam_stalk(signal_val):
    btn_mainbeam = 3

    if signal_val == 0:
        j.set_button(btn_mainbeam, 0)
    elif signal_val in [1, 2]:
        j.set_button(btn_mainbeam, 1)


@handle_signal("LIN_WiperAdjustStatus_1")
def hndl_wiper_adjust(signal_val):
    print("Handler not implemented, signal val is:", signal_val)


@handle_signal("LIN_WiperStalkStat_1")
def hndl_wiper_stalk(signal_val):
    btn_wipers_tgl = 4
    btn_wipers_off = 5
    btn_wipers_intermittent = 6
    btn_wipers_normal = 7
    btn_wipers_fast = 8
    btn_wipers_4 = 9  # wipers4 seems to be the same as wipers3 (which is 'fast')
    # Bit of a hack for single wipe, todo: check if single wipe is intended behaviour for stalk pos 1
    if signal_val == 1:
        press_btn(btn_wipers_off)
        press_btn(btn_wipers_fast, press_after=0.03)
        press_btn(btn_wipers_off, press_after=0.06)
        return

    btn_map = {0: btn_wipers_off,
               # 1: btn_wipers_tgl,
               2: btn_wipers_intermittent,
               3: btn_wipers_normal,
               4: btn_wipers_fast}
    press_btn(btn_map[signal_val])


@handle_signal("LIN_Rainsensor_ButtonStatus")
def hndl_rainsensor_btn(signal_val):
    print("Handler not implemented, signal val is:", signal_val)


@handle_signal("LIN_BrakeProgramButtonStatus")
def hndl_brakeprog_btn(signal_val):
    print("Handler not implemented, signal val is:", signal_val)


@handle_signal("LIN_Washing_Status_1")
def hndl_wash_status(signal_val):
    print("Handler not implemented, signal val is:", signal_val)


@handle_signal("LIN_RetarderStalkPosition_1")
def hndl_retarder_stalk(signal_val):
    print("Handler not implemented, signal val is:", signal_val)


@handle_signal("LIN_TrailerBrakeInputStatus")
def hndl_trailer_brake_status(signal_val):
    print("Handler not implemented, signal val is:", signal_val)

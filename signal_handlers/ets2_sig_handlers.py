# import pyKey as pK
from ets2_bindings import bindings
from main_handler import *


@handle_signal("LIN_DirInd_StalkStatus_1")
def hndl_dirind_stalk(signal_val):
    btn_dirind_l = bindings["lblinkerh"]
    btn_dirind_r = bindings["rblinkerh"]

    if signal_val == 0:
        j.set_button(btn_dirind_l, 0)
        j.set_button(btn_dirind_r, 0)
    elif signal_val in [1, 3]:
        j.set_button(btn_dirind_l, 1)
    elif signal_val in [2, 4]:
        j.set_button(btn_dirind_r, 1)


@handle_signal("LIN_MainBeamStalkStatus_1")
def hndl_mainbeam_stalk(signal_val):
    btn_mainbeam = bindings["hblight"]
    if signal_val == 0:
        j.set_button(btn_mainbeam, 0)
    elif signal_val in [1, 2]:
        j.set_button(btn_mainbeam, 1)


@handle_signal("LIN_WiperAdjustStatus_1")
def hndl_wiper_adjust(signal_val):
    print("Handler not implemented, signal val is:", signal_val)


@handle_signal("LIN_WiperStalkStat_1")
def hndl_wiper_stalk(signal_val):
    btn_wipers_mode = bindings["wipers"]
    btn_wipers_off = bindings["wipers0"]
    btn_wipers_intermittent = bindings["wipers1"]
    btn_wipers_normal = bindings["wipers2"]
    btn_wipers_fast = bindings["wipers3"]
    btn_wipers_4 = bindings["wipers4"]  # wipers4 seems to be the same as wipers3 (which is 'fast')
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


# Steering wheel buttons
@handle_signal("LIN_SW_Right_ButtonStatus_6")
def hndl_sw_right_btn(signal_val):
    btn_to_key_map(signal_val, Key.right)


@handle_signal("LIN_SW_Left_ButtonStatus_6")
def hndl_sw_left_btn(signal_val):
    btn_to_key_map(signal_val, Key.left)


@handle_signal("LIN_SW_Up_ButtonStatus_6")
def hndl_sw_up_btn(signal_val):
    btn_to_key_map(signal_val, Key.up)


@handle_signal("LIN_SW_Down_ButtonStatus_6")
def hndl_sw_down_btn(signal_val):
    btn_to_key_map(signal_val, Key.down)


@handle_signal("LIN_SW_Enter_ButtonStatus_6")
def hndl_sw_enter_btn(signal_val):
    btn_to_key_map(signal_val, Key.enter)


@handle_signal("LIN_SW_Esc_ButtonStatus_6")
def hndl_sw_esc_btn(signal_val):
    btn_to_key_map(signal_val, Key.esc)


@handle_signal("LIN_SW_Mute_ButtonStatus_6")
def hndl_sw_mute_btn(signal_val):
    btn_to_key_map(signal_val, Key.media_volume_mute)

# todo:
# Konstantinos, there are a few more buttons that can be mapped straight to windows buttons like the ones above, gunna go home now

# import pyKey as pK
from ets2_bindings import bindings
from .main_handler import *


@handle_signal("LIN_DirInd_StalkStatus_1")
def hndl_dirind_stalk(sig_val):
    # btn 1 will be used for keeping blinkers on, btn 2 will be used for "flashing" the blinkers a few secs on stalk tap
    btn_dirind_l1 = bindings["lblinkerh"][0]
    btn_dirind_l2 = bindings["lblinkerh"][1]
    btn_dirind_r1 = bindings["rblinkerh"][0]
    btn_dirind_r2 = bindings["rblinkerh"][1]

    if sig_val == 0:
        j.set_button(btn_dirind_l2, 0)
        j.set_button(btn_dirind_r2, 0)

    elif sig_val == 1:  # All the way left
        j.set_button(btn_dirind_l2, 1)

    elif sig_val == 3:  # Halfway left
        press_btn(btn_dirind_l1, release_after=4)
        j.set_button(btn_dirind_l2, 1)

    elif sig_val == 2:  # All the way right
        j.set_button(btn_dirind_r2, 1)

    elif sig_val == 4:  # Halfway right
        press_btn(btn_dirind_r1, release_after=4)
        j.set_button(btn_dirind_r2, 1)



@handle_signal("LIN_MainBeamStalkStatus_1")
def hndl_mainbeam_stalk(sig_val):
    btn_tgl_mainbeam = bindings["hblight"]
    btn_hold_mainbeam = bindings["lighthorn"]

    if sig_val == 0:
        j.set_button(btn_hold_mainbeam, 0)
    elif sig_val == 1:
        j.set_button(btn_hold_mainbeam, 1)
    elif sig_val == 2:
        press_btn(btn_tgl_mainbeam)


@handle_signal("LIN_WiperAdjustStatus_1")
def hndl_wiper_adjust(sig_val):
    print("Handler not implemented, signal val is:", sig_val)


@handle_signal("LIN_WiperStalkStat_1")
def hndl_wiper_stalk(sig_val):
    btn_wipers_mode = bindings["wipers"]
    btn_wipers_off = bindings["wipers0"]
    btn_wipers_intermittent = bindings["wipers1"]
    btn_wipers_normal = bindings["wipers2"]
    btn_wipers_fast = bindings["wipers3"]
    btn_wipers_4 = bindings["wipers4"]  # wipers4 seems to be the same as wipers3 (which is 'fast')
    # Bit of a hack for single wipe, todo: check if single wipe is intended behaviour for stalk pos 1
    if sig_val == 1:
        press_btn(btn_wipers_off, release_after=0.03)
        press_btn(btn_wipers_fast, press_after=0.03)
        press_btn(btn_wipers_off, press_after=0.06)
        return

    btn_map = {0: btn_wipers_off,
               # 1: btn_wipers_tgl,
               2: btn_wipers_intermittent,
               3: btn_wipers_normal,
               4: btn_wipers_fast}
    if sig_val in btn_map.values():
        press_btn(btn_map[sig_val])


@handle_signal("LIN_BrakeProgramButtonStatus")
def hndl_brakeprog_btn(sig_val):
    # Todo: Replace the retarder stalk for one without this button, not usable in ets2
    print("Handler not implemented, signal val is:", sig_val)


@handle_signal("LIN_RetarderStalkPosition_1")
def hndl_retarder_stalk(sig_val):
    # NOTE: The position to retarder level mapping is specific to the stalk module installed
    # Some stalks have settings 'A','0','1','2','3', some only have 'A','1'.
    if sig_val == 1:  # todo: check what we have and map that
        pass
    print("Handler not implemented, signal val is:", sig_val)


@handle_signal("LIN_Rainsensor_ButtonStatus")
def hndl_rainsensor_btn(sig_val):
    print("Handler not implemented, signal val is:", sig_val)


@handle_signal("LIN_Washing_Status_1")
def hndl_wash_status(sig_val):
    print("Handler not implemented, signal val is:", sig_val)


@handle_signal("LIN_TrailerBrakeInputStatus")
def hndl_trailer_brake_status(sig_val):
    print("Handler not implemented, signal val is:", sig_val)


# Steering wheel buttons
@handle_signal("LIN_SW_Right_ButtonStatus_6")
def hndl_sw_right_btn(sig_val):
    btn_to_key_map(sig_val, "right")


@handle_signal("LIN_SW_Left_ButtonStatus_6")
def hndl_sw_left_btn(sig_val):
    btn_to_key_map(sig_val, "left")


@handle_signal("LIN_SW_Up_ButtonStatus_6")
def hndl_sw_up_btn(sig_val):
    btn_to_key_map(sig_val, "up")


@handle_signal("LIN_SW_Down_ButtonStatus_6")
def hndl_sw_down_btn(sig_val):
    btn_to_key_map(sig_val, "down")


@handle_signal("LIN_SW_Enter_ButtonStatus_6")
def hndl_sw_enter_btn(sig_val):
    btn_to_key_map(sig_val, "enter")


@handle_signal("LIN_SW_Esc_ButtonStatus_6")
def hndl_sw_esc_btn(sig_val):
    btn_to_key_map(sig_val, "esc")


@handle_signal("LIN_SW_Mute_ButtonStatus_6")
def hndl_sw_mute_btn(sig_val):
    btn_to_key_map(sig_val, "volume mute")


@handle_signal("LIN_SW_VolDown_ButtonStatus_6")
def hndl_sw_voldown(sig_val):
    btn_to_key_map(sig_val, "volume down")

# This is getting tedious, going to use anonymous function names from here on out to save time


@handle_signal("LIN_SW_VolUp_ButtonStatus_6")
def hndl_sw_volup(sig_val):
    btn_to_key_map(sig_val, "volume up")


@handle_signal("LIN_SW_Menu_ButtonStatus_6")
def hndl_sw_menu(sig_val):
    btn_to_key_map(sig_val, "esc")


@handle_signal("LIN_SWSpdCtrlButtonsStatus6")
def hndl_sw_spdctrl(sig_val):
    btn_map = {1: bindings["cruiectrl"],  # val 1/2 should actually only turn off/on, but ets2 only has a toggle button
               2: bindings["cruiectrl"],
               3: bindings["cruiectrlinc"],
               4: bindings["cruiectrldec"]}
    if sig_val in btn_map.values():
        press_btn(btn_map[sig_val])
    elif sig_val == 5:
        keyboard.press_and_release("enter")


@handle_signal("LIN_SW_Home_ButtonsStatus_6")
def hndl_sw_home(sig_val):
    btn_to_key_map(sig_val, bindings["showhud"])


@handle_signal("LIN_SW_Focus_ButtonStatus_6")
def hndl_sw_focus(sig_val):
    btn_to_key_map(sig_val, bindings["advpagen"])

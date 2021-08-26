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
    if sig_val in btn_map.keys():
        press_btn(btn_map[sig_val])


@handle_signal("LIN_TrailerBrakeInputStatus")
# Todo: The stalk has 2 position for this function but there is only 1 in the game
def hndl_trailer_brake_btn(sig_val):
    btn_trailer_brake = bindings["trailerbrake"]
    if sig_val in (1, 2):
        j.set_button(btn_trailer_brake, 1)
    else:
        j.set_button(btn_trailer_brake, 0)


@handle_signal("LIN_RetarderStalkPosition_1")
def hndl_retarder_stalk(sig_val):
    btn_retard_off = bindings["retarder0"]
    btn_retard_pos_1 = bindings["retarder1"]
    btn_retard_pos_2 = bindings["retarder2"]
    btn_retard_pos_3 = bindings["retarder3"]
    btn_retard_pos_4 = bindings["retarder4"]
    btn_retard_pos_5 = bindings["retarder5"]
    btn_retard_auto = bindings["retarder0"]  # Todo: There is a setting with auto retarder in the game but no key binding
    btn_map = {0: btn_retard_off,
               1: btn_retard_pos_1,
               2: btn_retard_pos_2,
               3: btn_retard_pos_3,
               4: btn_retard_pos_4,
               5: btn_retard_pos_5,
               7: btn_retard_auto}
    if sig_val in btn_map.keys():
        press_btn(btn_map[sig_val])


@handle_signal("LIN_Rainsensor_ButtonStatus")
# Todo: It is not supported by the game as for now
def hndl_rainsensor_btn(sig_val):
    print("Handler not implemented, signal val is:", sig_val)


@handle_signal("LIN_Washing_Status_1")
# Todo: It is not supported by the game as for now
def hndl_wash_status(sig_val):
    print("Handler not implemented, signal val is:", sig_val)


prev_gear = None
# Gear Lever Unit
@handle_signal("LIN_GearLeverStatus_5")
def hndl_GLU_status(sig_val):
    global prev_gear
    
    btn_gear_R = bindings["reverse"]
    btn_gear_N = bindings["gear0"]
    btn_gear_A = bindings["drive"]
    btn_gear_M = bindings["transemi_on"]
    btn_map = {0: btn_gear_R,
               1: btn_gear_N,
               2: btn_gear_A,
               3: btn_gear_M}
    
    
    if sig_val in btn_map:
        if prev_gear is None:
            prev_gear = sig_val
            
        if sig_val == 3:
            press_btn(btn_map[3])
        
        elif sig_val == 2 and prev_gear == 3:
            press_btn(bindings["transemi_on"])


        # Looks dumb but ensures overlap when shifting gears to retain current gear num
        # TODO: Fix gear reset to N when swapping to manual
        if sig_val != 3:
            j.set_button(btn_map[sig_val], 1)
            
        for key in [2,1,0]:
            j.set_button(btn_map[key], 0 if sig_val != key else 1)


        prev_gear = sig_val
        
        

@handle_signal("LIN_GearShiftInputStatus_5")
def hndl_GLU_gear_shift(sig_val):
    btn_shift_up_h = bindings["gearuphint"]
    btn_shift_down_h = bindings["geardownhint"]
    btn_map = {1: btn_shift_up_h,
               2: btn_shift_down_h,
               3: bindings["gearup"],
               4: bindings["geardown"]}

    # NOTE: Buggy bhaviour when shifting up/down in A1, game bug
    if sig_val in btn_map.keys():
        if prev_gear == 3:
            sig_val += 2
        press_btn(btn_map[sig_val])


# Steering wheel buttons
# The green phone button will act as the ignition
@handle_signal("LIN_SW_GreenPhone_BtnStat_6")
def hndl_sw_green_phone_btn(sig_val):
    btn_green_phone = bindings["engine"]
    if sig_val == 1:
        press_btn(btn_green_phone)
# The red phone button will act as the parking brake toggle
@handle_signal("LIN_SW_RedPhone_BtnStat_6")
def hndl_sw_red_phone_btn(sig_val):
    btn_red_phone = bindings["parkingbrake"]
    if sig_val == 1:
        press_btn(btn_red_phone)

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

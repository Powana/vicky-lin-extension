# Provides helper functions for creating new handlers
# Provides keyboard and virtual gamepad controller

# Most keyboard input libraries use SendInput from win32 that doesn't work with ETS2, 'keyboard' does not
import keyboard
from threading import Thread
from time import sleep
import pyvjoy


signal_callbacks = {}
signal_values = {}  # todo: Check if needed, or if it slows stuff down too much


j = pyvjoy.VJoyDevice(1)
keyb = keyboard  # todo : useless variable


# Decorate a handler with this, using the string value of the signal name
def handle_signal(signal_name):
    def decorator(function):
        def wrapper(signal_val):
            # Only run the handler if the signal value has actually changed
            if signal_values[signal_name] != signal_val:
                signal_values[signal_name] = signal_val
                return function(signal_val)

        signal_callbacks[signal_name] = wrapper
        signal_values[signal_name] = None

        return wrapper

    return decorator


def _press_and_release_btn(btn, press_after, release_after):
    if press_after:
        sleep(press_after)
    j.set_button(btn, 1)
    sleep(release_after)
    j.set_button(btn, 0)
    return


def press_btn(btn, press_after=0.0, release_after=0.03):
    t = Thread(target=_press_and_release_btn, args=(btn, press_after, release_after))
    t.start()


# Can be used for convenience if the button should be mapped one-to-one to a windows key
# Possible key values are created at runtime, check: keyboard._winkeyboard.from_name.keys()
def btn_to_key_map(signal_val, key: str or int):
    keyb.press(key) if signal_val == 1 else keyb.release(key)
    # pK.pressKey(key) if signal_val == 1 else pK.releaseKey(key)  # Using pyKey doesn't work, uses sendinput

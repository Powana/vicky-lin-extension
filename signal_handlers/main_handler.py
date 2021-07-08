# Provides helper functions for creating new handlers
# Proides keyboard and virtual gamepad controller
from pynput.keyboard import Controller, Key
from threading import Thread
from time import sleep
import pyvjoy

signal_callbacks = {}
signal_values = {}  # todo: Check if needed, or if it slows stuff down too much


j = pyvjoy.VJoyDevice(1)
keyb = Controller()


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


# Can be used for convenience if the button should be mapped one-to-one to a windows key
# For posible Key values, check: https://pynput.readthedocs.io/en/latest/keyboard.html#pynput.keyboard.Key
def btn_to_key_map(signal_val, key: Key):
    keyb.press(key) if signal_val == 1 else keyb.release(key)
    # pK.pressKey(key) if signal_val == 1 else pK.releaseKey(key)

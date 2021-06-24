import pyKey as pk

signal_callbacks = {}


def handle_signal(signal_name):
    def decorator(function):
        signal_callbacks[signal_name] = function

        def wrapper(*args, **kwargs):
            return function(*args, **kwargs)
        return wrapper
    return decorator


def send_with_mod_key(key: str):
    # todo: add check for ets2 as activewindow here? might be too slow
    mod_key = "RSHIFT"

    pk.pressKey(mod_key)
    pk.pressKey(key)
    pk.releaseKey(mod_key)
    pk.releaseKey(key)


@handle_signal("LIN_DirInd_StalkStatus_1")
def hndl_dirind(signal_val):
    if signal_val == 1:
        pass
    if signal_val == "LIN_DirInd_StalkStatus_LeftTurningIndication":
        pass

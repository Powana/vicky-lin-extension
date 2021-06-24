import pyKey as pK
from timeit import default_timer as timer

start = timer()
end = timer()
print("time:", end-start)
signal_callbacks = {}


def handle_signal(signal_name):
    def decorator(function):
        signal_callbacks[signal_name] = function

        def wrapper(*args, **kwargs):
            return function(*args, **kwargs)
        return wrapper
    return decorator


def send_with_mod_key(key: str):
    # todo: add check for ets2 as active window here? might be too slow
    mod_key = "RSHIFT"

    pK.pressKey(mod_key)
    pK.pressKey(key)
    pK.releaseKey(mod_key)
    pK.releaseKey(key)


@handle_signal("LIN_DirInd_StalkStatus_1")
def hndl_dirind(signal_val):
    pref = "LIN_DirInd_StalkStatus_"
    if signal_val == 1:
        pass
    if signal_val == pref + "LeftTurningIndication":
        pass

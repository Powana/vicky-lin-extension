

# map between name of input in controls.sii, and the vJoy button # to associate with it
bindings = {
    "lblinkerh": 1,
    "rblinkerh": 2,
    "hblight": 3,
    "wipers": 4,
    "wipers0": 5,
    "wipers1": 6,
    "wipers2": 7,
    "wipers3": 8,
    "wipers4": 9,
}


#  Add all bindings to a controls.sii file if not already added
def main():
    path = "controls.sii"
    with open(path, "r") as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        for input_name in bindings:
            if " " + input_name + " " in line:
                joy_str = "joy.b" + str(bindings[input_name]) + "?0 "
                # bug: this will be False if ui_joy.b#?0 is in the line, but probably doesnt matter
                if joy_str not in line:
                    j = lines[i].index("`")+1  # bindings start after first backtick in line
                    lines[i] = lines[i][:j] + joy_str + "| " + lines[i][j:]  # insert joy_str after first backtick

    with open(path, "w") as f:
        f.writelines(lines)


if __name__ == '__main__':
    main()

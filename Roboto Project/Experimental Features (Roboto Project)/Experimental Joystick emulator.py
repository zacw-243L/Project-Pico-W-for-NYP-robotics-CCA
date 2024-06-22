import keyboard

keypress_forward = 0
keypress_backward = 0
keypress_left = 0
keypress_right = 0


def handle_key_event(e):
    global keypress_forward, keypress_backward, keypress_left, keypress_right

    if e.event_type == keyboard.KEY_DOWN:
        if e.name == "a":
            keypress_left += 1
            print(f"Left: {keypress_left}")
        elif e.name == "w":
            keypress_forward += 1
            print(f"Forward: {keypress_forward}")
        elif e.name == "d":
            keypress_right += 1
            print(f"Right: {keypress_right}")
        elif e.name == "s":
            keypress_backward += 1
            print(f"Backward: {keypress_backward}")


keyboard.on_press(handle_key_event)

# This keeps the script running
keyboard.wait("esc")

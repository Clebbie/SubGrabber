from pynput import keyboard
from pynput.keyboard import Key, Controller
import clipboard

board = Controller()
# The key combination to check
# Look into putting this into a config file
COMBINATION = {keyboard.Key.alt, keyboard.Key.ctrl}
current = set()


def on_press(key):
	if key in COMBINATION:
		current.add(key)
	if all(k in current for k in COMBINATION):
		paste()
	if key == keyboard.Key.esc:
		listener.stop()

def paste():
	#If the keystrok is hit, first pop all current keys out then type whatever is on clipboard
	for keyIndex in range(len(current)):
		current.pop()
	clipboard_message = clipboard.paste()
	board.type(clipboard_message)

def on_release(key):
        try:
        	current.remove(key)
        except KeyError:
        	pass

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
	listener.join()

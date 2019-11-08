from __future__ import print_function
import keyboard

def printMeDaddy(wordOne, wordTwo):
	print(wordOne + ' ' + wordTwo)

def printClipboard():
	#keyboard.send('shift + enter')
	keyboard.send('ctrl+shift+v', 'enter')
	#keyboard.write('ctrl+shift+v')
	#keyboard.call_later(keyboard.send, args=('ctrl+shift+v','enter'), delay=0.01)
	#keyboard.send('shift + enter')

keyboard.add_hotkey('ctrl+shift+a', printClipboard, args=())
keyboard.read_hotkey()

#keyboard.send('ctrl+shift+v')
#keyboard.call_later(printMeDaddy, args=('plz','help'), delay=0.001)

# Blocks until you press esc.
#keyboard.wait('esc')

# Type @@ then press space to replace with abbreviation.
#keyboard.add_abbreviation('@@', 'my.long.email@example.com')

# Block forever, like `while True`.
#keyboard.wait()



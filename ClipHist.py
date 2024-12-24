"""
ClipHist

Written 12/23/24 by Talia Shaffer
(github.com/TaliBytes/ClipHist)

A simple clipboard history manager service for Linux
"""


# set your preferred configuration here:
maxClipboardItems = 20





"""  START OF PROGRAM  """

import pyperclip
from pynput import keyboard


class tClipboardManager:
    def __init__(self):
        # self.history stores all items
        self.history = []

    def addToSystemClipboard(self, item):
        pyperclip.copy(item)

    def addToHistory(self, item):
        if item in self.history:
            # move item to top if it is already in history
            self.history.remove(item)
            self.history.insert(0, item)
            self.addToSystemClipboard(item)
            return

        if item not in self.history:
            # add to ClipHist
            self.history.insert(0, item)        
            self.addToSystemClipboard(item)

            # remove oldest item if too many items
            if len(self.history) > maxClipboardItems:
                self.history.pop()
            return

    def popFromHistory(self, itemNo = 0):
        # remove selected item or most recent item
        self.history.pop(itemNo)
        
        # copy the new most recent item to system clipboard
        # (just in case the previous item was the item removed from clipboard)
        anItem = self.history[0]
        self.addToSystemClipboard(anItem)

clipboard = tClipboardManager()



clipboard.addToHistory('goodnight')
clipboard.addToHistory('sky!')

print(clipboard.history)





def clipHistGUI():
    print('SUPER PASTE CALLED')



# tracks if <cmd> is pressed but not released
hotKeyPressed = False

def onPress(key):
    global hotKeyPressed

    try:
        print('pressed', key)
        if key == keyboard.Key.cmd:
            hotKeyPressed = True
        elif hotKeyPressed and key == keyboard.KeyCode.from_char('v'):
            hotKeyPressed = False
            clipHistGUI()
    except AttributeError:
        pass



def onRelease(key):
    global hotKeyPressed

    if key == keyboard.Key.cmd:
        print('released cmd')
        hotKeyPressed = False



def keyboardListener():
    with keyboard.Listener(on_press=onPress, on_release=onRelease, suppress=False) as listener:
        listener.join()

keyListener = keyboardListener()

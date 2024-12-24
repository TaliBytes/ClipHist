"""
LEGACY FILE
This was the start of ClipHist. I chose to restart once I had a better idea of what I'm aiming for and how to achieve it.
Keeping for future reference until ClipHist v.1 is complete.
"""



import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

from pynput import keyboard
import threading



# number of items the clipboard is allowed to store
maxClipboardItems = 20  

# flag to track state of the hotkey
hotKeyPressed = False



class tClipboardManager:
    def __init__(self):
        # get clipboard object and create history array
        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        self.history = []

    # add and item only if it doesn't exist
    def addToHistory(self, item):
        if item not in self.history:
            self.history.insert(0, item)

            # when an item is added, check to see if too many stored items
            if len(self.history) > maxClipboardItems:
                self.history.pop()

    # waits for text to be added to system clipboard, then adds it to history
    def getFromHistory(self):
        content = self.clipboard.wait_for_text()
        if content:
            self.addToHistory(content)

    def setClipboardContent(self, item):
        self.clipboard.set_text(item, -1)



class tClipboardHistoryGUI(Gtk.Window):
    def __init__ (self, manager):
        # create the window, link to clipboardManager
        super().__init__(title='ClipHist')
        self.manager = clipboardManager
        self.set_default_size(350,450)

        self.listbox = Gtk.ListBox()
        self.add(self.listbox)

        # link close event to handler (hide)
        self.connect("delete-event", self.onClose)

    def onClose(self, *args):
        # hide instead of close
        self.hide()
        return True

    def updateList(self):
        # remove outdated/empty rows on update of list
        self.listbox.foreach(lambda widget: self.listbox.remove(widget))

        # list current history items
        for item in self.manager.history:
            row = Gtk.ListBoxRow()
            label = Gtk.Label(label=item, xalign=0)
            row.add(label)
            self.listbox.add(row)
        self.listbox.show_all()

    def onRowActivated(self, listbox, row):
        # copy selected item to system clipboard
        item = row.get_child().get_label()
        self.manager.setClipboardContent(item)
        self.manager.addToHistory(item)
        self.hide()



# show history GUI
def showHistory():
    # ensure the GUI exists if it was accidentally destroyed
    global clipboardGUI
    if clipboardGUI is None:
        clipboardGUI = tClipboardHistoryGUI(clipboardManager)

    # open clipboardGUI and bring into focus
    clipboardGUI.show_all()
    clipboardGUI.present()



# hotkey pressed
def onPress(key):
    global hotKeyPressed

    try:
        if key == keyboard.Key.cmd:
            hotKeyPressed = True
        elif hotKeyPressed and key == keyboard.KeyCode.from_char('v'):
            showHistory()
            return False
    except AttributeError:
        pass



# hotkey released
def onRelease(key):
    global hotKeyPressed

    if key == keyboard.Key.cmd:
        hotKeyPressed = False



# listen for key press and releases
def hotKeyListener():
    with keyboard.Listener(on_press=onPress, on_release=onRelease, suppress=True) as listener:
        listener.join()



# initialize everything
def main():
    # new clipboard manager and associated GUI
    global clipboardManager, clipboardGUI
    clipboardManager = tClipboardManager
    clipboardGUI = tClipboardHistoryGUI(clipboardManager)

    # config and start hotkey listener thread ... start GTK main loop
    threading.Thread(target=hotKeyListener, daemon=True).start()    # threaded separate to prevent interference with Gtk.main() loop
    Gtk.main()

if __name__ == '__main__':
    main()

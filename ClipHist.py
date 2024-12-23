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


# new clipboard manager object
clipboardManager = tClipboardManager



class tClipboardHistoryGUI(Gtk.Window):
    def __init__ (self, manager):
        # create the window, link to clipboardManager
        super().__init__(title='Clipboard History')
        self.manager = clipboardManager
        self.set_default_size(300,500)

        self.listbox = Gtk.ListBox()
        self.add(self.listbox)

        # connect clise event to a function
        self.connect('destroy', Gtk.main_quit)

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
    # clipboard history GUI object
    clipboardGUI = tClipboardHistoryGUI(clipboardManager)

    # open clipboard window and bring into focus
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
threading.Thread(target=hotKeyListener, daemon=True).start()    # threaded separate to prevent interference with Gtk.main() loop
Gtk.main()

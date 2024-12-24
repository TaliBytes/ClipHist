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
import keyboard
import tkinter as tk


class tClipboardManager:
  def __init__(self):
    # self.history stores all items
    self.history = []

  def addToSystemClipboard(self, item):
    pyperclip.copy(item)
    return

  def addToHistory(self, item, addToSysClipboard = False):
    if item in self.history:
      # move item to top if it is already in history
      self.history.remove(item)
      self.history.insert(0, item)
      if addToSysClipboard: self.addToSystemClipboard(item)
      return

    if item not in self.history:
      # add to ClipHist
      self.history.insert(0, item)    
      if addToSysClipboard: self.addToSystemClipboard(item)

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
    return

  def paste(self, item):
    # move item to top, ensure it is copied to sys clipboard, paste
    self.history.remove(item)
    self.history.insert(0, item)
    self.addToSystemClipboard(item)
    pyperclip.paste()
    return

clipboard = tClipboardManager()



def clipHistGUI():
  # create and show GUI
  root = tk.Tk()
  root.title('ClipHist')
  root.geometry('405x450')
  root["background"] = "gray15"
  root.resizable(False, False)

  frame = tk.Frame(root, background="gray15")
  frame.grid()

  print('\n\n', len(clipboard.history), clipboard.history, '\n\n')

  # add ClipHist items to frame
  for position, item in enumerate(clipboard.history):
    position = clipboard.history.index(item)
    tk.Label(frame,
              width=47, height=4,
              wraplength=372,
              justify='left', anchor="nw",
              background="gray20", foreground="gray80",
              text=f"{item}"
            ).grid(column=0, row=position, ipadx=1, ipady=5, padx=(12,12), pady=(15,0))
    
  root.mainloop()



def on_alt_v():
  clipHistGUI()

# WHY NO SUPPRESS???
keyboard.add_hotkey('alt+v', on_alt_v, suppress=True, trigger_on_release=False)

try:
  keyboard.wait()
except KeyboardInterrupt:
  print('stopped')

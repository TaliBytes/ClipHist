"""
ClipHist

Written 12/23/24 by Talia Shaffer
(github.com/TaliBytes/ClipHist)

A simple clipboard history manager service for Linux
"""


# set your preferred configuration here:
maxClipboardItems = 20





"""  START OF PROGRAM  """

from pynput import keyboard   # ctrl+c listener
import pyperclip              # used to manage system clipboard
import threading              # used to run multiple listeners concurrently
import tkinter as tk          # used for copy history gui


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



def on_cmd_v():
  clipHistGUI()
 


ctrlPressed = False

def onPress(key):
  global ctrlPressed

  try:
    if key == keyboard.Key.ctrl:
      ctrlPressed = True
      return

    elif ctrlPressed and key == keyboard.KeyCode.from_char('c'):
      clipboard.addToHistory(pyperclip.paste(), True)
      return
    
  except AttributeError:
    pass
  


def onRelease(key):
  global ctrlPressed

  if key == keyboard.Key.ctrl:
    ctrlPressed = False
    return
  


def keyboardListener():
  # listen for ctrl+c
  with keyboard.Listener(on_press=onPress, on_release=onRelease, suppress=False) as listener:
    listener.join()



def commandProcessor(cmd):
  cmd = str(cmd).strip()
  
  if cmd == 'trigger_cmd_v':
    on_cmd_v()
  else: print('not listening for ' + cmd)



def commandListener():
  # listen for named pipe commands such as cmd+v ...
  # commands run through the named pipe in PIPE_PATH created by ClipHist.superPaste.trigger.sh

  PIPE_PATH = '/tmp/ClipHistPipe'

  with open(PIPE_PATH, 'r') as pipe:
    try:
      while True:
        cmd = pipe.readline().strip()
        if cmd:
          commandProcessor(cmd)
    except:
      print('\nterminated program\n\n')



if __name__ == '__main__':
  # initialize named pipe and keyboard listeners

  keyListenerThread = threading.Thread(target=keyboardListener, daemon=True)
  cmdListenerThread = threading.Thread(target=commandListener, daemon=True)

  cmdListenerThread.start()
  keyListenerThread.start()

  cmdListenerThread.join()
  keyListenerThread.join()

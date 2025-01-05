"""
ClipHist

Written 12/23/24 by Talia Shaffer
(github.com/TaliBytes/ClipHist)

A simple clipboard history manager service for Linux
"""


# set your preferred configuration here:
maxClipboardItems = 20





"""  START OF PROGRAM  """
import os                           # manages named pipe
from pyautogui import position      # open GUI next to mouse
from pyautogui import hotkey        # simulate paste from system clipboard
import pyperclip                    # used to manage system clipboard and listen for changes
import threading                    # used to run multiple listeners concurrently
from time import sleep              # reduces number of clipboard checks by waiting
from tkinter import *               # used for copy history gui


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
  root = Tk()
  mouseX = position().x
  mouseY = position().y
  root.geometry(f"405x450+{mouseX}+{mouseY}")

  root.title('ClipHist')
  root["background"] = "gray15"
  root.resizable(False, False)

  scrollbar = Scrollbar(root)
  scrollbar.pack(side=RIGHT, fill=Y)

  historyList = Text(
    root,
    background="gray20",
    foreground="gray80",
    selectbackground="gray50",
    selectforeground="white",
    wrap="word",
    yscrollcommand=scrollbar.set
  )

  historyList.pack(side=LEFT, fill=BOTH, expand=True)
  scrollbar.config(command=historyList.yview)

  for index, item in enumerate(clipboard.history):
    tagName = f"item_{index}"
    spacerTagName = f"{tagName}_spacer"
    historyList.insert(END, f"{item}\n", tagName)

    historyList.tag_config(
      tagName,
      foreground="white",
      background="gray30",
      font=("Arial",12),
      spacing1=5,
      spacing3=5
    )
    historyList.tag_bind(tagName, "<Button-1>", lambda e, i=index: onSelect(i))

    historyList.insert(END, "\n", spacerTagName)
    historyList.tag_config(
      spacerTagName,
      background="gray20"
    )


  def onSelect(index):
    # close ClipHist GUI
    root.destroy()
    
    # bring to top of clipboard, put in system clipboard
    clipboard.addToHistory(clipboard.history[index], True)
    
    # paste from system clipboard after small delay to resume focus on previous
    hotkey('ctrl', 'v')

  mainloop()



def commandProcessor(cmd):
  cmd = str(cmd).strip()
  
  if cmd == 'trigger_cmd_v':
    try:
      clipHistGUI()
    except Exception as err:
      print(f"\nError rendering GUI: {err}")
  else: print('Not listening for ' + cmd)



def commandListener():
  # listen for named pipe commands such as cmd+v ...
  # commands run through the named pipe in PIPE_PATH created by ClipHist.superPaste.trigger.sh

  PIPE_PATH = '/tmp/ClipHistPipe'

  if not os.path.exists(PIPE_PATH):
    with open(PIPE_PATH, 'w+') as pipe:
      pipe.close()  # close immediately after creating

  try:
    with open(PIPE_PATH, 'r') as pipe:
      try:
        while True:
          cmd = pipe.readline().strip()
          if cmd:
            commandProcessor(cmd)
      except Exception as err:
        print(f"\nTerminated program with error: {err}")
  except:
    print(f"\nCouldn't open or create {PIPE_PATH} ... error: {err}")



def clipboardChangeListener():
  previousContent = None
  while True:
    try:
      currentContent = pyperclip.paste()
      if currentContent != previousContent:
        previousContent = currentContent  # update previous content to match the current, since there has been a change
        clipboard.addToHistory(currentContent, False)
    except Exception as err:
      print(f'\nError accessing clipboard: {err}')

    # sleep for between checks
    sleep(.25)



if __name__ == '__main__':
  # initialize named pipe and clipboard listeners

  cmdListenerThread = threading.Thread(target=commandListener, daemon=True)
  copyListener = threading.Thread(target=clipboardChangeListener, daemon=True)

  copyListener.start()
  cmdListenerThread.start()

  copyListener.join()
  cmdListenerThread.join()

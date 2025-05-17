"""
ClipHist

Written 12/23/24 by Talia Shaffer
(github.com/TaliBytes/ClipHist)

A simple clipboard history manager service for Linux
"""


# set your preferred configuration here:
maxClipboardItems = 20





"""  START OF PROGRAM  """
import os                           # used to check if named pipe exists, get assets for GUI
from pyautogui import position      # open GUI next to mouse
from pyautogui import hotkey        # simulate paste from system clipboard
import pyperclip                    # used to manage system clipboard TEXT
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
  # whether ClipHist should attempt to paste (ctrl+v) upon GUI close
  doPaste = False

  assets_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets'))

  # create 418x450 tkinter GUI that appears under mouse
  root = Tk()
  mouseX = position().x - 202
  mouseY = position().y - 45
  root.geometry(f"418x450+{(mouseX)}+{(mouseY)}") # 418 instead of 405 to accomdate space for scrollbar (with width of 13)

  root.title('ClipHist')
  #root.overrideredirect(True)   # remove toolbar ... ALSO CAUSES LOSE FOCUS => CLOSE APP TO CEASE FUNCTIONING
  root["background"] = "gray15"
  root.resizable(False, False)

  icon = PhotoImage(file = assets_path + "/ClipHist.png")
  root.iconphoto(True, icon)

  # create canvas in the GUI, to which everything else (except scrollbar) is bound
  canvas = Canvas(
    root,
    bg = "#1E1E1E",
    height = 450,
    width = 405,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
  )
  canvas.place(x=0,y=0)

  # configure scrollbar to scroll the canvas
  scrollbar_frame = Frame(root, bg="gray15", padx=3, pady=5)
  scrollbar_frame.pack(side=RIGHT, fill=Y)

  scrollbar = Scrollbar(scrollbar_frame, orient=VERTICAL, command=canvas.yview)
  scrollbar.pack(side=RIGHT, fill=Y)
  scrollbar.config(bg="#4E4E4E", activebackground="#5E5E5E", troughcolor="gray15", border=0, borderwidth=0, relief="flat")
  canvas.config(yscrollcommand=scrollbar.set)

  # BACKGROUND
  canvas.create_rectangle(
    0.0,
    0.0,
    405.0,
    450.0,
    fill="#1E1E1E",
    outline=""
  )


  # LOOP COPIED ITEMS (lower python program line number = lower z-index in rendered GUI)
  btn_img = PhotoImage(file = assets_path + "/rounded_button.png")

  for index, item in enumerate(clipboard.history):
    # 47 = gap, 73 = added gap per item shown in GUI
    yPos = 47 + index * 73

    item_background = canvas.create_image(
      202.0, yPos, image = btn_img
    )

    # handle text items
    if isinstance(item, str):
      itemText = item.replace('\n\n', '\n')       # replace multiple new lines with single ones for better preview
      itemText = itemText.replace('\n', ' ' * 50) # replace newlines with 50 empty chars for string len counting purposes (to be changed back)
      itemText = itemText[:180]
      itemText = itemText.replace(' ' * 50, '\n') # replace 50 spaces with newline now that item length is counted
      if len(item) >= 180: itemText = itemText + '...'

      canvas.create_text(
        16.0, yPos-32,
        anchor="nw",
        text=itemText,
        fill="#FFFFFF",
        font=("Inter", 13 * -1),
        width=376
      )

    # handle other items  
    else:
      print('non-text items not supported yet')

    clickable_zone = canvas.create_rectangle(
      0, yPos-36,
      405,yPos+28,
      outline="",
      fill="",
      tags=f"item_{index}"
    )

    canvas.tag_bind(
      f"item_{index}",
      "<Button-1>",
      lambda e, i=index: onSelect(i)
    )
  # END LOOP COPIED ITEMS


  # when a copied item is selected from GUI
  def onSelect(index):
    # quit GUI mainloop
    root.quit()

    # bring copied item to top of clipboard, put in system clipboard
    clipboard.addToHistory(clipboard.history[index], True)
    
    # prime paste from system clipboard... paste occurs after GUI closes to ensure original input is selected
    nonlocal doPaste
    doPaste = True

  # UPDATE SCROLLABLE AREA
  canvas.config(scrollregion=canvas.bbox("all"))


  # MOUSE WHEEL scrollability for canvas+scrollbar
  def on_mouse_wheel(e):
    if e.num == 4:  # Linux scroll up
      canvas.yview_scroll(-1, "units")

    if e.num == 5:  # Linux scroll down
      canvas.yview_scroll(1, "units")

  root.bind_all('<Button-4>', on_mouse_wheel)
  root.bind_all('<Button-5>', on_mouse_wheel)


  # CLOSE ON LOSE FOCUS
  def on_focus_out(e):
    root.quit()

  root.bind_all("<FocusOut>", on_focus_out)


  # MAIN GUI LOOP
  root.mainloop()
  root.destroy()    # destroy upon quit if it still exists

  # paste after GUI closes
  if doPaste:
    sleep(.05)  # small delay to allow previously focussed item to regain focus
    hotkey('ctrl', 'v')
    doPaste = False # reset
    




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

  # wait until the named pipe exists
  while not os.path.exists(PIPE_PATH):
    sleep(.5)
    continue

  with open(PIPE_PATH, 'r') as pipe:
    try:
      while True:
        cmd = pipe.readline().strip()
        if cmd:
          commandProcessor(cmd)
    except Exception as err:
      print(f"\nTerminated program with error: {err}")





def clipboardChangeListener():
  previousContent = None
  while True:
    try:
      currentContent = pyperclip.paste()
      if currentContent != previousContent:
        print(type(currentContent))
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

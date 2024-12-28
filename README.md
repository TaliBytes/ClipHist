# Linux Clipboard History Manager (ClipHist)

## WARNING - APP IS STILL IN DEVELOPMENT AND NON FUNCTIONAL

Linux is an open source OS with (typically) minimal bloat pre-installed. This has the obvious advantage of no bloat but has the disadvantage that features one may consider key are simply missing from the experience. Up until recently, I've used Windows in my typical day-to-day work-flow (be it back when I was in school, today as a coder, or at various times I am word processing). I consistently used the Windows "Clipboard History" utility that is built into Windows. Upon moving to Linux I discovered that, not surprisingly, such a feature is not built into the few distros I've tried up till now.

To be straight-forward, I'm not satisfied with any of the existing clipboard managers that have been created for Linux thus far. I find that they're too over-engineered, have what I consider to be built-in bloat, or they have other/similar issues. I need something quite simple, much like the built in option for Windows.

## Features

ClipHist is my attempt at a simple clipboard manager for Linux. Here's what it should do:

1. Copying to the built-in clipboard (`ctrl+c`) should also store the item to ClipHist.
2. Pasting from the built-in clipboard (`ctrl+v`) does not affect ClipHist's stored items (up to 20).
3. A GUI should open using `cmd+v` (aka `super+v`). Historically copied items are navigatable using arrows keys (and enter) or mouse. Selecting an item:
    - Moves it to the "most recent" spot in ClipHist
    - Pastes it into the current selected field
    - "Copies" that item to the system's built-in clipboard
4. The history is stored in active memory. As soon as the user logs out, ClipHist service is stopped/restarted, the computer restarts, etc... all clipboard history is removed. The clipboard history is never stored in any other way on the computer.

## Getting Started

### Prerequisites

ClipHist is built using Python and its sys, pyperclip, tkinter, and threading libraries. Install the following:

```console
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pyperclip
```

### Configure ClipHist

#### A. Setup Background Service

1. Copy the `ClipHist.service` repo file to `/etc/systemd/system/ClipHist.service`

2. Make the following changes:

    - Run `echo $DISPLAY` in your CLI to get your graphic display output. Make sure the `Environment="Display=XX"` lines in ClipHist.service matches the returned value (replace XX with returned value).
    - Update `User=your-username` by replacing "your-username" with your profile name.
    - Update `ExecStart=/usr/bin/python3 /path/to/ClipHist.py` by replacing "path/to/ClipHist.py" to whatever directory ClipHist.py is stored in our your system.

3. Enable the service by running `sudo systemctl enable --now ClipHist.service`
4. Verify the service is working by runnign `journalctl -u ClipHist.service`

If you make a change to the program, run `sudo systemctl restart ClipHist.service`.

#### B. Setup Super Paste Shortcut

1. Copy the `ClipHist.superPaste.trigger.sh` to a directory of your choosing. It is recommended to store this shell script in the same directory as ClipHist.py.

2. To setup the keyboard shortcut (for Linux Mint... other distros may differ):

    - Open **Settings > Keyboard > Shortcuts**
    - Create a new shortcut named **"ClipHist Super Paste"** with the command `/path/to/ClipHist.superPaste.trigger.sh`
    - Enter "cmd+v" (likely to appear as "super+v") to the shortcut. Any other binding will also work.

Now that ClipHist.py and the ClipHist.superPaste.trigger.sh shell script are in place, a keybind is created to execute the shell script, and the ClipHist service is configured and enabled... ClipHist should, in theory, be working correctly.

## Contributing

Contributions are currently not accepted on this project. This may chagne at a later date once the base program is finished.

## License

This project is licensed under the MIT License.

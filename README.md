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

ClipHist is built using Python and its pynput library. Install the following:

```console
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pynput 
```
<!-- libs no longer used -->
<!-- sudo apt install gir1.2-gtk-3.0 libgtk-3-dev -->
<!-- python3-threading python3-gi python3-gi-cairo -->

### Configure Service

Copy the `ClipHist.service` repo file to `/etc/systemd/system/ClipHist.service`.

Make the following changes:

1. Run `echo $DISPLAY` in your CLI to get your graphic display output. Make sure the `Environment="Display=XX"` lines in ClipHist.service matches the returned value (replace XX with returned value).
2. Update `User=your-username` by replacing "your-username" with your profile name.
3. Update `ExecStart=/usr/bin/python3 /path/to/ClipHist.py` by replacing "path/to/ClipHist.py" to whatever directory ClipHist.py is stored in our your system.

Enable the service by running `sudo systemctl enable --now ClipHist.service`. It is recommended to check if the services is working correctly by running `journalctl -u ClipHist.service`.

If you make a change to the program, run `sudo systemctl restart ClipHist.service`.

## Contributing

Contributions are currently not accepted on this project. This may chagne at a later date once the base program is finished.

## License

This project is licensed under the MIT License.

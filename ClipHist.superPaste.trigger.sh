# trigger the super paste command in ClipHist.py upon system settings > keyboard > shortcuts keybind
# config by setting cmd+v keybind to run this shell script ... mark this program as executable using chmod +x /path/to/ClipHist.superPaste.trigger.sh

# creat named pipe for cmd imput (if it already exists, nothing happens)
mkfifo /tmp/ClipHistPipe

# send the command into the pipe
echo "trigger_cmd_v" > /tmp/ClipHistPipe

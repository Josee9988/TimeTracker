#!/bin/bash
NOTES_SCRIPT="TimeTracker"
CURRENT_DIR=$(pwd)

if [ ! -f "$NOTES_SCRIPT" ]; then # check if the compress script file is found
    echo -e "Can not find the ${NOTES_SCRIPT} script"
    exit 1 # it will exit if the compress script file is not found
fi

# checks if the script is executed as root
if [ "$EUID" -ne 0 ]; then # if not it will tell the user and exit
    echo -e "Please run the script as root!"
    echo -e "do: sudo bash $0"
    exit 1
fi

chmod +x $CURRENT_DIR/$NOTES_SCRIPT

ln -svf $CURRENT_DIR/$NOTES_SCRIPT /bin/$NOTES_SCRIPT

echo "You can now use the script anywhere with: ${NOTES_SCRIPT}"

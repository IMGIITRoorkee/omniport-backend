#!/bin/bash

# Clone Shell, with consent
read -p "Clone the shell for IIT Roorkee? (y/N): " CLONE_SHELL
if [ "$CLONE_SHELL" == 'y' -o "$CLONE_SHELL" == 'Y' ]; then
    bash ./scripts/clone/shell.sh
else
    printf "Skipping Shell\n"
fi

# Clone services
bash ./scripts/clone/services.sh

#!/bin/bash

# Import the utility functions
source ./scripts/clone/utils.sh

# Enter the directory to clone into
cd omniport/

# Clone shell
clonerepo   "Shell"     "omniport-shell"                    "shell"

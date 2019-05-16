#!/bin/bash

# Import the utility functions
source ./scripts/clone/utils.sh

# Enter the directory to clone into
cd omniport/

# Clone Formula 1
clonerepo   "Formula 1" "omniport-backend-formula-one"      "formula_one"

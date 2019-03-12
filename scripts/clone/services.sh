#!/bin/bash

# Import the utility functions
source ./scripts/clone/utils.sh

# Enter the directory to clone into
cd omniport/services/

# Clone services except GIF
clonerepo   "Apps"          "omniport-service-apps"             "apps"
clonerepo   "Categories"    "omniport-service-categories"       "categories"
clonerepo   "Comments"      "omniport-service-comments"         "comments"
clonerepo   "Developer"     "omniport-service-developer"        "developer"
clonerepo   "Feed"          "omniport-service-feed"             "feed"
clonerepo   "Groups"        "omniport-service-groups"           "groups"
clonerepo   "Helpcentre"    "omniport-service-helpcentre"       "helpcentre"
clonerepo   "Links"         "omniport-service-links"            "links"
clonerepo   "Notifications" "omniport-service-notifications"    "notifications"
clonerepo   "Settings"      "omniport-service-settings"         "settings"
clonerepo   "Yellow pages"  "omniport-service-yellow-pages"     "yellow_pages"

# Warn the user about the size of the GIF repository
printf "About to clone GIF, which has a huge size due to its assets\n"
printf "If you are on a slow connection, you can skip the cloning\n"
printf "If you are on a fast connection, clone it for an optimal experience\n"

# Clone GIF, with consent
read -p "Clone the service GIF? (y/N): " CLONE_GIF
if [ "$CLONE_GIF" == 'y' -o "$CLONE_GIF" == 'Y' ]; then
    clonerepo   "GIF"           "omniport-service-gif"              "gif"
else
    printf "Skipping GIF\n"
fi

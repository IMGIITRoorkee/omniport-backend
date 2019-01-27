#!/bin/bash

printf "Hello! Greetings from Team Omniport\n"
read -p "Enter app name in lowercase letters, separating words with spaces: " NAME

APP_NAME="${NAME// /_}"
APP_DISPLAY_NAME="$(tr '[:lower:]' '[:upper:]' <<< ${NAME:0:1})${NAME:1}"
APP_PASCAL_NAME="$(echo ${APP_NAME} | sed -r 's/(^|_)([a-z])/\U\2/g')"

# Enter the apps/ directory
cd omniport/apps/

# Clone the template
git clone "https://github.com/IMGIITRoorkee/omniport-app-template.git" ${APP_NAME}
printf "Cloned template successfully\n"

# Enter the app directory
cd ${APP_NAME}

# Restart Git history
rm -rf .git
git init

# Text substitution
sed -i "s/\[\[app_name\]\]/${APP_NAME}/g" config.yml
sed -i "s/\[\[app_display_name\]\]/${APP_DISPLAY_NAME}/g" config.yml
printf "Added ${APP_NAME} & ${APP_DISPLAY_NAME} in config.yml\n"

# Text substitution
sed -i "s/\[\[app_display_name\]\]/${APP_DISPLAY_NAME}/g" README.md
printf "Added ${APP_DISPLAY_NAME} in README.md\n"

# Text substitution
sed -i "s/\[\[app_pascal_name\]\]/${APP_PASCAL_NAME}/g" apps.py
sed -i "s/\[\[app_name\]\]/${APP_NAME}/g" apps.py
sed -i "s/\[\[app_display_name\]\]/${APP_DISPLAY_NAME}/g" apps.py
printf "Added ${APP_PASCAL_NAME}, ${APP_NAME} & ${APP_DISPLAY_NAME} in apps.py\n"

# Text substitution
sed -i "s/\[\[app_name\]\]/${APP_NAME}/g" http_urls.py
printf "Added ${APP_NAME} in http_urls.py\n"

# Add non-code files to VCS
git add config.yml README.md LICENSE .gitignore static/

# Enter the views/ directory
cd views/

# Text substitution
sed -i "s/\[\[app_name\]\]/${APP_NAME}/g" hello_world.py
printf "Added ${APP_NAME} in response_data\n"

# Add all code to VCS
git add ..

# Commit as IMG
git \
    -c user.email=img@iitr.ac.in \
    -c user.name='Information Management Group' \
    commit -m "Initial commit"

# Done!
printf "App created successfully! Happy scrAPIng!\n"

#!/bin/bash

printf "Hello! Greetings from Team Omniport\n"
read -p "Enter app name in lowercase letters, separating words with spaces: " NAME

APP_NAME="${NAME// /_}"
APP_DISPLAY_NAME="$(tr '[:lower:]' '[:upper:]' <<< ${NAME:0:1})${NAME:1}"
APP_PASCAL_NAME="$(echo ${APP_NAME} | sed -r 's/(^|_)([a-z])/\U\2/g')"

# Create a django app inside django-container
#
# Syntax: create_djang_app <app_name> 
create_django_app() {

    CWD=$(pwd)
    CONTAINER_NAME="create_app"
    APP_NAME=$1

    docker run \
        --tty \
        --interactive \
        --rm \
        --userns host \
        --user $(id -u $(whoami)) \
        --mount type=bind,src=${CWD}/omniport,dst=/omniport \
        --name=${CONTAINER_NAME} \
        --env NAME=${CONTAINER_NAME} \
        omniport-django:latest \
        /bin/bash -c "cd apps && django-admin startapp \
        --template=https://github.com/IMGIITRoorkee/omniport-app-template/archive/master.zip \
        ${APP_NAME}"

}

create_django_app ${APP_NAME}
APP_STATUS=$?

# If django app is created successfully, add app name in the template and add the app to VCS
if [[ $APP_STATUS -eq 0 ]];then

    # Enter the apps directory
    cd omniport/apps/${APP_NAME}

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
fi

#!/bin/bash

PORT_LOWER_LIMIT=60000
PORT_UPPER_LIMIT=60031
PREFERRED_PORT=-1

while getopts ":p:" opt; do
    case ${opt} in
        p )
            PREFERRED_PORT=${OPTARG}
            ;;
        \? )
            printf "Bad command: ${OPTARG} is not a valid flag\n"
            printf "Usage: ./scripts/start-the-dj.sh [-p <port>]\n"
            ;;
        : )
            printf "Bad command: ${OPTARG} requires an argument\n"
            printf "Usage: ./scripts/start-the-dj.sh [-p <port>]\n"
            ;;
    esac
done
shift $((OPTIND -1))

# Start the Django server on the specified port
#
# Syntax: start_django_server <port>
start_django_server() {

    PORT=$1

    CWD=$(pwd)
    NAME=${PORT}
    BIND="0.0.0.0:${PORT}"

    docker run \
        --tty \
        --interactive \
        --rm \
        --userns host \
        --user $(id -u $(whoami)) \
        --network=omniport-docker_network \
        --publish ${PORT}:${PORT}/tcp \
        --mount type=bind,src=${CWD}/omniport,dst=/omniport \
        --mount type=bind,src=${CWD}/configuration,dst=/configuration \
        --mount type=bind,src=${CWD}/branding,dst=/branding \
        --mount type=bind,src=${CWD}/static_files,dst=/static_files \
        --mount type=bind,src=${CWD}/media_files,dst=/media_files \
        --mount type=bind,src=${CWD}/web_server_logs,dst=/web_server_logs \
        --name=${NAME} \
        --env SITE_ID=0 \
        omniport-django:latest \
        python /omniport/manage.py runserver ${BIND}
}

if [ ${PREFERRED_PORT} -ne -1 ]; then
    printf "Trying to assign port: ${PREFERRED_PORT}\n"
    docker container ls -a | grep ${PREFERRED_PORT} &> /dev/null
    if [ $? -ne 0 ]; then
        start_django_server ${PREFERRED_PORT} && break 2
    else
        printf "Port ${PREFERRED_PORT} is not available\n"
    fi
else
    printf "Searching for a free port\n"
    for (( i = ${PORT_LOWER_LIMIT} ; i <= ${PORT_UPPER_LIMIT} ; i++ )); do
        printf "Trying to assign port: ${i}\r"
        docker container ls -a | grep ${i} &> /dev/null
        if [ $? -ne 0 ]; then
            printf "\n"
            start_django_server ${i}; break 2
        fi
    done
    printf "Done\n"
fi
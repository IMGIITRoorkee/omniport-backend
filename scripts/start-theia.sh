#!/bin/bash

PORT_LOWER_LIMIT=62000
PORT_UPPER_LIMIT=62031
PREFERRED_PORT=-1

while getopts ":p:" opt; do
    case ${opt} in
        p )
            PREFERRED_PORT=${OPTARG}
            ;;
        \? )
            printf "Bad command: ${OPTARG} is not a valid flag\n"
            printf "Usage: ./scripts/start-theia.sh [-p <port>]\n"
            ;;
        : )
            printf "Bad command: ${OPTARG} requires an argument\n"
            printf "Usage: ./scripts/start-theia.sh [-p <port>]\n"
            ;;
    esac
done
shift $((OPTIND -1))

# Start the Theia server on the specified port
#
# Syntax: start_theia_server <port>
start_theia_server() {

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
        --publish ${BIND}:3000/tcp \
        --mount type=bind,src=${CWD},dst=/home/project \
        --name ${NAME} \
        --env SITE_ID=0 \
        omniport-theia:latest
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
    while :; do
        printf "Searching for a free port\n"
        for (( i = ${PORT_LOWER_LIMIT} ; i <= ${PORT_UPPER_LIMIT} ; i++ )); do
            printf "Trying to assign port: ${i}\r"
            docker container ls -a | grep ${i} &> /dev/null
            if [ $? -ne 0 ]; then
                printf "\n"
                start_theia_server ${i}; break 2
            fi
        done
    done
fi
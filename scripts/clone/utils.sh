# Encore the given string to a URLencoded format
#
# Syntax: urlencode <string>
urlencode() {
    # Preserve current LC_COLLATE
    old_lc_collate=$LC_COLLATE
    
    LC_COLLATE=C
    local length="${#1}"
    for (( i = 0; i < length; i++ )); do
        local c="${1:i:1}"
        case $c in
            [a-zA-Z0-9.~_-]) printf "$c" ;;
            *) printf '%%%02X' "'$c" ;;
        esac
    done

    # Restore the original value
    LC_COLLATE=$old_lc_collate
}

# Clone the given repository from GitHub
#
# Syntax: clonerepo <disply_name> <repo_name> <folder_name>
clonerepo() {
    # Setting required values from arguments
    DISPLAY_NAME=$1
    REPO_NAME=$2
    FOLDER_NAME=$3

    # Clone the given repository
    printf "Cloning ${DISPLAY_NAME}... "
    git clone https://github.com/IMGIITRoorkee/${REPO_NAME}.git ${FOLDER_NAME} &> /dev/null
    printf "done\n"

    # Remove sensitive information from the remote URL
    cd ${FOLDER_NAME}
    git remote set-url origin https://github.com/IMGIITRoorkee/${REPO_NAME}.git
    cd ..
}

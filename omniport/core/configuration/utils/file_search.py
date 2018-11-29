import os


def file_search(files, name, extensions=None):
    """
    Find a file with the given name from a list of files
    :param files: the list of files within which to search for the file
    :param name: the name of the file removing the extension to look for
    :param extensions: the allowed extensions, in order of preference
    :return: the full file name if found, None otherwise
    """

    if extensions is None:
        for file in files:
            file_name, file_extension = os.path.splitext(file)
            if file_name == name:
                return file
    else:
        current_file = None
        current_pos = len(extensions)

        for file in files:
            file_name, file_extension = os.path.splitext(file)
            if (
                    file_name == name
                    and file_extension in extensions
                    and extensions.index(file_extension) < current_pos
            ):
                current_file = file
                current_pos = extensions.index(file_extension)

        return current_file

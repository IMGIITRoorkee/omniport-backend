import logging


def get_logging_function(module_name):
    """
    This function is used to create a logging function for different modules
    in core using the specified logger.
    :param module_name: the module name
    :return: the logging function
    """

    logger = logging.getLogger('core')

    def log(message, log_type='info', user=None):
        """
        Logs the message with user information
        :param message: the message to be logged
        :param log_type: type of event to be logged
        :param user: user responsible for the event
        """

        if user is not None:
            user_information = f'User: {user}({user.id}) '
        else:
            user_information = ''

        getattr(logger, log_type, 'info')(
            f'{[module_name.upper()]} '
            f'{user_information}'
            f'{message}'
        )

    return log

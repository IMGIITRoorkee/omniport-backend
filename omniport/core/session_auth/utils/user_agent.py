from user_agents import parse

from session_auth.constants import device_types


def get_agent_information(user_agent_string):
    """
    Get additional information about the user agent, such as browser and OS
    :param user_agent_string: the user-agent string sent by the browser
    :return: the additional information produced by parsing the string
    """

    user_agent = parse(user_agent_string)
    if user_agent.is_pc:
        device_type = device_types.COMPUTER
    elif user_agent.is_tablet:
        device_type = device_types.TABLET
    elif user_agent.is_mobile:
        device_type = device_types.MOBILE
    else:
        device_type = device_types.UNKNOWN

    return user_agent.browser, user_agent.os, device_type,

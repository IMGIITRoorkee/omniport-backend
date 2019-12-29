from django_redis import get_redis_connection

from base_auth.models import User


CLIENT = get_redis_connection('communication')


def push(token, user_id):
    """
    This function pushes the password recovery token to
    the redis database specified.
    :param token:the token to be pushed.
    :param user_id: Id of user whose password is to be changed.
    :return: The result of push.
    """

    pipe = CLIENT.pipeline(transaction=True)

    pipe.set(
        name=token,
        value=user_id,
        ex=3600,
        nx=True,
    )
    res = pipe.execute()
    return res[0]


def retreive(token):
    """
    This function retrieves the user associated with the recovery token
    from the redis database.
    :param token: Recovery token to be parsed.
    :return: The user associated with the access token.
    """

    pipe = CLIENT.pipeline(transaction=True)

    pipe.get(token)
    res = pipe.execute()

    if not res:
        return None
    user_id = res[0].decode("utf-8")
    user = User.objects.get(id=user_id)

    return user

def delete(token):
    """
    This function deletes the given recovery token from the database.
    :param token: Recovery token to be deleted.
    :return: error or success message
    """

    pipe = CLIENT.pipeline(transaction=True)

    pipe.delete(token)

    res = pipe.execute()
    return res[0]

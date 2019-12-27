from django_redis import get_redis_connection

from base_auth.models import User


client = get_redis_connection('communication')


def push(token, user_id):

    pipe = client.pipeline(transaction=True)

    pipe.set(
        name=token,
        value=user_id,
        ex=3600,
        nx=True,
    )
    res = pipe.execute()
    return res[0]


def retreive(token):
    pipe = client.pipeline(transaction=True)

    pipe.get(token)
    res = pipe.execute()

    if not res:
        return None
    user_id = res[0].decode("utf-8")
    user = User.objects.get(id=user_id)

    return user

def delete(token):
    pipe = client.pipeline(transaction=True)

    pipe.delete(token)

    res = pipe.execute()
    return res[0]

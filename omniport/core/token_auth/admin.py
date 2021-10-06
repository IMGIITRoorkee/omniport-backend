from omniport.admin.site import omnipotence

from token_auth.models import AppAccessToken

omnipotence.register(AppAccessToken)

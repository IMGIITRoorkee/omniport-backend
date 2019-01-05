from base_auth.admin.models.user import UserAdmin
from base_auth.models import User
from omniport.admin.site import omnipotence

omnipotence.register(User, UserAdmin)

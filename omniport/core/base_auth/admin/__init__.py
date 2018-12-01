from base_auth.admin.models.user import UserAdmin
from base_auth.models import User
from kernel.admin.site import omnipotence

omnipotence.register(User, UserAdmin)

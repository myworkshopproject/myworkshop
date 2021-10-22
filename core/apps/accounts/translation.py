import simple_history
from django.contrib.auth.models import Group

from accounts.models import User

simple_history.register(Group, app="accounts")
simple_history.register(User, excluded_fields=["date_joined", "last_login", "password"])

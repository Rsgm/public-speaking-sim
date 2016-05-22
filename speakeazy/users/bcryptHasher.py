from django.conf import Settings
from django.contrib.auth.hashers import BCryptSHA256PasswordHasher


class Bcrypt(BCryptSHA256PasswordHasher):
    rounds = 12

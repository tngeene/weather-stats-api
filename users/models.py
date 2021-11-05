from django.contrib.auth.models import AbstractUser, UserManager

# model definitions


class UserAccountManager(UserManager):
    pass


class UserAccount(AbstractUser):
    objects = UserAccountManager()

# from django.contrib.auth.models import BaseUserManager


# class MyAccountManager(BaseUserManager):
#     def create_user(self, email, username, password=None):
#         if not email:
#             return ValueError("Users must have an email address")
#         if not username:
#             return ValueError("Users must have a name")

#         user = self.model(
#             email=self.normalize_email(email).lower(),
#             username=username,
#             password=password,
#         )

#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_admin(self, email, username, password=None):
#         user = self.create_user(
#             email=self.normalize_email(email),
#             password=password,
#             username=username,
#         )
#         user.is_admin = True
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, username, password=None):
#         user = self.create_user(
#             email=self.normalize_email(email),
#             password=password,
#             username=username,
#         )
#         user.is_staff = True
#         user.is_superuser = True
#         user.save(using=self._db)
#         return user

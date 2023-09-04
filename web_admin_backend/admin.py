from django.contrib import admin
from .models import Lodge, AdminUserRegistration

# Register your models here.
admin.site.register(Lodge)
admin.site.register(AdminUserRegistration)
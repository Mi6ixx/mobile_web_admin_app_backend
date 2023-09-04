from django.contrib import admin
from .models import Lodge, CustomUser

# Register your models here.
admin.site.register(Lodge)
admin.site.register(CustomUser)
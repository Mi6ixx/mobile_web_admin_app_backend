from django.contrib import admin
from .models import CustomUser, Student, Lodge, LodgeAmenity, LodgeReview

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Student)
admin.site.register(Lodge)
admin.site.register(LodgeAmenity)
admin.site.register(LodgeReview)


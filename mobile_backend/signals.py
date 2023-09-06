from django.db.models.signals import post_save, pre_delete
from django.conf import settings
from django.dispatch import receiver
from .models import Student
 
 
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_student(sender, instance, created, **kwargs):
    if created:
        if instance.user_type=='STUDENT':
            Student.objects.create(user=instance)
  
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_student(sender, instance, **kwargs):
        instance.student.save()
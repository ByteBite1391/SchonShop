from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, verbose_name="شماره تماس")
    address = models.TextField(verbose_name="آدرس", blank=True)
    
    class Meta:
        verbose_name = "پروفایل"
        verbose_name_plural = "پروفایل‌ها"
    
    def __str__(self):
        return f"Profile of {self.user.email}"
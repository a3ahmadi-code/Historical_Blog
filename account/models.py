from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    objects = None
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="profiles")
    biography = models.CharField(max_length=1000)
    Profile_photo = models.ImageField(upload_to="profile_photo",null=True,blank=True)

    class Meta:
        verbose_name = "پروفایل"
        verbose_name_plural = "پروفایل ها"


    def __str__(self):
        return str(self.user)
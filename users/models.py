from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import localtime
from PIL import Image



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

class CustomUserPasswordHistory(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    old_pass = models.CharField(max_length=128)
    pass_date = models.DateTimeField()

    @classmethod
    def remember_password(cls, user):
        cls(username=user, old_pass=user.password, pass_date=localtime()).save()
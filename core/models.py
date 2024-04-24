from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# model profilu
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    u_id = models.IntegerField()
    bio = models.TextField(blank=True)
    profile_img = models.ImageField(upload_to='profile_images', default = 'def_prof_pic.png')
    fav_couisine = models.CharField(max_length=60, blank=True)

    def __str__(self):
        return  self.user.username
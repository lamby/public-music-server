from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User)
    nickname = models.CharField(max_length=40, blank=True)

    def __unicode__(self):
        return self.nickname or self.user.username

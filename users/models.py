from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    email = models.EmailField(default='')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100,default='Ivan')
    surname = models.CharField(max_length=100,default='Ivanov')
    father = models.CharField(max_length=100,default='Ivanovich')
    bitcoin_address = models.CharField(max_length=100, default=0x00)
    ethereum_address = models.CharField(max_length=100, default=0x00)
    card_number = models.CharField(max_length=16, default=000000000000)
    passport_number = models.CharField(max_length=20, default='MB0')

    def __str__(self):
        return self.user.username

# Create your models here.

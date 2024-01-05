from django.db import models
# что бы создать связь с встроенной таблицей юзеров надо ее импортировать
from django.contrib.auth.models import User

# Create your models here.

class Account(models.Model):
    gender_choices = (('M','Male'),
                      ('F','Female'),
                      ('N/A','Not answer'))
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    nickname = models.CharField(max_length=100)
    birthdate = models.DateField(null=True)
    gender = models.CharField(choices=gender_choices, max_length=20)
    account_image = models.ImageField(default='default.jpg',
                                      upload_to='account_images')
    address = models.CharField(max_length=100,null=True)
    vk = models.CharField(max_length=100,null=True)
    instagram = models.CharField(max_length=100,null=True)
    telegram = models.CharField(max_length=100,null=True)
    phone = models.CharField(max_length=20,null=True)#,validators=[validate_phone])
    def __str__(self):
        return f"{self.user.username}'s account"

    class Meta:
        ordering = ['user']
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
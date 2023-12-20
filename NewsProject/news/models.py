from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Article(models.Model):
    categories = (
        ('E', 'Economic'),
        ('S', 'Science'),
        ('I', 'IT'),
    )
    # поля
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField('Название', max_length=50, default='')
    anouncement = models.TextField('Аннотация', max_length=250, default='')
    text = models.TextField('Текст новости')
    date = models.DateTimeField('Дата новости', auto_now=True)
    category = models.CharField(choices=categories, max_length=20, verbose_name='Категории')

    # методы моделей
    def __str__(self):
        return f'{self.title} от: {str(self.date)[:10]}'

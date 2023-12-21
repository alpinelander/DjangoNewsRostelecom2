from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Tag(models.Model):
    title = models.CharField(max_length=80)
    status = models.BooleanField(default=True)
    def __str__(self):
        return self.title
    class Meta:
        ordering = ['title','status']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


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
    tags = models.ManyToManyField(to=Tag, blank=True)

    # методы моделей
    def __str__(self):
        return f'{self.title} от: {str(self.date)[:10]}'
# тут встроенный метод мы его переопределяем

    def get_absolute_url(self):
        return f'/news/{self.id}'
# метаданные модели, все что не связано с полями, а связанно с самой моделью

    class Meta:
        ordering = ['date','title']
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'


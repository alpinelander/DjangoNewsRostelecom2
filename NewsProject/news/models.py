from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

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
    slug = models.SlugField()

    # методы моделей
    def __str__(self):
        return f'{self.title} от: {str(self.date)[:10]}'

    def tag_list(self):
        s = ''
        for t in self.tags.all():
            s+=t.title+' '
        return s

# тут встроенный метод мы его переопределяем

    def get_absolute_url(self):
        return f'/news/{self.id}'
# метаданные модели, все что не связано с полями, а связанно с самой моделью
    def get_views(self):
        return self.views.count()
    class Meta:
        ordering = ['date','title']
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def image_tag(self):
        image = Image.objects.filter(article=self)
        print('!!!!',image)
        if image:
            return mark_safe(f'<img src="{image[0].image.url}" height="50px" width="auto" />')
        else:
            return '(no image)'
class Image(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(upload_to='article_images/',null=True,blank=True) #лучше добавить поле default !!!

    def __str__(self):
        return self.title

    def image_tag(self):
        if self.image is not None:
            return mark_safe(f'<img src="{self.image.url}" height="50px" width="auto" />')
        else:
            return '(no image)'

class ViewCount(models.Model):
    article = models.ForeignKey(Article,on_delete=models.CASCADE,
                                related_name='views')
    ip_address = models.GenericIPAddressField()
    view_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=('-view_date',)
        indexes = [models.Index(fields=['-view_date'])]

    def __str__(self):
        return self.article.title
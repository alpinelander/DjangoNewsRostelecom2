from django.contrib import admin
from .models import *
# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    ordering = ['-date','title','author']
    list_display = ['title','author','date', 'symbol_count','image_tag']
    list_filter = ['title','author','date']
    list_display_links = ('date',) # можно как список, а можно как картеж
#    list_editable = ['title']
    readonly_fields = ['author']
    prepopulated_fields = {"slug":("title",)}
    list_per_page = 5
    @admin.display(description='Длина')
    def symbol_count(self, article:Article):
        return f"Кол-во символов: { len(article.text) }"

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['title','status']
    list_filter = ['title','status']

admin.site.register(Article,ArticleAdmin)
# заменяем на декоратор выше, можно будет добавить еще в декоратор параметры
#admin.site.register(Tag,TagAdmin)

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['title','article','image_tag']
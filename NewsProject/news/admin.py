from django.contrib import admin
from django.db.models.functions import Length
from .models import *
# Register your models here.
class ArticleFilter(admin.SimpleListFilter):
    title = 'По длине новости'
    parameter_name = 'text'

    def lookups(self, request, model_admin):
        return [('S',("Короткие, <100 зн.")),
                ('M',("Средние, 100-500 зн.")),
                ('L',("Длинные, >500 зн.")),]

    def queryset(self, request, queryset):
        if self.value() == 'S':
            return queryset.annotate(text_len=Length('text')).filter(text_len__lt=100)
        elif self.value() == 'M':
            return queryset.annotate(text_len=Length('text')).filter(text_len__lt=500,
                                                                     text_len__gte=100)
        elif self.value() == 'L':
            return queryset.annotate(text_len=Length('text')).filter(text_len__gt=500)
class ArticleImageInline(admin.TabularInline):
    model = Image
    extra = 3
    readonly_fields = ('id','image_tag')

class ArticleAdmin(admin.ModelAdmin):
    ordering = ['-date','title','author']
    list_display = ['title','author','date', 'symbol_count','image_tag']
    list_filter = ['title','author','date', ArticleFilter]
    list_display_links = ('date',) # можно как список, а можно как картеж
    search_fields = ['title__icontains','text__icontains']
#    list_editable = ['title']
    readonly_fields = ['author']
    prepopulated_fields = {"slug":("title",)}
    list_per_page = 5
    inlines= [ArticleImageInline,]
    @admin.display(description='Длина')
    def symbol_count(self, article:Article):
        return f"Кол-во символов: { len(article.text) }"

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['title','status']
    list_filter = ['title','status']
    actions =['set_true','set_false']

    @admin.action(description='Активировать выбранные теги')
    def set_true(self,request,queryset):
        amount = queryset.update(status=True)
        self.message_user(request,f'Активировано {amount} тегов')
    @admin.action(description='Деактивировать выбранные теги')
    def set_false(self,request,queryset):
        amount = queryset.update(status=False)
        self.message_user(request,f'Деактивировано {amount} тегов')

admin.site.register(Article,ArticleAdmin)
# заменяем на декоратор выше, можно будет добавить еще в декоратор параметры
#admin.site.register(Tag,TagAdmin)

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['title','article','image_tag']
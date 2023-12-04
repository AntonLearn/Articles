from django.contrib import admin

from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
from .models import Article, ArticleTags, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class ArticleTagsInlineFormset(BaseInlineFormSet):
    def clean(self):
        if len(self.forms) == 0:
            raise ValidationError('Тегов нет. Добавьте хотя бы основной тег!')
        self.count_is_main_tag = 0
        for form in self.forms:
            if form.cleaned_data.get('is_main'):
                self.count_is_main_tag += 1
            if self.count_is_main_tag > 1:
                raise ValidationError('Основных тегов более одного. Оставьте только один основной тег!')
        if self.count_is_main_tag == 0:
            raise ValidationError('Среди тегов основных нет. Отметьте один основной тег!')
        return super().clean()


class ArticleTagsInline(admin.TabularInline):
    model = ArticleTags
    formset = ArticleTagsInlineFormset
    extra = 0


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    inlines = [ArticleTagsInline]
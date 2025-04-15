from django.contrib import admin
from . import models


admin.site.register(models.Category)
admin.site.register(models.ContactUs)
admin.site.register(models.Comment)
admin.site.register(models.SocialMedia)
admin.site.register(models.AboutDynamic)
admin.site.register(models.Like)
@admin.register(models.Article)
class ArticleAdnin(admin.ModelAdmin):
    list_display = ["title","author","published"]
    list_filter = ["author","category"]
    search_fields = ["title","category","body"]


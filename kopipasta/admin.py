from django.contrib import admin

# Register your models here.
from kopipasta.models.Category import Category
from kopipasta.models.Item import Item


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ['name']
    ordering = ['id']


class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'title')
    list_display_links = ['title']
    list_filter = ['category']
    ordering = ['id']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Item, ItemAdmin)

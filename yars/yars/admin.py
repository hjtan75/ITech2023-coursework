from django.contrib import admin
from .models import Category, MenuItem

admin.site.register(Category)
admin.site.register(MenuItem)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'background_image']
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'price', 'category']
from django.shortcuts import render
from .models import Category, MenuItem

def menu(request):
    categories = Category.objects.all()
    menu_items = MenuItem.objects.all()
    context = {'categories': categories, 'menu_items': menu_items}
    return render(request, 'menus/menu.html', context)
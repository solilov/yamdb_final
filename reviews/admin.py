from django.contrib import admin

from .models import Category, Genre, Review, Title, User

# Регистрируем модели в админке

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Title)
admin.site.register(Review)

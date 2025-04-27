from django.contrib import admin


from .models import Category, Location, Post

# ...и регистрируем её в админке:
admin.site.register(Category)
admin.site.register(Location)
admin.site.register(Post)

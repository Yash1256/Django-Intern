from django.contrib import admin

from .models import Author, User

admin.site.register(User)
admin.site.register(Author)

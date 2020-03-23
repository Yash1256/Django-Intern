"""posts URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from registration.views import author, authors_table
from post.views import post, posts_table
from registration.views import Landing


urlpatterns = [
    path('', Landing.as_view(), name="home"),
    path('admin/', admin.site.urls),
    path('auth/', include('registration.urls')),
    path('details/author/<int:aid>', author, name="author"),
    path('details/posts/<int:pid>', post, name="post"),
    path('posts/', posts_table, name="posts"),
    path('authors/', authors_table, name="authors")
]

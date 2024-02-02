from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.title, name="title"),
    path("create/", views.create, name="create"),
    path("search/", views.search_html, name="search"),
    path("search_g/", views.search_form, name="search_g"),
]

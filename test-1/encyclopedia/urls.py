from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.title, name="title"),
    path("search/", views.search_html, name="search"),
    path("search_g/", views.search_form, name="search_g"),
]

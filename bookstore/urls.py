from django.urls import path
from . import views

app_name = 'bookstore'

urlpatterns = [
    path('', views.home, name='home'),
    path('books/', views.book_list, name='book_list'),
]
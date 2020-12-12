
from django.urls import path, include

from items.views import index, list_pics, list_mods, details, like_item, edit, delete, create

urlpatterns = [
    path('', index, name='index'),
    path('pics/', list_pics, name='list pics'),
    path('mods/', list_mods, name='list mods'),
    path('detail/<int:pk>/',details, name='details'),
    path('like/<int:pk>/', like_item, name='like'),
    path('edit/<int:pk>/', edit, name='edit'),
    path('delete/<int:pk>/', delete, name='delete'),
    path('create/', create, name='create'),
    path('', include('accounts.urls')),
]
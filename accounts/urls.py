from django.conf.urls import url
from django.urls import path, include

from accounts.views import user_profile, signup_user, delete_user, edit_user, change_password

urlpatterns = [

    path('', include('django.contrib.auth.urls')),
    path('profile/<int:pk>/', user_profile, name='user profile'),
    path('profile/', user_profile, name='current user profile'),
    path('signup/', signup_user, name='signup user'),
    path('delete_user/<int:pk>/', delete_user, name='delete user'),
    path('edit_user/<int:pk>/', edit_user, name='edit user'),
    url(r'^password/', change_password, name='change_password'),
]

from django.contrib.auth.views import LogoutView
from django.urls import path

from checker.views import profile_view, profile_edit_view, user_register
from .views import UserCreateView, login_view

urlpatterns = [
    path('register/', user_register, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('profile/', profile_view, name='profile'),
    path('profile_edit/', profile_edit_view, name='profile_edit')

]

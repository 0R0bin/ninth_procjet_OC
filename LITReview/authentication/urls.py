from django.urls import path
from . import views

app_name = 'authentication'
urlpatterns = [
    path('', views.login_page, name='login_page'),
    path('signup', views.signup_page, name='signup'),
    path('logout', views.logout_user, name='logout'),
    path('follows', views.follows, name='follows'),
    path('follows/<int:followed_id>/remove', views.remove_followed, name='remove_followed'),
]
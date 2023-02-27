"""LITReview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
import authentication.views
import reviews.views

from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(
            template_name='authentication/login.html',
            redirect_authenticated_user=True),
        name='login'),
    path('logout/', authentication.views.logout_user, name='logout'),
    path('home/', reviews.views.home, name='home'),
    path('signup/', authentication.views.signup_page, name='signup'),
    path('photo/upload/', reviews.views.photo_upload, name='photo_upload'),
    path('reviews/create', reviews.views.review_and_photo_upload, name='review_create'),
    path('review/<int:review_id>', reviews.views.view_review, name='view_review'),
    path('review/<int:review_id>/edit', reviews.views.edit_review, name='edit_review'),
    path('photo/upload-multiple/', reviews.views.create_multiple_photos, name='create_multiple_photos'),
]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

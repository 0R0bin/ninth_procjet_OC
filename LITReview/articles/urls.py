from django.urls import path
from . import views

app_name = 'articles'
urlpatterns = [
    path('flow', views.flow, name='flow'),
    path('posts', views.posts, name='posts'),
    path('details/<int:ticket_id>/', views.detail, name='detail_ticket'),
    path('create', views.ticket_upload, name='create_ticket'),
    path('create_both', views.review_and_ticket_upload, name='create_both'),
    path('details/<int:ticket_id>/edit', views.edit_ticket_view, name='edit_ticket_view'),
]
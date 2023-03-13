from django.urls import path

from . import views

app_name = 'articles'
urlpatterns = [
    path('', views.index, name='index'),
    path('details/<int:ticket_id>/', views.detail, name='detail_ticket'),
    path('create', views.ticket_upload, name='create_ticket'),
    path('details/<int:ticket_id>/edit', views.edit_ticket, name='edit_ticket'),
]
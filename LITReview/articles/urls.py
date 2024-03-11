from django.urls import path
from . import views

app_name = 'articles'
urlpatterns = [
    path('flow', views.flow, name='flow'),
    path('posts', views.posts, name='posts'),
    path('create_review/<int:ticket_id>/', views.create_review, name='create_review'),
    path('del/<int:ticket_id>/', views.del_ticket, name='del_ticket'),
    path('del_review/<int:review_id>/', views.del_review, name='del_review'),
    path('create', views.ticket_upload, name='create_ticket'),
    path('create_both', views.review_and_ticket_upload, name='create_both'),
    path('details/<int:ticket_id>/edit', views.edit_ticket_view, name='edit_ticket_view'),
    path('details/<int:review_id>/edit_review', views.edit_review_view, name='edit_review_view'),
]
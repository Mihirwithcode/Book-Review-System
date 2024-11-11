from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('book/<int:book_id>/review/', views.submit_review, name='submit_review'),
    path('book/new/', views.book_create, name='book_create'),
    path('book/<int:pk>/edit/', views.book_update, name='book_update'), 
    path('book/<int:pk>/delete/', views.book_delete, name='book_delete'),
    path('register/', views.register, name='register'),
    path('profile/', views.user_profile, name='profile')
]

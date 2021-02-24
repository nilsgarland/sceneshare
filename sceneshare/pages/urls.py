from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('upload/', views.upload, name='upload'),
    path('like/', views.like, name='like'),
    path('delete/', views.delete, name='delete'),
    path('scene/<int:scene_id>/', views.scene, name='scene')
]

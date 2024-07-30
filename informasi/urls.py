from django.urls import path
from . import views

urlpatterns = [
    path('kegiatan/', views.kegiatanList, name='kegiatan'),
    path('kegiatan/add/', views.kegiatanCreate, name='kegiatanAdd'),
    path('kegiatan/edit/<int:id>/', views.kegiatanEdit, name='kegiatanEdit'),
    path('kegiatan/delete/<int:id>/', views.kegiatanDelete, name='kegiatanDelete'),
]

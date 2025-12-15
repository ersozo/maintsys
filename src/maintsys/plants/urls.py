from django.urls import path
from . import views

app_name = 'plants'

urlpatterns = [
    path('', views.plant_list, name='plant_list'),
    path('archive/', views.plant_archive, name='plant_archive'),
    path('create/', views.plant_create, name='plant_create'),
    path('<int:pk>/', views.plant_detail, name='plant_detail'),
    path('<int:pk>/edit/', views.plant_edit, name='plant_edit'),
    path('<int:pk>/delete/', views.plant_delete, name='plant_delete'),
    path('<int:pk>/restore/', views.plant_restore, name='plant_restore'),
]


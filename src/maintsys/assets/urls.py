from django.urls import path
from . import views

app_name = 'assets'

urlpatterns = [
    path('', views.asset_list, name='asset_list'),
    path('archive/', views.asset_archive, name='asset_archive'),
    path('create/', views.asset_create, name='asset_create'),
    path('<int:pk>/', views.asset_detail, name='asset_detail'),
    path('<int:pk>/edit/', views.asset_edit, name='asset_edit'),
    path('<int:pk>/delete/', views.asset_delete, name='asset_delete'),
    path('<int:pk>/restore/', views.asset_restore, name='asset_restore'),
]

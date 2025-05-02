from django.urls import path
from . import views

app_name = 'company_profiles'

urlpatterns = [
    path('', views.company_list, name='company_list'),
    path('<int:pk>/', views.company_detail, name='company_detail'),
    path('create/', views.company_create, name='company_create'),
    path('<int:pk>/update/', views.company_update, name='company_update'),
    path('<int:pk>/delete/', views.company_delete, name='company_delete'),
] 
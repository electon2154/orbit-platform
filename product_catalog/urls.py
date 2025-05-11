from django.urls import path
from . import views

app_name = 'product_catalog'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('add/', views.product_create, name='product_create'),
    path('<int:pk>/', views.product_detail, name='product_detail'),
    path('<int:pk>/update/', views.product_update, name='product_update'),
    path('<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('company/<int:company_id>/', views.company_products, name='company_products'),
    path('api/search-products/', views.search_company_products, name='search_company_products'),
] 
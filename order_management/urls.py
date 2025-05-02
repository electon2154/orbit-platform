from django.urls import path
from . import views

app_name = 'order_management'

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('<int:pk>/', views.order_detail, name='order_detail'),
    path('create/', views.order_create, name='order_create'),
    path('<int:pk>/update/', views.order_update, name='order_update'),
    path('<int:pk>/delete/', views.order_delete, name='order_delete'),
    path('<int:pk>/status/', views.order_status_update, name='order_status_update'),
    path('company-orders/', views.company_orders_api, name='company_orders_api'),
    path('create-company-order/', views.create_order_for_company, name='create_company_order'),
    path('create-all/', views.create_all_orders, name='create_all_orders'),
]
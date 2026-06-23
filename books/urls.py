from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('abdurahmonadmin/', views.admin_login, name='admin_login'),
    path('abdurahmonadmin/logout/', views.admin_logout, name='admin_logout'),
    path('abdurahmonadmin/orders/', views.admin_orders, name='admin_orders'),
    path('api/books/add/', views.add_book, name='add_book'),
    path('api/books/<int:pk>/edit/', views.edit_book, name='edit_book'),
    path('api/books/<int:pk>/delete/', views.delete_book, name='delete_book'),
    path('api/books/<int:pk>/data/', views.get_book_data, name='get_book_data'),
    path('api/categories/add/', views.add_category, name='add_category'),
    path('api/categories/<int:pk>/edit/', views.edit_category, name='edit_category'),
    path('api/categories/<int:pk>/delete/', views.delete_category, name='delete_category'),
    path('api/categories/<int:pk>/data/', views.get_category_data, name='get_category_data'),
    path('api/cart/add/', views.cart_add, name='cart_add'),
    path('api/cart/remove/', views.cart_remove, name='cart_remove'),
    path('api/cart/', views.cart_get, name='cart_get'),
    path('api/orders/create/', views.create_order, name='create_order'),
    path('api/admin/orders/<int:pk>/accept/', views.admin_accept_order, name='admin_accept_order'),
    path('api/admin/orders/<int:pk>/reject/', views.admin_reject_order, name='admin_reject_order'),
]

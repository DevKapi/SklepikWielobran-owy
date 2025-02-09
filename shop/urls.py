from django.urls import path
from . import views
from django.contrib.auth import views as auth_views  # Django login/logout

urlpatterns = [
    path('', views.home, name='home'),  # Strona główna
    path('products/', views.product_list, name='product_list'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('products/<int:product_id>/edit/', views.edit_product, name='edit_product'),
    path('products/<int:product_id>/delete/', views.delete_product, name='delete_product'),
    path('orders/', views.order_summary, name='order_summary'),  # Zamówienia 2024-2025

    # Logowanie, rejestracja, wylogowanie
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='shop/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),


    path('cart/', views.cart_view, name='cart_view'),  # Widok koszyka
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),  # Dodanie do koszyka
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),  # Usunięcie produktu
    path('cart/clear/', views.clear_cart, name='clear_cart'),  # Wyczyść koszyk


    path('checkout/', views.checkout, name='checkout'),

    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),

    path('cart/decrease/<int:product_id>/', views.decrease_from_cart, name='decrease_from_cart'),

    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),


]

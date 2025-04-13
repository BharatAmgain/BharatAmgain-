from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Home and authentication
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Menu and ordering
    path('menu/', views.menu, name='menu'),
    path('order/<int:item_id>/', views.place_order, name='place_order'),

    #order_history
    path('order/success/<int:order_id>/', views.order_success, name='order_success'),

    # Registration
    path('register/', views.register, name='register'),
    path('order-history/', views.order_history, name='order_history'),
    # Staff views
    path('dashboard/', views.dashboard, name='dashboard'),
    path('update_status/<int:order_id>/', views.update_order_status, name='update_status'),
    path('manage_menu/', views.manage_menu, name='manage_menu'),

#payment
path('payment/', views.payment_options, name='payment_options'),
]
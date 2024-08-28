from django.urls import path
from .views import (
    CustomUserView, CustomUserDetailView, ManagerMenuItemView,
    ManagerOrderListView, ManagerRoleUpdateView, ManagerUserListView, 
    DeliveryCrewOrderListView, UpdateOrderStatusView, 
    CategoryView, CategoryDetailView, MenuItemView, MenuItemDetail, FeaturedMenuItemView, 
    CartView, CartDetailView, OrderView, OrderDetailView, 
    OrderItemView, OrderItemDetail, TestimonialListCreateView, ReservationListCreateView, AvailableTimesView, ReservationDetailView, PaymentView
)

urlpatterns = [
    path('users/', CustomUserView.as_view(), name='user-list'),
    path('users/<int:pk>/', CustomUserDetailView.as_view(), name='user-detail'),
    path('manager/users/', ManagerUserListView.as_view(), name='manager-user-list'),
    path('manager/users/<int:pk>/roles/', ManagerRoleUpdateView.as_view(), name='manager-role-update'),
    path('manager/orders/', ManagerOrderListView.as_view(), name='manager-order-list'),
    path('manager/menu-items/', ManagerMenuItemView.as_view(), name='manager-menuitem-list'),
    path('delivery-crew/orders/', DeliveryCrewOrderListView.as_view(), name='delivery-crew-order-list'),
    path('delivery-crew/orders/<int:pk>/status/', UpdateOrderStatusView.as_view(), name='update-order-status'),
    path('categories/', CategoryView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('menu-items/', MenuItemView.as_view(), name='menuitem-list'),
    path('featured-menu-items/', FeaturedMenuItemView.as_view(), name='featured-menuitem-list'),
    path('menu-items/<int:pk>/', MenuItemDetail.as_view(), name='menuitem-detail'),
    path('carts/', CartView.as_view(), name='cart-list'),
    path('carts/<int:pk>/', CartDetailView.as_view(), name='cart-detail'),
    path('orders/', OrderView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('order-items/', OrderItemView.as_view(), name='orderitem-list'),
    path('order-items/<int:pk>/', OrderItemDetail.as_view(), name='orderitem-detail'),
    path('payments/', PaymentView.as_view(), name='payment'),
    path('reservations/', ReservationListCreateView.as_view(), name='reservation-list'),
    path('reservations/<int:pk>/', ReservationDetailView.as_view(), name='reservation-detail'),
    path('reservations/available-times/', AvailableTimesView.as_view(), name='available-times'),
    path('testimonial/', TestimonialListCreateView.as_view(), name='testimonial-list'),
]

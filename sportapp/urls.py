from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('item', views.item_list, name='item_list'),
    path('itemcreate', views.item_create, name='item_create'),
    path('turfs', views.turf_list, name='turf_list'),
    path('turfcreate', views.item_create, name='turf_create'),
    path('turfsbooking<int:turf_id>', views.turf_booking, name='turf_booking'),
    path('events', views.event_list, name='event_list'),
    path('eventsbooking<int:event_id>', views.event_booking, name='event_booking'),
    path('academies', views.academy_list, name='academy_list'),
    path('academies/<int:academy_id>/', views.academy_detail, name='academy_detail'),
    path('academies/<int:academy_id>/admission/', views.academy_admission, name='academy_admission'),
    path('academy_checkout/', views.academy_checkout, name='academy_checkout'),
    path('academy_admission_complete/', views.academy_admission_complete, name='academy_admission_complete'),
    path('comments<int:post_id>', views.post_detail, name='post_detail'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),  
    path('equipment/', views.equipment_list, name='equipment'),
    path('booking/confirmation/<int:booking_id>/', views.turf_booked, name='turf_booked'),
    path('add_to_cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),  # Add to cart
    path('cart/', views.view_cart, name='cart'),  # Cart page
    path('update_cart/<int:item_id>/', views.update_cart, name='update_cart'),  # Update cart quantity
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),  # Remove item
    path('checkout/', views.checkout, name='checkout'),  # Checkout page
    path('process_payment/', views.process_payment, name='process_payment'),
    path('events/create/', views.event_create, name='event_create'),
]
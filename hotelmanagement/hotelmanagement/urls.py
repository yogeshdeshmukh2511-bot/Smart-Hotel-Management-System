from django.contrib import admin
from django.urls import path
from hotel.views import home, rooms,guests,bookings,login_view,logout_view,add_room,edit_room,delete_room,add_guest,edit_guest,delete_guest,cancel_booking,booking_history,invoice,complete_booking,gallery

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('rooms/', rooms, name='rooms'),
    path('guests/', guests, name='guests'),
    path('bookings/', bookings, name='bookings'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('add-room/', add_room, name='add_room'),
    path('edit-room/<int:room_id>/', edit_room, name='edit_room'),
    path('delete-room/<int:room_id>/', delete_room, name='delete_room'),
    path('add-guest/', add_guest, name='add_guest'),
    path('edit-guest/<int:guest_id>/', edit_guest, name='edit_guest'),
    path('delete-guest/<int:guest_id>/', delete_guest, name='delete_guest'),
    path('cancel-booking/<int:booking_id>/', cancel_booking, name='cancel_booking'),
    path('booking-history/', booking_history, name='booking_history'),
    path('invoice/<int:booking_id>/', invoice, name='invoice'),
    path('complete-booking/<int:booking_id>/', complete_booking, name='complete_booking'),
    path('gallery/', gallery, name='gallery'),
]

"""
URL configuration for room_reservation_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from booking_management.views import AddRoomView, ShowAllRoomsView, DeleteRoomView, ModifyRoomView, MainMenuView, ReservationView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('room/new', AddRoomView.as_view(), name='add_room'),
    path('rooms/', ShowAllRoomsView.as_view(), name='show_all_rooms'),
    path('rooms/delete/<int:room_id>/', DeleteRoomView.as_view(), name='delete_room'),
    path('rooms/modify/<int:room_id>/', ModifyRoomView.as_view(), name='modify_room'),
    path('', MainMenuView.as_view(), name='main_menu'),
    path('room/reserve/<int:room_id>/', ReservationView.as_view(), name='room_reservation'),
]

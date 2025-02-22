from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.base import View
from booking_management.models import Room


# Create your views here.
class AddRoomView(View):
    def get(self, request):
        return render(request, 'add_room.html')
    def post(self, request):
        room_name = request.POST.get('room_name')
        if not room_name:
            return render(request, 'add_room.html', context={'error': 'No room name'})
        if Room.objects.filter(name=room_name).exists():
            return render(request, 'add_room.html', context={'error': 'Room already exists'})
        room_capacity = int(request.POST.get('room_capacity'))
        if room_capacity < 1:
            return render(request, 'add_room.html', context={'error': 'Capacity must be greater than 0'})
        projector_availability = request.POST.get('projector_availability') == 'on'
        Room.objects.create(name=room_name, room_capacity=room_capacity, projector_availability=projector_availability)
        return redirect('all_rooms')
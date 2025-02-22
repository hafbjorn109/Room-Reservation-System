from sqlite3 import IntegrityError

from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.base import View
from booking_management.models import Room


def validate_room_data(room_name, room_capacity):
    """
    Helper function to validate room data.

    Args:
        room_name (str): The name of the room.
        room_capacity (int): The capacity of the room.

    Returns:
        tuple: (error_message, is_valid) where `is_valid` is a boolean indicating
               if the room data is valid and `error_message` provides an error message.
    """
    if not room_name:
        return "No room name", False
    if Room.objects.filter(name=room_name).exists():
        return "Room already exists", False
    if room_capacity < 1:
        return "Capacity must be greater than 0", False
    return None, True

# Create your views here.
class AddRoomView(View):
    """
    View for adding a new room to the system.

    Methods:
        get(request): Renders the form for adding a new room.
        post(request): Handles form submission to create a new room.
    """
    def get(self, request):
        """
        Renders the form for adding a new room.
        """
        return render(request, 'add_room.html')
    def post(self, request):
        """
        Handles the form submission to create a new room.
        """
        room_name = request.POST.get('room_name')
        room_capacity = int(request.POST.get('room_capacity', 0))  # Default to 0 if not provided
        projector_availability = request.POST.get('projector_availability') == 'on'

        error_message, is_valid = validate_room_data(room_name, room_capacity)
        if not is_valid:
            return render(request, 'add_room.html', context={'error': error_message})

        # Create the room
        try:
            Room.objects.create(name=room_name, room_capacity=room_capacity, projector_availability=projector_availability)
        except IntegrityError:
            return render(request, 'add_room.html', context={'error': error_message})
        return redirect('show_all_rooms')

class ShowAllRoomsView(View):
    """
    View for displaying all the rooms.
    """
    def get(self, request):
        """
        Retrieves and displays all rooms.
        """
        rooms = Room.objects.all()
        if not rooms:
            return render(request, 'show_all_rooms.html', context={'error': 'No rooms'})
        return render(request, 'show_all_rooms.html', context={'rooms': rooms})

class DeleteRoomView(View):
    """
    View for deleting a room from the system.
    """
    def get(self, request, room_id):
        """
        Deletes the room with the given room_id.
        """
        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return render(request, 'show_all_rooms.html', context={'error': 'Room not found'})
        room.delete()
        return redirect('show_all_rooms')

class ModifyRoomView(View):
    """
    View for modifying the details of an existing room.
    """
    def get(self, request, room_id):
        """
        Displays the form to modify the room with the given room_id.
              """
        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return render(request, 'show_all_rooms.html', context={'error': 'Room not found'})
        return render(request, 'modify_room.html', context={'room': room})
    def post(self, request, room_id):
        """
        Handles the form submission to modify the room's details.
        """
        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return render(request, 'show_all_rooms.html', context={'error': 'Room not found'})
        room_name = request.POST.get('room_name')
        room_capacity = int(request.POST.get('room_capacity', 0))  # Default to 0 if not provided
        projector_availability = request.POST.get('projector_availability') == 'on'

        # Validate the room data
        error_message, is_valid = validate_room_data(room_name, room_capacity)
        if not is_valid:
            return render(request, 'modify_room.html', context={'error': error_message, 'room': room})

        # Update the room details
        room.name = room_name
        room.room_capacity = room_capacity
        room.projector_availability = projector_availability
        room.save()

        return redirect('show_all_rooms')

class MainMenuView(View):
    """
    View for rendering the main menu of the application.

    Methods:
        get(request): Renders the main menu page.
    """
    def get(self, request):
        return render(request, 'index.html')
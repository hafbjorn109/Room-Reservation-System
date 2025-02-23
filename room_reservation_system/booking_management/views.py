from datetime import datetime, date

from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.base import View
from booking_management.models import Room, Reservation


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

        Room.objects.create(name=room_name, room_capacity=room_capacity, projector_availability=projector_availability)
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
        for room in rooms:
            reservations = [reservation.date for reservation in room.reservation_set.all()]
            room.reserved = date.today() in reservations
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

class ReservationView(View):
    """
        This view allows users to make reservations for a specific room. It provides
        error handling for the following cases:
        - Room not found.
        - Room already reserved on the selected date.
        - Attempt to reserve a room for a date in the past.

        Attributes:
            room_id (int): The ID of the room being reserved.
        """
    def get(self, request, room_id):
        """
        Retrieves the room details and the list of existing reservations for the room.

        Args:
            request (HttpRequest): The request object.
            room_id (int): The ID of the room being viewed.

        Returns:
            HttpResponse: The rendered reservation form or error page if the room is not found.
        """
        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return render(request, 'show_all_rooms.html', context={'error': 'Room not found'})
        reservations = room.reservation_set.all().order_by('date')
        return render(request, 'room_reservation.html', context={'room': room, 'reservations': reservations})
    def post(self, request, room_id):
        """
        Handles form submission for room reservation, validating the reservation
        date and checking for room availability.

        Args:
            request (HttpRequest): The request object containing form data.
            room_id (int): The ID of the room being reserved.

        Returns:
            HttpResponse: The rendered reservation form with error messages or
                          success redirect to room list.
        """
        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return render(request, 'show_all_rooms.html', context={'error': 'Room not found'})

        reservation_date_str = request.POST.get('date')
        reservations = room.reservation_set.all().order_by('date')

        if Reservation.objects.filter(room_id=room_id, date=reservation_date_str).exists():
            return render(request, 'room_reservation.html', context={'error': 'The room is already booked for this date',
                                                                     'reservations': reservations})
        reservation_date = datetime.strptime(reservation_date_str, '%Y-%m-%d').date()
        if reservation_date < date.today():
            return render(request, 'room_reservation.html', context={'error': 'You cant reserve a room for the past',
                                                                     'reservations': reservations})
        comment = request.POST.get('comment')
        Reservation.objects.create(room_id=room, date=reservation_date, comment=comment)
        return redirect('show_all_rooms')

class RoomDetailsView(View):
    """
    A view to display the details of a specific room.
    """
    def get(self, request, room_id):
        """
        Retrieves the room details and the list of existing reservations for the room.

        Args:
            request (HttpRequest): The request object.
            room_id (int): The ID of the room being viewed.

        Returns:
            HttpResponse: The rendered room details page or error page if the room is not found.
        """
        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return render(request, 'show_all_rooms.html', context={'error': 'Room not found'})
        reservations = room.reservation_set.all().order_by('date')
        return render(request, 'room_details.html', context={'room': room, 'reservations': reservations})

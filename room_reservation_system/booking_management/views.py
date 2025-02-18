from django.shortcuts import render
from django.views.generic.base import View


# Create your views here.
class AddRoomView(View):
    def get(self, request):
        return render(request, 'add_room.html')
    def post(self, request):
        pass
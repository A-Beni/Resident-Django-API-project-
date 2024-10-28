from django.contrib import admin
from .models import Building
from .models import Room
from .models import Resident

admin.site.register(Building)
admin.site.register(Room)
admin.site.register(Resident)

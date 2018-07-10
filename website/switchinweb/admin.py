from django.contrib import admin
from .models import Policy, Coverage, City, State, Vehicle

admin.site.register(Policy)
admin.site.register(Vehicle)
admin.site.register(Coverage)
admin.site.register(State)
admin.site.register(City)

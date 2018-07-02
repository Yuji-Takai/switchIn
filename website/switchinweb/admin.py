from django.contrib import admin
from .models import Policy, Vehicle, Coverage

admin.site.register(Policy)
admin.site.register(Vehicle)
admin.site.register(Coverage)

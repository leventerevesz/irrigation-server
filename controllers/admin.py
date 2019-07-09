from django.contrib import admin

# Register your models here.
from .models import Controller, Channel


admin.site.register(Channel)
admin.site.register(Controller)
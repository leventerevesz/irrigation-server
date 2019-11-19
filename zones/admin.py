from django.contrib import admin

# Register your models here.
from .models import Zone

class ZoneAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

admin.site.register(Zone, ZoneAdmin)
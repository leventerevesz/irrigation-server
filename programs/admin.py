from django.contrib import admin

from .models import Program

class ProgramAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'program_type', 'priority', 'adaptivity', 'enabled')

admin.site.register(Program, ProgramAdmin)

from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(DownloadMaterials)
class DownloadMaterialsAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at')

admin.site.register(Gallery)

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_time', 'end_time', 'is_event_active')

admin.site.register(Event, EventAdmin)

admin.site.register(LandingPageText)
admin.site.register(StudentAdmission)



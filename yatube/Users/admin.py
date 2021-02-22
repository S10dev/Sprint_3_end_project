from django.contrib import admin
from .models import Disk

# Register your models here.
class DiskAdmin(admin.ModelAdmin):
    list_display = ("pk", "artist")
    search_fields = ("artist",) 
    list_filter = ("artist",) 
    empty_value_display = "-пусто-"


admin.site.register(Disk, DiskAdmin)
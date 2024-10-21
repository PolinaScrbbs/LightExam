from django.contrib import admin
from .models import UploadedFile

@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'file', 'upload_date', 'is_video')
    search_fields = ('file',)
    list_filter = ('is_video', 'upload_date')

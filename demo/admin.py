from django.contrib import admin

from . import models as m


# Register your models here.
@admin.register(m.UploadFile)
class UploadFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'attachment')

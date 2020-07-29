from django.contrib import admin

# Register your models here.
from tagging_system import models

admin.site.register(models.Images)
admin.site.register(models.Tags)

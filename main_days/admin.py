from django.contrib import admin

from .models import StrVar, NumVar, OffDay, WorkDay

admin.site.register(StrVar)
admin.site.register(NumVar)
admin.site.register(OffDay)
admin.site.register(WorkDay)

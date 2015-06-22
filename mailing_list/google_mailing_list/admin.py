from django.contrib import admin
from .models import Staff
from .models import MailingList
# from .models import CreateMailingList


class StaffAdmin(admin.ModelAdmin):
    list_display=('first_name', 'last_name', 'email')
    list_filter=['first_name', 'last_name']
    search_fields=['first_name', 'last_name']

class MailingListAdmin(admin.ModelAdmin):
    list_display=('name',)

admin.site.register(Staff, StaffAdmin)
admin.site.register(MailingList,MailingListAdmin)
from django.contrib import admin

from send_mail.models import Contact


@admin.register(Contact)
class PostAdmin(admin.ModelAdmin):
    list_display = ('email', 'date')

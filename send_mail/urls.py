from django.urls import path
from send_mail.views import ContactView

urlpatterns = [
    path('', ContactView.as_view(), name='contact_email')
]

from django.urls import path
from send_mail.views import ContactView, SendLetters

urlpatterns = [
    path('', ContactView.as_view(), name='contact_email'),
    path('send/', SendLetters.as_view(), name='send_emails')
]

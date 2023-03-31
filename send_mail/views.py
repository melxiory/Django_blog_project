from django.views.generic import CreateView

from send_mail.models import Contact
from send_mail.forms import ContactForm


class ContactView(CreateView):
    model = Contact
    form_class = ContactForm
    success_url = '/'


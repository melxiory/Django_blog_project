from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.views import View
from django.views.generic import CreateView

from django.core.mail import send_mail, send_mass_mail

from blog.models import Post
from send_mail.models import Contact
from send_mail.forms import ContactForm


class ContactView(CreateView):
    model = Contact
    form_class = ContactForm
    success_url = '/'


class SendLetters(View):
    def get(self, request, *args, **kwargs):
        list_emails = [e.email for e in Contact.objects.all()] + [e.email for e in User.objects.only('email')]
        list_posts = Post.objects.all()[:3]
        datatuple = []
        for email in list_emails:
            datatuple.append(
                ('Новости на сегодня!!', f'{", ".join([f"http://127.0.0.1:8000/{s.slug}" for s in list_posts])}',
                 'melxiory@example.com', [email]))
        send_mass_mail(datatuple)
        return HttpResponseRedirect('/admin/')

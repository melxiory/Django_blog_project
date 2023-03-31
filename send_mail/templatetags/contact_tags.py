from django import template
from send_mail.forms import ContactForm

register = template.Library()


@register.inclusion_tag('send_mail/tags/subscribe.html')
def contact_form():
    return {'contact_form': ContactForm()}

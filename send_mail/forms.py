from django import forms

from send_mail.models import Contact


class ContactForm(forms.ModelForm):
    email = forms.EmailField(label='', widget=forms.TextInput(attrs={'class': 'form-control',
                                                                     'id': "colFormLabel",
                                                                     'placeholder': 'Enter Your Email'
                                                                     }))

    class Meta:
        model = Contact
        fields = ('email',)

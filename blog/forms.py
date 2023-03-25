from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from blog.models import Comment


class SigUpForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'id': "inputUsername",
            'placeholder': "Имя пользователя"
        }),
    )

    email = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'id': "inputEmail",
            'placeholder': "E-mail"
        }),
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': "form-control",
            'id': "inputPassword",
            'placeholder': "Пароль"
        }),
    )
    repeat_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': "form-control",
            'id': "ReInputPassword",
            'placeholder': "Повторите пароль"
        }),
    )

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['repeat_password']

        if password != confirm_password:
            raise forms.ValidationError(
                "Пароли не совпадают"
            )

    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
        )
        user.save()
        auth = authenticate(**self.cleaned_data)
        return auth


class SignInForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'id': "inputUsername",
        })
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': "form-control mt-2",
            'id': "inputPassword",
        })
    )


class FeedBackForm(forms.Form):
    full_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'full_name',
            'placeholder': "ФИО"
        })
    )
    email = forms.CharField(
        max_length=100,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'id': 'email',
            'placeholder': "Ваша почта"
        })
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control md-textarea',
            'id': 'message',
            'rows': 2,
            'placeholder': "Ваше сообщение",
            'style': "height: 100px"
        })
    )
    CATEGORY_CHOICES = [
        ('none', '-'),
        ('comment', 'Комментарий'),
        ('post', 'Пост'),
        ('account', 'Учетная запись'),
    ]
    subject = forms.CharField(
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'subject',
        }, choices=CATEGORY_CHOICES)
    )

#
# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = ('text',)
#         widgets = {
#             'text': forms.Textarea(attrs={
#                 'class': 'form-control',
#                 'rows': 3
#             }),
#         }

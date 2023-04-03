from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from blog.models import Comment, Profile, Post


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError('Email адрес должен быть уникальным')
        return email


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('location', 'birth_date', 'bio', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })


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


class CommentCreateForm(forms.ModelForm):
    parent = forms.IntegerField(widget=forms.HiddenInput, required=False)
    content = forms.CharField(label='', widget=forms.Textarea(
        attrs={'cols': 30, 'rows': 5, 'placeholder': 'Комментарий', 'class': 'form-control'}))

    class Meta:
        model = Comment
        fields = ('content',)


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'slug', 'category', 'tag', 'content', 'image', 'status')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off'})

        self.fields['content'].widget.attrs.update({'class': 'form-control ckeditor'})
        self.fields['content'].required = False


class PostUpdateForm(PostCreateForm):
    class Meta:
        model = Post
        fields = PostCreateForm.Meta.fields

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields['content'].widget.attrs.update({'class': 'form-control ckeditor'})
        self.fields['content'].required = False

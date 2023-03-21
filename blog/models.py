from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    bio = models.TextField(max_length=500, blank=True, verbose_name='О себе')
    location = models.CharField(max_length=30, blank=True, verbose_name='Местонахождение')
    birth_date = models.DateField(null=True, blank=True, verbose_name='День рождения')
    avatar = models.ImageField(verbose_name='Аватар')

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Профиль'
        verbose_name = 'Профиль'


class Category(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название')
    description = models.CharField(max_length=250, verbose_name='Описание')
    image = models.ImageField(verbose_name='Иконка')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категории'
        verbose_name_plural = 'Категории'


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=200, verbose_name='Название')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    slug = models.SlugField(max_length=200, unique_for_date='publish', verbose_name='Слаг')
    tag = TaggableManager(verbose_name='Тэг')
    content = RichTextUploadingField(verbose_name='Содержание')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts', verbose_name='Автор')
    image = models.ImageField(verbose_name='Картинка')
    numb_of_views = models.IntegerField(default=0, verbose_name='Количество просмотров')
    created_at = models.DateField(default=timezone.now, verbose_name='Дата создания')
    update_at = models.DateField(auto_now=True, verbose_name='Дата обновления')
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft', verbose_name='Статус')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Пост'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='Пост')
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_name', verbose_name='Автор')
    content = models.TextField('Содержание', max_length=500, default='')
    created_date = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')
    parent = models.ForeignKey(
        'self',
        default=None,
        blank=True, null=True,
        on_delete=models.CASCADE,
        related_name='parent_%(class)s',
        verbose_name='Родительский комментарий'
    )

    class Meta:
        verbose_name = 'Комментарии'
        ordering = ['-created_date']
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.post.title

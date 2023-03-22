from django.contrib import admin
from blog.models import Profile, Category, Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'created_at', 'status')
    list_filter = ('status', 'created_at', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'created_at'
    ordering = ('status', 'created_at')


@admin.register(Profile)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'birth_date')
    list_filter = ('location', 'birth_date')
    search_fields = ('user', 'location', 'birth_date')
    ordering = ('user',)


@admin.register(Category)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_filter = ('title',)
    search_fields = ('title',)
    ordering = ('title',)


@admin.register(Comment)
class PostAdmin(admin.ModelAdmin):
    list_display = ('post', 'username', 'created_date')
    list_filter = ('post', 'username', 'created_date')
    search_fields = ('username', 'created_date')
    ordering = ('created_date',)

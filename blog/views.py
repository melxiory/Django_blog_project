from django.contrib.auth import login, authenticate
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponseRedirect, BadHeaderError, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.core.paginator import Paginator
from taggit.models import Tag
from blog.models import Category, Post, Comment
from .forms import SignInForm, SigUpForm, FeedBackForm


class MainView(View):
    def get(self, request, *args, **kwargs):
        five_posts = Post.objects.all()[:5]
        best_post_today = Post.objects.all()[1]
        best_post_week = Post.objects.all()[:3]
        categories = Category.objects.all()
        four_authors = User.objects.all()[:4]

        return render(request, 'blog/home.html', context={
            'five_posts': five_posts,
            'best_post_today': best_post_today,
            'best_post_week': best_post_week,
            'categories': categories,
            'four_authors': four_authors
        })


class AuthorPage(View):
    def get(self, request, user_name, *args, **kwargs):
        username = get_object_or_404(User, username=user_name)
        author = User.objects.get(username=username)
        my_posts = Post.objects.filter(author=author.id)

        return render(request, 'blog/author_page.html', context={
            'my_posts': my_posts,
            'author': author,
        })


class PostsView(View):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()
        paginator = Paginator(posts, 6)
        best_post_today = Post.objects.all()[1]
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'blog/posts.html', context={
            'page_obj': page_obj,
            'best_post_today': best_post_today
        })


class PostDetailView(View):
    def get(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        common_tags = Post.tag.most_common()
        last_posts = Post.objects.all().order_by('-id')[:3]
        return render(request, 'blog/post_details.html', context={
            'post': post,
            'common_tags': common_tags,
            'last_posts': last_posts,
        })

    # def post(self, request, slug, *args, **kwargs):
    #     comment_form = CommentForm(request.POST)
    #     if comment_form.is_valid():
    #         text = request.POST['text']
    #         username = self.request.user
    #         post = get_object_or_404(Post, url=slug)
    #         comment = Comment.objects.create(post=post, username=username, text=text)
    #         return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    #     return render(request, 'blog/post_details.html', context={
    #         'comment_form': comment_form
    #     })


class SignUpView(View):
    def get(self, request, *args, **kwargs):
        form = SigUpForm()
        return render(request, 'blog/signup.html', context={
            'form': form,
        })

    def post(self, request, *args, **kwargs):
        form = SigUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
        return render(request, 'blog/signup.html', context={
            'form': form,
        })


class SignInView(View):
    def get(self, request, *args, **kwargs):
        form = SignInForm()
        return render(request, 'blog/signin.html', context={
            'form': form,
        })

    def post(self, request, *args, **kwargs):
        form = SignInForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
        return render(request, 'blog/signin.html', context={
            'form': form,
        })


class PrivacyPolicy(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'blog/privacy_policy.html')


class FeedBackView(View):
    def get(self, request, *args, **kwargs):
        form = FeedBackForm()
        return render(request, 'blog/contact.html', context={
            'form': form,
        })

    def post(self, request, *args, **kwargs):
        form = FeedBackForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            from_email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            subject = form.cleaned_data['subject']
            try:
                send_mail(f'От {full_name} | {subject}', message, from_email, ['sibagatullinnail@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Невалидный заголовок')
            return HttpResponseRedirect('/')
        return render(request, 'blog/contact.html', context={
            'form': form,
        })


class AboutUSView(View):
    def get(self, request, *args, **kwargs):
        four_authors = User.objects.all()[:4]
        return render(request, 'blog/about_us.html', context={
            'four_authors': four_authors
        })


class SearchResultsView(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('q')
        results = ""
        if query:
            results = Post.objects.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            )
        paginator = Paginator(results, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'blog/search.html', context={
            'title': 'Поиск',
            'page_obj': page_obj,
            'count': paginator.count
        })


class TagView(View):
    def get(self, request, slug, *args, **kwargs):
        tag = get_object_or_404(Tag, slug=slug)
        posts = Post.objects.filter(tag=tag)
        paginator = Paginator(posts, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        common_tags = Post.tag.most_common()
        categories = Category.objects.all()[:6]
        return render(request, 'blog/tag.html', context={
            'title': f'#ТЕГ {tag}',
            'page_obj': page_obj,
            'common_tags': common_tags,
            'categories': categories,
        })


class CategoryView(View):
    def get(self, request, slug, *args, **kwargs):
        category = get_object_or_404(Category, slug=slug)
        posts = Post.objects.filter(category=category)
        paginator = Paginator(posts, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        common_tags = Post.tag.most_common()
        categories = Category.objects.all()[:6]
        return render(request, 'blog/categories.html', context={
            'title': category,
            'page_obj': page_obj,
            'common_tags': common_tags,
            'categories': categories,
        })

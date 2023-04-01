from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponseRedirect, BadHeaderError, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.core.paginator import Paginator
from django.views.generic import CreateView, UpdateView
from taggit.models import Tag
from blog.models import Category, Post, Comment, Profile
from .forms import SignInForm, SigUpForm, FeedBackForm, CommentCreateForm, ProfileUpdateForm, UserUpdateForm, \
    PostCreateForm, PostUpdateForm


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
        posts = Post.objects.filter(author=author.id)
        paginator = Paginator(posts, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'blog/author_page.html', context={
            'page_obj': page_obj,
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


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentCreateForm

    def form_invalid(self, form):
        return super().form_invalid(form)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.post_id = self.kwargs.get('pk')
        comment.author = self.request.user
        comment.parent_id = form.cleaned_data.get('parent')
        comment.save()

        return redirect(comment.post.get_absolute_url())


class PostDetailView(View):
    def get(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        common_tags = Post.tag.most_common()
        last_posts = Post.objects.all().order_by('-id')[:3]
        comment_form = CommentCreateForm()
        return render(request, 'blog/post_details.html', context={
            'post': post,
            'common_tags': common_tags,
            'last_posts': last_posts,
            'form': comment_form
        })


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


class ProfileDetailView(View):
    def get(self, request, pk, *args, **kwargs):
        user = get_object_or_404(User, pk=pk)
        posts = Post.objects.filter(author=user.pk)
        paginator = Paginator(posts, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'blog/profile_detail.html', context={
            'page_obj': page_obj,
            'user': user,
        })


class ProfileUpdateView(UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'blog/profile_edit.html'

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Редактирование профиля пользователя: {self.request.user.username}'
        if self.request.POST:
            context['user_form'] = UserUpdateForm(self.request.POST, instance=self.request.user)
        else:
            context['user_form'] = UserUpdateForm(instance=self.request.user)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        user_form = context['user_form']
        with transaction.atomic():
            if all([form.is_valid(), user_form.is_valid()]):
                user_form.save()
                form.save()
            else:
                context.update({'user_form': user_form})
                return self.render_to_response(context)
        return super(ProfileUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profile_detail', kwargs={'slug': self.object.slug})


class PostCreateView(CreateView):

    model = Post
    template_name = 'blog/post_create.html'
    form_class = PostCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление статьи на сайт'
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)


class PostUpdateView(UpdateView):

    model = Post
    template_name = 'blog/post_update.html'
    context_object_name = 'post'
    form_class = PostUpdateForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Обновление статьи: {self.object.title}'
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

from django.contrib.auth.views import LogoutView
from Django_blog_project import settings
from django.urls import path, include
from blog.views import *

urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('blog/', PostsView.as_view(), name='posts'),
    path('blog/<slug>/', PostDetailView.as_view(), name='post_detail'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('signout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='signout'),
    path('contact/', FeedBackView.as_view(), name='contact'),
    path('success/', AboutUSView.as_view(), name='about_us'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('tag/<slug:slug>/', TagView.as_view(), name="tag"),
    path('category/<slug:slug>/', CategoryView.as_view(), name="category"),
    path('privacy-policy/', PrivacyPolicy.as_view(), name='privacy_policy'),
    path('<str:user_name>', AuthorPage.as_view(), name='author_page'),
    path('blog/<int:pk>/comments/create/', CommentCreateView.as_view(), name='comment_create_view'),
    path('user/edit/', ProfileUpdateView.as_view(), name='profile_edit'),
    path('user/<int:pk>/', ProfileDetailView.as_view(), name='profile_detail'),
    path('post/create/', PostCreateView.as_view(), name='post_create'),
    path('post/<str:slug>/update/', PostUpdateView.as_view(), name='post_update'),
    path('post/<str:slug>/delete/', PostDeleteView.as_view(), name='post_delete'),
]

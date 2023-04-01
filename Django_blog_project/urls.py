from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from Django_blog_project import settings

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('ckeditor/', include('ckeditor_uploader.urls')),
                  path('send_mail/', include('send_mail.urls')),
                  path('', include('blog.urls')),
              ]


if settings.DEBUG:
    urlpatterns = [path('__debug__/', include('debug_toolbar.urls'))] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from Django_blog_project import settings

urlpatterns = [
                  path('__debug__/', include('debug_toolbar.urls')),
                  path('admin/', admin.site.urls),
                  path('ckeditor/', include('ckeditor_uploader.urls')),
                  path('send_mail/', include('send_mail.urls')),
                  path('', include('blog.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

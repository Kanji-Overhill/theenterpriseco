from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^djangoadmin/', include(admin.site.urls)),
    url(r'^', include("home.urls"))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

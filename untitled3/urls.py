from django.contrib import admin
from django.conf.urls import include, url
from django.urls import path

urlpatterns = [
    url(r'^twitter/', include('twitter.urls')),
    url(r'^twitter/', include('social_django.urls', namespace='social')),
    url(r'^admin/', admin.site.urls),

]


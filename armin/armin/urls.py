"""armin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import django
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path , include
from accont.views import Login


app_name = 'armin'
urlpatterns = [
    path("login/", Login.as_view(), name="login"),
    path("", include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('',include('web.urls')),
    path('account/',include('accont.urls')),
    path('comment/', include('comment.urls')),
    path('ratings/', include('star_ratings.urls', namespace='ratings')),
]


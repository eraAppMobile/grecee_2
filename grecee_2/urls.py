"""grecee_2 URL Configuration

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
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect

from django.urls import path, include

from grecee_2 import settings
from main.views import logout_user

urlpatterns = [
    path('logout/', logout_user, name='logout'),

    path('admin/logout/', lambda request: redirect('/logout/', permanent=False)),
    path('admin/', admin.site.urls),

    path('', include('main.urls')),

    # re_path(r'^registration/?$', RegistrationAPIView.as_view(), name='user_registration'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = "main.views.page_not_found"
admin.autodiscover()

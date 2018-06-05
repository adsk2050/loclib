"""loclib URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib import admin, auth
from django.urls import include, path
# Use static() to add url mapping to serve static files during development (only)
from django.conf import settings
from django.conf.urls.static import static
#from . import blog, catalog, downloads, main, wiki

urlpatterns = [
    path('admin/', admin.site.urls),
]


urlpatterns += [
    path('main/', include('main.urls')),
    path('catalog/', include('catalog.urls')),
    path('downloads/', include('downloads.urls')),
    path('wiki/', include('wiki.urls')),
    path('blog/', include('blog.urls')),
    path('uauth/', include('uauth.urls')),
]

#urlpatterns += [
#    path('accounts/', include(auth.urls)),
#]


#Add URL maps to redirect the base URL to our application
from django.views.generic import RedirectView
urlpatterns += [
    path('', RedirectView.as_view(url='/catalog/', permanent=True)),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

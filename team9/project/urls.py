"""webapps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from project import views

urlpatterns = [
    url(r'^$', views.cover, name='cover'),
    url(r'^home$', views.home, name='home'),
    url(r'^login$', auth_views.login, {'template_name':'project/login.html'}, name='login'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^register$', views.register, name='register'),
    url(r'^profile-overview$', views.edit_overview, name='edit-overview'),
    url(r'^sendRouteText$', views.sendRouteText, name='sendRouteText'),
    url(r'^edit-name$', views.edit_name, name='edit-name'),
    url(r'^change-password$', views.change_password, name='change-password'),
    url(r'^sendVerifyCode/(?P<phoneNum>\w+)$', views.sendVerifyCode, name = 'sendVerifyCode'),
    url(r'^add-favorite-location$', views.add_fav_lo, name="add-fav-lo"),
]

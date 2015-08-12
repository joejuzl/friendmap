from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from friendmap import settings
from friendmap.views import (users, login_user, logout_user, friends, login_form, friend_page, admin_page, whoami,
                             all_connections)

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login_form', login_form, name='login_form'),
    url(r'^admin_page', admin_page, name='admin_page'),
    url(r'^user', users, name='user'),
    url(r'^friend', friends, name='friend'),
    url(r'^whoami', whoami, name='whoami'),
    url(r'^all_connections', all_connections, name='whoami'),
    url(r'^login_user', login_user, name='login'),
    url(r'^logout_user', logout_user, name='logout'),
    url(r'^', friend_page, name='friend_page'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


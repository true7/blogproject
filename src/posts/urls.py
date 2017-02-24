from django.conf.urls import url

from .views import (
    post_list,
    post_detail,
    post_create,
    post_like,
    )

urlpatterns = [
    url(r'^$', post_list, name='list'),
    url(r'^create/$', post_create, name='create'),
    url(r'^post/(?P<id>\d+)/like/$', post_like, name='like'),
    url(r'^post/(?P<id>\d+)/$', post_detail, name='detail'),
]
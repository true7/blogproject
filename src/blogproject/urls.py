from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView

from accounts.views import login_view, logout_view, register_view, activate

urlpatterns = [
    
    url(r'^admin/', admin.site.urls),
    url(r'^confirm/$', TemplateView.as_view(template_name='confirm.html'), name='confirm'),
    url(r'^activate/(?P<id>\d+)/$', activate, name='activate'),
    url(r'^register/', register_view, name='register'),
    url(r'^login/', login_view, name='login'),
    url(r'^logout/', logout_view, name='logout'),
    url(r'^', include("posts.urls", namespace='posts')),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
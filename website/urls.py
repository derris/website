from django.conf.urls import patterns, include, url
from django.contrib import admin
from App import views
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'website.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^App/1/', views.test1,name='test1'),
    url(r'^notstatic/js/ueditor/controller', views.dealPAjax,name='dealPAjax'),
)

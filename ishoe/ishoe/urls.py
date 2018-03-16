"""ishoe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from info import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/$', admin.site.urls),
    url(r'^list/$',views.state_list),
    url(r'^sign-up/$',views.info_detail),
    url(r'^submit/$',views.submit),
    url(r'^head/$',views.get_head),
    url(r'^left/$',views.get_left),
    url(r'^index/$',views.get_index),
    url(r'^ajax/$',views.ajax_list),
    url(r'^person/$',views.handle_person),
    url(r'^add_person/$',views.add_person),
    url(r'^del_person/$',views.delete_person),
    url(r'^update_person/$',views.update_person),
    url(r'^device/$',views.handle_device),
    url(r'^add_device/$',views.add_device),
    url(r'^del_device/$',views.del_device),
    url(r'^update_device/$',views.update_device),
    url(r'^change_status/$',views.change_status),
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

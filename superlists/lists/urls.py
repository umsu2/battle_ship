from django.conf.urls import url
from django.contrib import admin
from lists import views

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^(\d+)/$', views.view_list, name= "view_list"),
    url(r'^new$', views.new_list, name= "new_list"),
    url(r'^(\d+)/add_item$', views.add_item, name= "add_item")
]
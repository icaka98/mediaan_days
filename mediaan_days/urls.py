from django.contrib import admin
from django.urls import path, include, re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^days/$', include('main_days.urls')),
    path(r'', include('main_days.urls'))
]

from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.index, name='index_only'),
    re_path(r'^days/add_day/$', views.add_work_day, name='add_work_day'),
    re_path(r'^days/add_off_days/$', views.add_from_to, name='add_from_to')
]
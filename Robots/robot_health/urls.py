# -*- coding:utf-8 -*-
from django.urls import path, re_path

from robot_health import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('robots_list/', views.robots_list, name='robots_list'),
    path('add_robot/', views.add_robot, name='add_robot'),
    path('add_datas/', views.add_datas, name='add_datas'),
    re_path(r'^del_robot/(?P<r_num>\d{5})/$', views.del_robot, name='del_robot'),
    re_path(r'^query_rotate_speed/(?P<r_num>\d{5})/$', views.query_rotate_speed, name='query_rotate_speed'),
]

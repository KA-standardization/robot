import glob
import datetime
import threading
import time

import numpy as np
import pandas as pd
from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from robot_health.funcs.coroutine_ import Task, task, loop
from robot_health.models import RobotNun, Actions
from robot_health.funcs.f_echarts import echarts, line_base


def index(request):
    """主页面"""
    return render(request, 'index.html')


@csrf_exempt
def add_robot(request):
    """添加机器人"""
    if request.method == 'POST':
        r = RobotNun()
        data = request.POST
        r.number = data['number']
        r.state = data.get('state', 'on')
        r.save()
    return render(request, 'add_robot.html')


def add_datas(request):
    """添加机器人对应的数据，以Excel导入，可同时导入多个文件，入数据库实现异步，可以浏览其他页面"""
    total = 0
    if request.method == 'POST':
        f_s = request.FILES.getlist('file')
        for f in f_s:
            with open(f"./robot_health/datas/{str(time.time())}.xlsx", 'wb') as save_file:
                for part in f.chunks():
                    save_file.write(part)
                    save_file.flush()
        s_time = time.time()

        def save_data(fut, path):
            def inner():
                nonlocal total
                df = pd.read_excel(path)
                a_ = [Actions(action=item[0], time_set=item[1], r_num_id=item[2]) for item in
                      zip(list(df['action'].astype(np.int32)), list(df['time_set']),
                          list(df['r_num'].astype(np.int32)))]
                Actions.objects.bulk_create(a_)
                fut.set_res(1)
                total += 1
                if total == 10:
                    loop.call_later(2.1, loop.stop)

            threading.Thread(target=inner).start()

        for src in glob.glob('./robot_health/datas/*'):
            t = Task(task(save_data, src))
            print(t)

        loop.run()
        print(time.time() - s_time)
    return render(request, 'add_datas.html')


def del_robot(request, r_num):
    """删除机器人，对应的数据表也会删除"""
    RobotNun.objects.get(number=r_num).delete()
    return render(request, 'index.html')


def query_rotate_speed(request, r_num):
    """查询机器人并生成折线图"""
    r = RobotNun.objects.get(number=r_num)
    d = r.actions_set.order_by('time_set').all()

    tmp_data = dict()
    for item in d:
        tmp_data.update({item.time_set: item.action})

    data = {
        "high": [1500 for _ in range(d.count())],
        "low": [100 for _ in range(d.count())],
        "attr": list(tmp_data.keys()),
        "val_1": list(tmp_data.values()),
    }
    echarts(data, line_base)
    return render(request, 'echarts.html')


def robots_list(request):
    """现有机器人列表"""
    robots = RobotNun.objects.all()
    return render(request, 'list.html', context=locals())

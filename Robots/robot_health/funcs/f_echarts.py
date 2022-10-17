# -*- coding:utf-8 -*-
import string
import datetime

import pyecharts.options as opts
from pyecharts.charts import Line


def line_base(data):
    template = 'Line().add_xaxis($attr).add_yaxis("正常上限", $high).add_yaxis("正常下线", $low)'
    for i in range(len(data) - 3):
        template += f'.add_yaxis("r_num: {i + 1}", $val_{i + 1})'
    return (eval(string.Template(template).safe_substitute(data)))


def echarts(data, func):
    func(data).set_global_opts(
        title_opts=opts.TitleOpts(title="机器人转速"),
        datazoom_opts=[
            opts.DataZoomOpts(range_start=0, range_end=100),
            opts.DataZoomOpts(type_="inside", range_start=0, range_end=100),
        ],
    ).render('./templates/echarts.html')

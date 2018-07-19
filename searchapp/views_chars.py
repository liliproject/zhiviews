from django.shortcuts import render

# Create your views here.

# from __future__ import unicode_literals

import math
from pyecharts import Map
from django.http import HttpResponse
from django.template import loader
from pyecharts import Line3D
from pyecharts import Bar
from pyecharts import EffectScatter
import numpy as np
from pandas import DataFrame, Series
import pandas as pd
from pyecharts import Geo
from pyecharts import Bar, Timeline
from random import randint

REMOTE_HOST = "https://pyecharts.github.io/assets/js"


def index(request):
    template = loader.get_template('smallsearch.html')
    l3d = line3d()
    context = dict(
        myechart=l3d.render_embed(),
        host=REMOTE_HOST,
        script_list=l3d.get_js_dependencies()
    )
    return HttpResponse(template.render(context, request))


# 查询数据
'''如
w = models.Simp.objects.all().values_list('username')
print w, type(w)

[(u'chenc',), (u'zan',), (u'zhangsan',)] <class 'django.db.models.query.QuerySet'>



w = models.Simp.objects.all().values_list('id', 'username')
print w, type(w)

[(1, u'chenc'), (2, u'zan'), (3, u'zhangsan')] <class 'django.db.models.query.QuerySet'>

'''

# 划分等级   0-2000   2000-4000   4000-6000 6000-8000 8000-10000   10000-15000  150000-20000  20000-30000 30000以上


# 饼图
from pyecharts import Pie

# 折线图
from pyecharts import Line
# from __future__ import unicode_literals
from pyecharts import Bar, Line, Grid
from pyecharts import Boxplot
from pyecharts import Page
import nltk
import jieba
from pyecharts import WordCloud

'''
    # add()中的参数
    title = ''  # 主标题


'''


def line3d():
    page =Page()
    # # ---------------------------------------薪资频数分布图-----------------------------------
    # #
    # #
    # # 饼图  薪资频数分布图
    a = [('0-2000',), ('2000-4000',), ('4000-6000',),
         ('6000-8000',), ('8000-10000',), ('10000-15000',),
         ('6000-8000',), ('8000-10000',), ('10000-15000',),
         ('6000-8000',), ('8000-10000',), ('10000-15000',),
         ('15000-20000',), ('20000-30000',), ('30000以上',)]
    s = []
    for i in a:
        for j in i:
            s.append(j)

    ss = {}
    for i in s:
        if s.count(i) >= 1:
            ss[i] = s.count(i)
    key = list(ss.keys())
    value = list(ss.values())

    # line = Line("薪资频数分布图", width=1200)
    # line.add(
    #     "薪资频数分布直方图",
    #     key,
    #     value,
    #     mark_point=["max", "min"],
    #     mark_line=["average"],
    # )

    pie = Pie("饼图", title_pos='left', width=1300, height=620)
    # pie.add(
    #     "",
    #     key,
    #     value,
    #     radius=[35, 60],
    #     center=[65, 50],
    #     legend_pos="80%",
    #     legend_orient="vertical",
    # )


    # 选图
    # pie.add("", key, value, radius=[35, 50], label_text_color=None, title_pos='left',
    #         is_label_show=True, legend_orient='vertical')
    #
    # pie.add("商品A", key, value, center=[65, 50], is_random=True,
    #         radius=[35, 50], rosetype='radius', legend_pos='left', legend_orient='vertical')

    pie.add("商品B", key, value, center=[45, 50], is_random=True,
            radius=[35, 60], rosetype='area',legend_pos='left',legend_orient='vertical',
            is_legend_show=False, is_label_show=True)

    # grid = Grid()
    # grid.add(line, grid_right="55%")
    # grid.add(pie, grid_left="55%")
    # return grid
    page.add(pie)

    #
    # # -----------------------------工作经验的平均薪资的关系图----------------------------
    #
    exprice = [('1-3年', 5000), ('3-5年', 10000), ('5年以上', 15000), ('5年以上', 13000)]
    exprice = DataFrame(exprice)
    sss = Series(exprice.groupby(0).mean()[1])
    index1 = list(sss.index)
    value1 = list(sss.values)

    line = Line('折线图',width=1300, height=620)
    line.add('工作经验与平均薪资关系图', index1, value1, area_color='#000',
             is_stack=True, is_label_show=True, is_smooth=True)
    page.add(line)
    # return line

    # --------------------------------学历与平均薪资的箱线图--------------------------------

    edu = [('本科', 1200), ('大专', 1000), ('本科', 1566), ('研究生', 2234), ('博士', 2345),
           ('博士后', 2345),('博士后', 4345),('博士后', 345), ('研究生', 8256), ('本科', 6666), ('本科', 3423),
           ('博士后', 5445), ('研究生', 4256), ('本科', 6216), ('本科', 5423),
           ('本科', 1500), ('大专', 1480), ('本科', 1896), ('研究生', 7234),
           ('研究生', 6634), ('研究生', 12234), ('研究生', 5234), ('研究生', 3234),
           ('博士', 1345),('博士', 5345),('博士', 6345),('博士', 4345),('博士', 8345),
           ('大专', 5000), ('大专', 300), ('大专', 1400), ('大专', 2100), ('大专', 4500)]
    edu = DataFrame(edu)
    edulist = {}
    for i in edu[0]:
        edulist[i] = list(edu.loc[edu[0] == i][1])

    k = []
    v = []
    for key, value in edulist.items():
        k.append(key)
        v.append(value)
    print(k)
    print('----',v)
    boxplot = Boxplot("箱形图",background_color='#b6edbd',width=1300, height=620)
    _v = boxplot.prepare_data(v)  # 转换数据
    print(_v)
    boxplot.add("boxplot", k, _v, xaxis_name='学历',yaxis_name='薪资水平',yaxis_name_gap=45)
    page.add(boxplot)
    # return boxplot


    # ----------------------------------------------- 招聘需求词云图 ----------------------------------------------
    # Django返回的查询结果：

    ci = [(
        "岗位职责 1. 负责计算机视觉、图像处理相关算法的研发和优化； 2. 深入分析现有算法，了解业务需求，给出有效的优化解决方案； 3. 跟踪业界学界前沿算法最新进展。 任职要求1. 计算机、电子、统计及数学等专业； 2. 了解机器学习、计算机视觉或图像处理； 3. 熟练使用Python，熟悉至少一种深度学习框架比如Caffe，TensorFlow, MXNet, (Py)Torch, 等 。代码能力较强，有C++和Java语言编程经验的优先。 4. 数理功底扎实，自学能力强",),
        (
            "岗位描述： 1、负责前端产品线的工程化建设和开发规范的制定2、负责封装公用组件和优化系统架构3、与系统工程师、设计师密切合作，参与产品需求、产品设计，负责开发实现以及测试、维护等迭代周期岗位要求： 1、熟练掌握 HTML、CSS、JavaScript 等前端基础技术2、熟练掌握至少一种 HTML 模板语言如 Jinja、Smarty、Velocity、Jade、Mustache 等",), ]


    cici = []
    for i in ci:
        cici.append(i[0])
    c = ''
    ciyu = c.join(cici)
    a = list(jieba.cut(ciyu))
    stripa = []
    for i in a:
        stripa.append(i.strip(" "))

    # 停词表
    stopwords = []
    for word in open('static/file/StopWords.txt', 'r', encoding='gbk'):
        stopwords.append(word.strip())

    for i in stripa:
        if i in stopwords:
            stripa.remove(i)
    print(stripa)
    cfd = nltk.FreqDist(a)
    cipin = list(cfd.keys())
    fre = list(cfd.values())

    wordcloud = WordCloud('词云图',width=1300, height=620)
    wordcloud.add("", cipin, fre, word_size_range=[20, 100])
    page.add(wordcloud)
    # return page
    # return wordcloud


# ------------------------------------------------测试  时间轮播---------------------------------------------
    bar_1 = Bar('2012 年')
    bar_1.add("春季", k, [randint(10, 100) for _ in range(5)])
    bar_1.add("夏季", k, [randint(10, 100) for _ in range(5)])
    bar_1.add("秋季", k, [randint(10, 100) for _ in range(5)])
    bar_1.add("冬季", k, [randint(10, 100) for _ in range(5)])

    bar_2 = Bar("2013 年")
    bar_2.add("春季", k, [randint(10, 100) for _ in range(5)])
    bar_2.add("夏季", k, [randint(10, 100) for _ in range(5)])
    bar_2.add("秋季", k, [randint(10, 100) for _ in range(5)])
    bar_2.add("冬季", k, [randint(10, 100) for _ in range(5)])

    bar_3 = Bar("2014 年")
    bar_3.add("春季", k, [randint(10, 100) for _ in range(5)])
    bar_3.add("夏季", k, [randint(10, 100) for _ in range(5)])
    bar_3.add("秋季", k, [randint(10, 100) for _ in range(5)])
    bar_3.add("冬季", k, [randint(10, 100) for _ in range(5)])

    bar_4 = Bar("2015 年")
    bar_4.add("春季", k, [randint(10, 100) for _ in range(5)])
    bar_4.add("夏季", k, [randint(10, 100) for _ in range(5)])
    bar_4.add("秋季", k, [randint(10, 100) for _ in range(5)])
    bar_4.add("冬季", k, [randint(10, 100) for _ in range(5)])

    bar_5 = Bar("2016 年销量", "数据纯属虚构")
    bar_5.add("春季", k, [randint(10, 100) for _ in range(5)])
    bar_5.add("夏季", k, [randint(10, 100) for _ in range(5)])
    bar_5.add("秋季", k, [randint(10, 100) for _ in range(5)])
    bar_5.add("冬季", k, [randint(10, 100) for _ in range(5)], is_legend_show=True)

    timeline = Timeline(is_auto_play=True, timeline_bottom=0)
    timeline.add(bar_1, '2012 年')
    timeline.add(bar_2, '2013 年')
    timeline.add(bar_3, '2014 年')
    timeline.add(bar_4, '2015 年')
    timeline.add(bar_5, '2016 年')
    page.add(timeline)

    return page





from blueapps.account.decorators import login_exempt
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render

from stuhelper_app.models import Empty_Classroom


@login_exempt
def empty_classroom(request):
    print("转到”空教室查询“")
    q_all = False
    page_numnum = 5
    empty_session1 = request.GET.get('empty_session1')
    empty_session2 = request.GET.get('empty_session2')
    empty_week = request.GET.get('empty_week')
    empty_day = request.GET.get('empty_day')
    campus = request.GET.get('campus')
    building_id = request.GET.get('building_id')
    if empty_day is None or empty_week is None or empty_session1 is None or empty_session2 is None or campus is None:

        empty_week = 0
        empty_day = 0
        empty_session1 = 0
        empty_session2 = 0
        campus = 0
        empty_classrooms = Empty_Classroom.objects.filter(
            empty_week=empty_week, empty_day=empty_day, campus=campus,
            empty_session__gte=empty_session1, empty_session__lte=empty_session2, building_id=building_id).order_by('location_id')

    else:
        empty_classrooms = Empty_Classroom.objects.filter(
            empty_week=empty_week, empty_day=empty_day, campus=campus,
            empty_session__gte=empty_session1, empty_session__lte=empty_session2, building_id=building_id).order_by('location_id')
    paginator = Paginator(empty_classrooms, 24)  # 实例化一个分页对象, 每页显示30个
    page = request.GET.get('page')  # 从URL通过get页码，如?page=3
    if not page:
        page = '1'
    if paginator.num_pages <= page_numnum:
        page_range = range(1, paginator.num_pages + 1)

    else:
        if int(page) <= paginator.num_pages - min(page_numnum, paginator.num_pages):
            page_range = range(int(page), int(page) + min(page_numnum, paginator.num_pages))
        else:
            page_range = range(paginator.num_pages - min(page_numnum, paginator.num_pages), paginator.num_pages + 1)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)  # 如果传入page参数不是整数，默认第一页
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)  # 如果传入page参数超过最大页数，则返回最后一页
    is_paginated = True if paginator.num_pages > 1 else False  # 如果页数小于1不使用分页
    buildings = ['A1', 'A2', 'A3', 'A4', 'A5', 'BXL', '33', '34', 'A', 'B', 'C', 'D', ]
    xingqi = {
        1: '星期一',
        2: '星期二',
        3: '星期三',
        4: '星期四',
        5: '星期五',
        6: '星期六',
        7: '星期日'
    }
    xiaoqu = {
        1: '大学城校区',
        2: '五山校区',
        3: '国际校区'
    }
    campus_num = range(1, 4)
    context = {
        'buildings': buildings,
        'building_id': building_id,
        'empty_classrooms': empty_classrooms,
        'empty_week': int(empty_week),
        'empty_day': int(empty_day),
        'empty_session1': int(empty_session1),
        'empty_session2': int(empty_session2),
        'section_num': range(1, 13),
        'week_num': range(1, 27),
        'day_num': range(1, 8),
        'xingqi': xingqi,
        'page_obj': page_obj,
        'is_paginated': is_paginated,
        'page_range': page_range,
        'page': page,
        'q_all': q_all,
        'campus': int(campus),
        'campus_num': campus_num,
        'xiaoqu': xiaoqu,

    }

    return render(request, 'empty_classroom.html', context)


@login_exempt
def empty_classroom_search(request):
    empty_week = request.GET.get('empty_week')
    empty_day = request.GET.get('empty_day')
    empty_session1 = request.GET.get('empty_session1')
    empty_session2 = request.GET.get('empty_session2')
    xingqi = {
        1: '星期一',
        2: '星期二',
        3: '星期三',
        4: '星期四',
        5: '星期五',
        6: '星期六',
        7: '星期日'
    }
    empty_classrooms = Empty_Classroom.objects.filter(
        empty_week=empty_week, empty_day=empty_day,
        empty_session=empty_session1)
    paginator = Paginator(empty_classrooms, 15)  # 实例化一个分页对象, 每页显示10个
    page = request.GET.get('page')  # 从URL通过get页码，如?page=3
    if not page:
        page = '1'
    if int(page) <= paginator.num_pages - min(4, paginator.num_pages):
        page_range = range(int(page), int(page) + min(4, paginator.num_pages))
    else:
        page_range = range(paginator.num_pages - min(4, paginator.num_pages), paginator.num_pages + 1)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)  # 如果传入page参数不是整数，默认第一页
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)  # 如果传入page参数超过最大页数，则返回最后一页
    is_paginated = True if paginator.num_pages > 1 else False  # 如果页数小于1不使用分页
    if empty_classrooms.count() == 0:
        messages.error(request, "no result")
        empty_classrooms = Empty_Classroom.objects.all()
    context = {
        'empty_classrooms': empty_classrooms,
        'empty_week': empty_week,
        'empty_day': empty_day,
        'empty_section1': 1,
        'empty_section2': 1,
        'section_num': range(1, 13),
        'week_num': range(1, 20),
        'day_num': range(1, 8),
        'xingqi': xingqi,
        'page_obj': page_obj,
        'is_paginated': is_paginated,
        'page_range': page_range,
        'page': page
    }
    return render(request, 'empty_classroom.html', context)

from datetime import datetime
from multiprocessing import context
from django.shortcuts import render,redirect
from django.http import HttpRequest
from .forms import MarkWriteForm
from django.core.paginator import Paginator # 장고에서 페이지네비게이션을 하기위해 만들어진 클래스.

from Members.models import User
from Brands.models import Brand
from Menubar.models import Buy
from .models import Mark

from django.db.models import Max#컬럼 최대값 구하는 객체
from django.db.models import F

# 후기 페이지(Read All)
def Review(request:HttpRequest):
    
    MAX_PAGE_CNT = 10
    MAX_LIST_CNT = 5

    markList = Mark.objects.all().order_by('-groupno','orderno')

    page = request.GET.get('page','1')# page 파라미터가 있으면 값을 가져오고 없으면 1을 반환하겟다..

    #페이징처리
    paginator = Paginator(markList,MAX_LIST_CNT)
    # Paginator 객체 생성할때 리스트값이랑 한페이지당 띄울 후기개수
    page_obj = paginator.get_page(page)
    # 해당페이지에 해당하는 후기을 저장....
    
    #끝페이지.
    last_page = 0
    for last_page in paginator.page_range:
        last_page += 1

    #페이지그룹의 블록...
    current_block = ((int(page) - 1) // MAX_PAGE_CNT) + 1
    
    start_page = (current_block - 1) * MAX_PAGE_CNT + 1

    end_page = start_page + MAX_PAGE_CNT - 1

    context = {
        'list' : page_obj,
        'last_page' : last_page,
        'start_page' : start_page,
        'end_page' : end_page,
    }
    return render(request,'review/list.html',context)

# 후기 생성(Create)
def write(request,buy_no,m_no=0):

    buy_no = Buy.objects.get(buy_no=buy_no)

    forms = MarkWriteForm()
    context = {
        'forms' : forms,
        'buy_no' : buy_no,
        'm_no' : m_no
    }
    return render(request,'review/wirteForm.html',context)

# 후기 확인
def checkWrite(request:HttpRequest):

    m_no = request.POST.get('m_no')
    u_no = User.objects.get(u_no = int(request.session['login']))
    buy_no = request.POST.get('buy_no')           # 타이틀
    buy_no = Buy.objects.get(buy_no=buy_no)
    m_title = request.POST.get('m_title')           # 타이틀
    m_content = request.POST.get('m_content')       # 컨텐트
    m_size = int(request.POST.get('m_size'))        # 사이즈 평점
    m_color = int(request.POST.get('m_color'))     # 색상 평점
    m_puton = int(request.POST.get('m_puton'))     # 착용감 평점
    m_rebuy = int(request.POST.get('m_rebuy'))     # 재구매 의사
    m_tot = (m_size+m_color+m_puton)/3     # 종합 점수
    b_no = int(request.POST.get('b_no'))
    b_no = Brand.objects.get(b_no=b_no)

    # content = content.replace('\r\n','<br>')

    url = None
    msg = None
    try:
        print("여긴가")
        print(m_no)
        print(type(m_no))
        if m_no == '0': # 새후기
            print("여긴가2")

            if Mark.objects.aggregate(max_group=Max('groupno')).get('max_group') == None:
                print("여긴가3")
                groupno = 1
                print("여긴가4")
            else:
                print("여긴가5")
                groupno = Mark.objects.aggregate(max_group=Max('groupno')).get('max_group') + 1
                print("여긴가6")
            print("여긴가8989")
            mark = Mark.objects.create(u_no = u_no,m_title = m_title,m_content = m_content,m_size=m_size,m_color=m_color,m_puton=m_puton,m_rebuy=m_rebuy,m_tot=m_tot,groupno=groupno,buy_no=buy_no,b_no=b_no)
            print("여긴가7")
        else:
            print("여긴가8")
            mark2 = Mark.objects.get(m_no=m_no)
            print("여긴가9")
            Mark.objects.filter(orderno__gte=mark2.orderno + 1).update(orderno=F('orderno') + 1)
            print("여긴가10")
            mark = Mark.objects.create(u_no = u_no,m_title = m_title,m_content = m_content,m_size=m_size,m_color=m_color,m_puton=m_puton,m_rebuy=m_rebuy,m_tot=m_tot,groupno=groupno,buy_no=buy_no,b_no=b_no)
            print("여긴가11")
    except Exception as e:
        print("여긴가12")
        print("후기 실패")
        print("여긴가13")
        print(e)
        print("여긴가14")
        url = '/review/write/0'
        print("여긴가15")
        msg = '후기 쓰기에 실패 하였습니다.'
        print("여긴가16")
    else:
        url = '/review'
        msg = '후기 쓰기에 성공하였습니다.'
    
    context = {
        'url' : url,
        'msg' : msg,
    }

    return render(request,'review/result.html',context)

# 후기 읽기(Read)
def read(request:HttpRequest):
    m_no = request.GET.get('m_no')

    mark = Mark.objects.get(m_no = m_no)

    mark.save()

    context = {
        'content' : mark
    }

    return render(request,'review/read.html',context)

# 후기 수정(Update)
def update(request:HttpRequest):
    m_no = request.GET.get('m_no')

    mark = Mark.objects.get(m_no = m_no)

    forms = MarkWriteForm(instance=mark)
    context = {
        'forms' : forms,
        'm_no' : mark,
    }

    return render(request,'review/updateForm.html',context)

# 후기 수정 확인
def checkUpdate(request:HttpRequest):
    m_no = request.POST.get('m_no')
    m_title = request.POST.get('m_title')+"(수정됨)"
    m_content = request.POST.get('m_content')
    m_size = int(request.POST.get('m_size'))        # 사이즈 평점
    m_color = int(request.POST.get('m_color'))     # 색상 평점
    m_puton = int(request.POST.get('m_puton'))     # 착용감 평점
    m_rebuy = int(request.POST.get('m_rebuy'))     # 재구매 의사
    m_tot = (m_size+m_color+m_puton)/3     # 종합 점수
    m_content = m_content.replace('\r\n','<br>')

    url = None
    msg = None
    try:
        mark = Mark.objects.filter(m_no=m_no).update(m_title = m_title,m_content = m_content,m_size=m_size,m_color=m_color,m_puton=m_puton,m_rebuy=m_rebuy,m_tot=m_tot)
    except Exception as e:
        print(e)
        url = '/review/update/?m_no=' + m_no
        msg = '후기수정에 실패 하였습니다.'
    else:
        url = '/review/read/?m_no=' + m_no
        msg = '후기수정에 성공 하였습니다.'

    context = {
        'url' : url,
        'msg' : msg,
    }

    return render(request,'review/result.html',context)

# 후기 삭제(Delete)
def delete(request:HttpRequest):
    m_no = request.GET.get('m_no')
    
    url = None
    msg = None
    try:
        mark = Mark.objects.get(m_no=m_no).delete()
    except Exception as e:
        print(e)
        url = '/review/read/?m_no=' + m_no
        msg = '후기삭제에 실패 하였습니다.'
    else:
        url = '/review/'
        msg = '후기삭제에 성공하였습니다.'

    context = {
        'url' : url,
        'msg' : msg,
    }

    return render(request,'review/result.html',context)

from datetime import datetime
from multiprocessing import context
from django.shortcuts import render,redirect
from django.http import HttpRequest
from .forms import QnaWriteForm
from django.core.paginator import Paginator # 장고에서 페이지네비게이션을 하기위해 만들어진 클래스.

from Members.models import User
from Brands.models import Brand
from .models import Qcategory, Qna, CS_Comment

from django.db.models import Max#컬럼 최대값 구하는 객체
from django.db.models import F

# 고객센터 페이지(Read All)
def CS(request:HttpRequest):
    
    MAX_PAGE_CNT = 10
    MAX_LIST_CNT = 5

    qnaList = Qna.objects.all().order_by('-groupno','orderno')

    page = request.GET.get('page','1')# page 파라미터가 있으면 값을 가져오고 없으면 1을 반환하겟다..

    #페이징처리
    paginator = Paginator(qnaList,MAX_LIST_CNT)
    # Paginator 객체 생성할때 리스트값이랑 한페이지당 띄울 글개수
    page_obj = paginator.get_page(page)
    # 해당페이지에 해당하는 글을 저장....
    
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
    return render(request,'cs/list.html',context)

# 글 생성(Create)
def write(request,qna_no = 0):
    forms = QnaWriteForm()
    context = {
        'forms' : forms,
        'qna_no' : qna_no
    }
    return render(request,'cs/wirteForm.html',context)

# 글 확인
def checkWrite(request:HttpRequest):

    qna_no = request.POST.get('qna_no')
    u_no = User.objects.get(u_no = int(request.session['login']))
    qna_title = request.POST.get('qna_title')   # 타이틀
    qna_content = request.POST.get('qna_content')   # 컨텐트
    qcate_no = int(request.POST.get('qcate_no'))  # 카테고리
    b_no = int(request.POST.get('b_no'))  # 브랜드 번호

    qcate_no = Qcategory.objects.get(qcate_no=qcate_no)
    b_no = Brand.objects.get(b_no=b_no)

    # content = content.replace('\r\n','<br>')

    url = None
    msg = None
    try:
        if qna_no == '0': # 새글
            if Qna.objects.aggregate(max_group=Max('groupno')).get('max_group') == None:
                groupno = 1
            else:
                groupno = Qna.objects.aggregate(max_group=Max('groupno')).get('max_group') + 1
            qna = Qna.objects.create(u_no = u_no,qna_title = qna_title,qna_content = qna_content,groupno=groupno,qcate_no=qcate_no,b_no=b_no)
        else:
            qna2 = Qna.objects.get(qna_no=qna_no)
            Qna.objects.filter(orderno__gte=qna2.orderno + 1).update(orderno=F('orderno') + 1)
            qna = Qna.objects.create(u_no = u_no,qna_title = qna_title,qna_content = qna_content,groupno=qna2.groupno,orderno=qna2.orderno+1,depth=qna2.depth + 1,qcate_no=qcate_no,b_no=b_no)
    except Exception as e:
        print(e)
        url = '/cs/write/0'
        msg = '글쓰기에 실패 하였습니다.'
    else:
        url = '/cs'
        msg = '글쓰기에 성공 하였습니다.'
    
    context = {
        'url' : url,
        'msg' : msg,
    }

    return render(request,'cs/result.html',context)

# 글 읽기(Read)
def read(request:HttpRequest):
    qna_no = request.GET.get('qna_no')

    qna = Qna.objects.get(qna_no = qna_no)

    qna.save()

    comments = CS_Comment.objects.filter(cs_board = qna_no)
    context = {
        'content' : qna,
        'comments' : comments
    }

    return render(request,'cs/read.html',context)

# 글 수정(Update)
def update(request:HttpRequest):
    qna_no = request.GET.get('qna_no')

    qna = Qna.objects.get(qna_no = qna_no)

    forms = QnaWriteForm(instance=qna)
    context = {
        'forms' : forms,
        'qna_no' : qna_no,
    }

    return render(request,'cs/updateForm.html',context)

# 글 수정 확인
def checkUpdate(request:HttpRequest):
    qna_no = request.POST.get('qna_no')
    qna_title = request.POST.get('qna_title')+"(수정됨)"
    qna_content = request.POST.get('qna_content')

    qna_content = qna_content.replace('\r\n','<br>')

    url = None
    msg = None
    try:
        qna = Qna.objects.filter(qna_no=qna_no).update(qna_title = qna_title,qna_content = qna_content)
    except Exception as e:
        print(e)
        url = '/cs/update/?qna_no=' + qna_no
        msg = '글수정에 실패 하였습니다.'
    else:
        url = '/cs/read/?qna_no=' + qna_no
        msg = '글수정에 성공하였습니다.'

    context = {
        'url' : url,
        'msg' : msg,
    }

    return render(request,'cs/result.html',context)

# 글 삭제(Delete)
def delete(request:HttpRequest):
    qna_no = request.GET.get('qna_no')
    
    url = None
    msg = None
    try:
        qna = Qna.objects.get(qna_no=qna_no).delete()
    except Exception as e:
        print(e)
        url = '/cs/read/?qna_no=' + qna_no
        msg = '글삭제에 실패 하였습니다.'
    else:
        url = '/cs/'
        msg = '글삭제에 성공하였습니다.'

    context = {
        'url' : url,
        'msg' : msg,
    }

    return render(request,'cs/result.html',context)

# 댓글 생성(Create)
def commentInsert(request:HttpRequest,no):

    print("-------------------------------------------")
    print(request.session.get('login'))
    print("-------------------------------------------")

    if request.session.get('login') != None :    # 사용자라면
        cs_user = User.objects.get(u_no = int(request.session['login']))
        cs_board = Qna.objects.get(qna_no=no)
        cs_content = request.POST.get('content')
    
        comment = CS_Comment.objects.create(cs_user = cs_user,cs_board = cs_board,cs_content = cs_content)
    elif request.session.get('brandlogin') != None:  # 브랜드라면
        brand = Brand.objects.get(b_no = int(request.session['brandlogin']))
        cs_board = Qna.objects.get(qna_no=no)
        cs_content = request.POST.get('content')

        cs_content = cs_content.replace('\r\n','<br>')
        comment = CS_Comment.objects.create(cs_brand = brand,cs_board = cs_board,cs_content = cs_content)
    else:   # 사용자도 브랜드도 아니라면
        pass

    return redirect('/cs/read/?qna_no=' + str(no))




    # # 유저인지 확인
    # try:
    #     print("여기까지옴")
    #     cs_user = User.objects.get(u_no = request.session.get('login'))
    #     print("유저임")
    # except:
    #     # 브랜드인지 확인
    #     try:
    #         brand = Brand.objects.get(b_no = int(request.session['brandlogin']))
    #     except Exception as e:
    #         # 유저도 브랜드도 아님
    #         print(e)
    #     else:
    #         # 브랜드일 경우
    #         cs_board = Qna.objects.get(qna_no=no)
    #         cs_content = request.POST.get('content')

    #         cs_content = cs_content.replace('\r\n','<br>')
    #         comment = CS_Comment.objects.create(brand = brand,cs_board = cs_board,cs_content = cs_content)
    # else:
    #     # 유저인 경우
    #     cs_board = Qna.objects.get(qna_no=no)
    #     cs_content = request.POST.get('content')
    
    #     comment = CS_Comment.objects.create(cs_user = cs_user,cs_board = cs_board,cs_content = cs_content)


    return redirect('/cs/read/?qna_no=' + str(no))

# 댓글 삭제(Delete)
def commentDelete(request:HttpRequest,cs_co_no):
    try:
        comment = CS_Comment.objects.get(cs_co_no=cs_co_no)
        url = '/cs/read/?qna_no=' + str(comment.qna.qna_no)
        comment.delete()
    except Exception as e:
        print(e)
        url='/'
    return redirect(url)

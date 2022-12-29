from datetime import datetime
from multiprocessing import context
from django.shortcuts import render,redirect
from django.http import HttpRequest
from .forms import BoardWriteForm
from django.core.paginator import Paginator # 장고에서 페이지네비게이션을 하기위해 만들어진 클래스.

from Members.models import User
from .models import Board, Comment

from django.db.models import Max#컬럼 최대값 구하는 객체
from django.db.models import F

# 커뮤니티 페이지(Read All)
def community(request:HttpRequest):
    
    MAX_PAGE_CNT = 10
    MAX_LIST_CNT = 5

    boardList = Board.objects.all().order_by('-groupno','orderno')

    page = request.GET.get('page','1')# page 파라미터가 있으면 값을 가져오고 없으면 1을 반환하겟다..

    #페이징처리
    paginator = Paginator(boardList,MAX_LIST_CNT)
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
    return render(request,'board/list.html',context)

# 글 생성(Create)
def write(request,bo_no = 0):
    forms = BoardWriteForm()
    context = {
        'forms' : forms,
        'bo_no' : bo_no
    }
    return render(request,'board/wirteForm.html',context)

# 글 확인
def checkWrite(request:HttpRequest):

    bo_no = request.POST.get('bo_no')
    u_no = User.objects.get(u_no = int(request.session['login']))
    bo_title = request.POST.get('bo_title')   # 타이틀
    bo_content = request.POST.get('bo_content')   # 컨텐트
    bo_hit = 0 # 조회수

    # content = content.replace('\r\n','<br>')

    url = None
    msg = None
    try:
        if bo_no == '0': # 새글
            if Board.objects.aggregate(max_group=Max('groupno')).get('max_group') == None:
                groupno = 1
            else:
                groupno = Board.objects.aggregate(max_group=Max('groupno')).get('max_group') + 1
            board = Board.objects.create(u_no = u_no,bo_title = bo_title,bo_content = bo_content,groupno=groupno,bo_hit = bo_hit)
        else:
            board2 = Board.objects.get(bo_no=bo_no)
            Board.objects.filter(orderno__gte=board2.orderno + 1).update(orderno=F('orderno') + 1)
            board = Board.objects.create(u_no = u_no,bo_title = bo_title,bo_content = bo_content,groupno=board2.groupno,orderno=board2.orderno+1,depth=board2.depth + 1,bo_hit = bo_hit)
    except Exception as e:
        print(e)
        url = '/community/write/0'
        msg = '글쓰기에 실패 하였습니다.'
    else:
        url = '/community'
        msg = '글쓰기에 성공하였습니다.'
    
    context = {
        'url' : url,
        'msg' : msg,
    }

    return render(request,'board/result.html',context)

# 글 읽기(Read)
def read(request:HttpRequest):
    bo_no = request.GET.get('bo_no')

    board = Board.objects.get(bo_no = bo_no)

    board.bo_hit += 1

    board.save()

    comments = Comment.objects.filter(board = bo_no)
    context = {
        'content' : board,
        'comments' : comments
    }

    return render(request,'board/read.html',context)

# 글 수정(Update)
def update(request:HttpRequest):
    bo_no = request.GET.get('bo_no')

    board = Board.objects.get(bo_no = bo_no)

    forms = BoardWriteForm(instance=board)
    context = {
        'forms' : forms,
        'bo_no' : bo_no,
    }

    return render(request,'board/updateForm.html',context)

# 글 수정 확인
def checkUpdate(request:HttpRequest):
    bo_no = request.POST.get('bo_no')
    bo_title = request.POST.get('bo_title')+"(수정됨)"
    bo_content = request.POST.get('bo_content')

    bo_content = bo_content.replace('\r\n','<br>')

    url = None
    msg = None
    try:
        board = Board.objects.filter(bo_no=bo_no).update(bo_title = bo_title,bo_content = bo_content)
    except Exception as e:
        print(e)
        url = '/community/update/?bo_no=' + bo_no
        msg = '글수정에 실패 하였습니다.'
    else:
        url = '/community/read/?bo_no=' + bo_no
        msg = '글수정에 성공하였습니다.'

    context = {
        'url' : url,
        'msg' : msg,
    }

    return render(request,'board/result.html',context)

# 글 삭제(Delete)
def delete(request:HttpRequest):
    bo_no = request.GET.get('bo_no')
    
    url = None
    msg = None
    try:
        board = Board.objects.get(bo_no=bo_no).delete()
    except Exception as e:
        print(e)
        url = '/community/read/?bo_no=' + bo_no
        msg = '글삭제에 실패 하였습니다.'
    else:
        url = '/community/'
        msg = '글삭제에 성공하였습니다.'

    context = {
        'url' : url,
        'msg' : msg,
    }

    return render(request,'board/result.html',context)

# 댓글 생성(Create)
def commentInsert(request:HttpRequest,no):
    user = User.objects.get(u_no = int(request.session['login']))
    board = Board.objects.get(bo_no=no)
    content = request.POST.get('content')

    content = content.replace('\r\n','<br>')

    try:
        comment = Comment.objects.create(user = user,board = board,content = content)
    except Exception as e:
        print(e)

    

    return redirect('/community/read/?bo_no=' + str(no))

# 댓글 삭제(Delete)
def commentDelete(request:HttpRequest,co_no):
    try:
        comment = Comment.objects.get(co_no=co_no)
        url = '/community/read/?bo_no=' + str(comment.board.bo_no)
        comment.delete()
    except Exception as e:
        print(e)
        url='/'
    return redirect(url)

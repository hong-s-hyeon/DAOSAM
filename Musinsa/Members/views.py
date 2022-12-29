from datetime import datetime
from multiprocessing import context
from time import strftime
from django.shortcuts import render,redirect
from django.http import HttpRequest
from .models import User,Delivery,Payment,Grade
from datetime import datetime

# 회원가입 페이지로 이동
def joinform(request):
    return render(request,'join/joinform.html')

# 회원가입
def checkjoinform(request:HttpRequest):
    u_id = request.POST.get('u_id')
    u_pw = request.POST.get('u_pw')
    u_name = request.POST.get('u_name')
    u_nickname = request.POST.get('u_nickname')
    u_email = request.POST.get('u_email')
    u_hp = request.POST.get('u_hp')
    u_birth = request.POST.get('u_birth')
    datetime_format = "%Y%m%d"
    u_birth =  datetime.strptime(u_birth,datetime_format)

    u_joindate = datetime.now()
    print('여기까지옴')
    # 가입이 이미 되어 있는지 확인해주기
    #없다면 가입하기
    # try:
    #     msg='이미 가입된 아이디입니다'
    #     url='/member/login/'
    #     User.objects.get(u_id=u_id)
    # except:
    newuser=User.objects.create(u_id=u_id,u_pw=u_pw,u_nickname=u_nickname,u_name=u_name,u_birth=u_birth,u_email=u_email,u_hp=u_hp,u_joindate=u_joindate)
    
    no = str(newuser.u_no)
    print(no)
    msg='회원가입에 성공하였습니다.'
    url='/members/loginform/?n='+no

    context={
        'msg' : msg,
        'url' : url,

    }

    return render(request,'result.html',context)

# 로그인 페이지
def loginform(request:HttpRequest):

    u_id = request.GET.get("u_id") # ''
    print("1번째 u_id : " + str(u_id))
    check = False
    
    if u_id == '' or u_id == None:
        u_id = request.COOKIES.get("cookie_name")
        print(u_id)
        if u_id != None:
            check = True
    
    try:
        context={
            'u_id' : u_id,
            "check" : check,
        }

    except:
        print('except로 옴')
        return render(request,'login/loginform.html')
    else:
        print('id 가지고 옴')
        return render(request,'login/loginform.html',context)

# 로그인 확인
def checkloginform(request:HttpRequest):
    u_id = request.POST.get('u_id')
    u_pw = request.POST.get('u_pw')

    msg = None
    check = False

    try:
        user=User.objects.get(u_id=u_id,u_pw=u_pw)
    except:
        msg ='해당 아이디와 비밀번호 정보가 없습니다.'
        url ='/members/loginform/'
    else:
        check = True
        msg =user.u_name+'님 환영합니다'
        url ='/'

        request.session['login'] = user.u_no    # 세션에 로그인 등록
    context= {
        'msg' : msg,
        'url' :url,
        'check' : check
    }

    response = render(request,'result.html',context)

    if check:
        ckid = request.POST.get("ckid") # 아이디 기억하기 체크여부 확인
        print(ckid)

        ck_u_id = request.COOKIES.get('u_id') # 쿠키파일중에 파일명이 ckid 찾기
        print(ck_u_id)

        
        if ckid != None: #아이디 기억하기 체크된 상태
            if ck_u_id == None:
                #쿠키파일 생성...
                response.set_cookie("cookie_name",u_id,max_age=60*60*10) #생성
                # ckid라는 파일명으로 로그인한 아이디를 컨텐츠에 넣고 유지시간 10시간으로 쿠키파일 설정.
            elif ck_u_id != u_id: #쿠키파일의 아이디와 로그인된 아이디가 다른경우
                response.set_cookie("cookie_name",u_id,max_age=60*60*10) # 만들어진 상황이면 쿠키파일 변경
        else: # 아이디 기억하기 체크 해제된 상태
            pass
            # if ck_u_id == u_id: # 쿠키파일의 아이디와 로그인된 아이디가 같은경우
            #     response.delete_cookie("cookie_name") # 쿠키파일 삭제
            # else:   # 쿠키파일의 아이디와 로그인된 아이디가 다른경우
            #     response.delete_cookie("cookie_name") # 쿠키파일 삭제


    return response

#로그아웃
def logout(request:HttpRequest):
    print(request.session['login'])
    
    u_no = request.session['login']
    u_pw = request.POST.get('u_pw')
        
    request.session.pop('login')
    msg='로그아웃 성공'
    url='/'

    context={
        'msg' : msg,
        'url' :url       
    }

    return render(request,'result.html',context)

# 마이페이지
def mypage(request:HttpRequest):
    u_no = request.session['login']
    user = User.objects.get(u_no=u_no)    # 현재 로그인 중인 user의 정보 전체

    deli = checkDeli(u_no)
    payment = checkPayment(u_no)
    
    context = {
        'user' : user,
        'deli' : deli,
        'payment' : payment
    }
    return render(request,'mypage/mypage.html',context)

# # 비밀번호 확인 페이지
def pwpage(request:HttpRequest):
    print(request.GET.get('kind'))
    context = {
        'kind' : request.GET.get('kind')
    }
    return render(request,'pwpage.html',context)


# 기본 주소 여부 확인
def checkDeli(u_no):
    try:
        deli=Delivery.objects.get(u_no=u_no)
    except Exception as e:
        return ''
    else:
        return deli


# 기본 결제정보 여부 확인
def checkPayment(u_no):
    try:
        payment=Payment.objects.get(u_no = u_no)
    except Exception as e:
        return ''
    else:
        return payment


# 비밀번호 확인
def checkPw(request:HttpRequest):
    # 수정 / 탈퇴
    u_no = request.session['login']
    u_pw = request.POST.get('u_pw')
    kind = request.POST.get('kind')
    url = '/members/pwpage/?kind='+kind

    deli = checkDeli(u_no)
    payment = checkPayment(u_no)

    try:
        user=User.objects.get(u_no=u_no,u_pw=u_pw)    # 현재 로그인 중인 user의 정보 전체
    except:
        msg ='비밀번호가 틀렸습니다.'
        context= {
            'msg' : msg,
            'url' : url
        }
        return render(request,'result.html',context)
    else:
        # 수정
        if (kind == "0"):
            # 수정페이지로 이동
            context = {
                'user' : user,
                'deli' : deli,
                'payment' : payment
            }
            return render(request,'update/updateInfo.html',context)
        # 탈퇴
        elif (kind == "1"):
            try:
                user = User.objects.filter(u_no=u_no, u_pw=u_pw)
                # deli = Delivery.objects.filter(u_no=u_no)
            except:
                msg='비밀번호가 일치하지 않습니다.'

                context={
                    'msg' : msg
                }
                return render(request,'result.html',context)
            else:
                msg = '계정이 탈퇴되었습니다'
                # deli.delete()
                user.delete()
                context= {
                    'msg' : msg,
                    'url' : ''
                }

                return render(request,'result.html',context)

        else:
            msg = '잘못된 입력입니다.'

            context= {
                'msg' : msg,
                'url' : ''
            }

            return render(request,'result.html',context)

# 내 정보 수정
def updateInfo(request:HttpRequest):
    u_no = request.session['login']
    
    # 유저정보 관련
    u_id = request.POST.get('u_id')                         # 유저 id
    u_pw = request.POST.get('u_pw')                         # 유저 pw
    u_name = request.POST.get('u_name')                     # 유저 이름
    u_nickname = request.POST.get('u_nickname')             # 유저 닉네임
    u_email = request.POST.get('u_email')                   # 유저 이메일
    u_hp = request.POST.get('u_hp')                         # 유저 전화번호
    u_birth = request.POST.get('u_birth')                   # 유저 생년월일(1)
    datetime_format = "%Y년 %m월 %d일"                      # 유저 생년월일(2)
    u_birth =  datetime.strptime(u_birth,datetime_format)   # 유저 생년월일(3)
    u_refundnum = request.POST.get('u_refundnum')           # 유저 환불계좌번호

    # 배송관련
    d_addr = request.POST.get('d_addr')                     # 배송지
    d_recipient = request.POST.get('d_recipient')           # 수령인
    d_name = request.POST.get('d_name')                     # 배송지명
    d_phone = request.POST.get('d_phone')                   # 휴대전화
    
    # 결제관련
    p_name = request.POST.get('p_name')                     # 결제수단 명
    p_cardnum = request.POST.get('p_cardnum')               # 결제카드번호

    try : 
        # User테이블 수정
        user = User.objects.filter(u_no=u_no)
        user.update(u_id=u_id, u_pw=u_pw, u_name=u_name, u_nickname=u_nickname, u_email=u_email, u_hp=u_hp, u_birth=u_birth, u_refundnum = u_refundnum)
        
        user = User.objects.get(u_no=u_no)

    except Exception as e:
        print(e)
        print("유저 테이블 수정 실패")
    else:
        print("유저 테이블 수정 완료")

    try :
        # Delivery테이블 수정
        addr = Delivery.objects.filter(u_no=u_no, d_default_addr=0)
        addr.update(d_addr = d_addr, d_recipient=d_recipient, d_name=d_name, d_phone=d_phone)

        addr = Delivery.objects.get(u_no=u_no, d_default_addr=0)

    except Exception as e:
        # 배송지가 처음에 없을 때
        print(e)
        print("배송지 없음")
        addr = Delivery.objects.create(u_no=user, d_addr=d_addr, d_recipient=d_recipient, d_name=d_name, d_phone=d_phone)
        print("배송지 추가")

    else:
        print("배송지 수정 성공")

    try :
        # Payment테이블 수정
        payment = Payment.objects.filter(u_no=u_no)
        payment.update(p_name = p_name, p_cardnum=p_cardnum)

        payment = Payment.objects.get(u_no=u_no)

    except Exception as e:
        # 결제정보가 처음에 없을 때
        print(e)
        print("결제정보 없음")
        payment = Payment.objects.create(u_no=user, p_name = p_name,p_cardnum=p_cardnum)
        print("결제정보 추가")
        return  redirect('/members/mypage')

    else:
        print("결제정보 수정 성공")
        print("전제수정 완료")
        return redirect('/members/mypage')

# 아이디 찾기 페이지
def findid(request:HttpRequest):
    return render(request,'findid.html')

# 아이디 찾기 확인
def checkfindId(request:HttpRequest):
    u_name = request.POST.get('u_name')
    u_hp = request.POST.get('u_hp')

    msg = None

    try:
        user = User.objects.get(u_name=u_name,u_hp=u_hp)
    except Exception as e:
        msg ='일치하는 정보가 없습니다.'
        url ='/members/loginform/'
    else:
        msg = user.u_name+'님의 아이디는 ' + user.u_id +'입니다'
        url = '/members/loginform/'

    context = {
        'msg' : msg,
        'url' : url
    }

    return render(request,'result.html',context)


# 비밀번호 찾기 페이지
def findpw(request:HttpRequest):
    return render(request,'findpw.html')


# 비밀번호 찾기 확인
def checkfindPw(request:HttpRequest):
    u_id = request.POST.get('u_id')
    u_name = request.POST.get('u_name')
    u_hp = request.POST.get('u_hp')

    msg = None

    try:
        user = User.objects.get(u_id=u_id, u_name=u_name, u_hp=u_hp)
    except Exception as e:
        msg ='일치하는 정보가 없습니다.'
        url ='/members/loginform/'
    else:
        msg = user.u_name+'님의 비밀번호는 ' + user.u_pw +'입니다'
        url = '/members/loginform/'

    context = {
        'msg' : msg,
        'url' : url
    }

    return render(request,'result.html',context)












# 9/13 브랜드가 완성되면 제작
# 최근 본 상품 페이지
def viewed_item(request:HttpRequest):
    return render(request,'mypage/viewed_item.html')

# 9/13 브랜드가 완성되면 제작
# 좋아요 누른 상품 페이지
def like_item(request:HttpRequest):
    return render(request,'mypage/like_item.html')

# 9/13 브랜드가 완성되면 제작
# 장바구니 페이지
def basket_item(request:HttpRequest):
    return render(request,'mypage/basket_item.html')

# 9/13 브랜드가 완성되면 제작
# 주문배송조회 페이지
def ordered_list(request:HttpRequest):
    return render(request,'mypage/ordered_list.html')

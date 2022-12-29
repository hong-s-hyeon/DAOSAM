from datetime import datetime

import os

from django.shortcuts import render,redirect
from django.http import HttpRequest

from django.conf import settings
from .models import Bigcate, Brand,Brandcate, Color, Item, Itemimage, Midcate, Shoesize, Size,Options, Stock
from Menubar.models import Buy
# Create your views here.

def Brands_index(request):
    return render(request,'brandsindex.html')


def Brands_joinform(request):
    bcate = Brandcate.objects.all()
    
    context= {
        'bcate' : bcate
    }
    return render(request,'join/bjoinform.html',context)

def Brands_checkjoinform(request:HttpRequest):
    try:                            #여기서 그 객체를 담아줌
        bc_no = int(request.POST.get('bc_no')) # foreign key로 받아온값
        b_url = request.POST.get('b_url')
        b_addr = request.POST.get('b_addr')
        b_managername = request.POST.get('b_managername')
        b_korname = request.POST.get('b_korname')
        b_engname = request.POST.get('b_engname')
        b_info = request.POST.get('b_info')
        b_info = b_info.replace('\r\n','<br>')
        b_id = request.POST.get('b_id')
        b_pw = request.POST.get('b_pw')
        b_email = request.POST.get('b_email')
        b_serialnum = request.POST.get('b_serialnum')
        tel1 = request.POST.get('tel1')
        tel2 = request.POST.get('tel2')
        tel3 = request.POST.get('tel3')
        b_hp = tel1+tel2+tel3
        
    
        b_img = request.FILES.get('b_img')
        
        bcate= Brandcate.objects.get(bc_no=bc_no)   # foreign key로 받아온값으로 get해서 변수에넣음
        new = Brand.objects.create(bc_no=bcate,b_url=b_url,b_addr=b_addr,b_managername=b_managername,b_korname=b_korname,b_engname=b_engname,b_info=b_info,b_id=b_id,b_pw=b_pw,b_email=b_email,b_serialnum=b_serialnum,b_hp=b_hp,b_img=b_img)
        
    except :
        
        msg='회원가입에 실패하였습니다.'
        url='/brands/bjoinform/'
        context={
                'msg' : msg,
                'url' : url
            }
        return render(request,'result.html',context)
    else:
        msg='브랜드 : {}/{}관리자 : {}으로 회원가입처리 완료.상태 : 가입승인 절차 대기중'.format(b_korname,b_engname,b_managername)
        url='/brands/'
       
        context={
                'msg' : msg,
                'url' : url
            }
        return render(request,'result.html',context)


def Brands_loginform(request):
    id = request.GET.get("id") # '' ---> 회원가입에 성공한 아이디 정보
    check = False
    print(request.COOKIES.get("ckid"))
    if id == '' or id == None:  #바로 login 버튼누르고 들어왔다면?
        id = request.COOKIES.get("ckid") #쿠키에 저장된 아이디를 가지고 찾기
        if id != None:      #쿠키에 아이디가 저장되어있다는 의미
            check = True

    context = {
        'id' : id,
        "check" : check,
    }
    return render(request,'login/bloginform.html',context)

def Brands_checkloginform(request:HttpRequest):
    id= request.POST.get('id')
    pw= request.POST.get('pw')

    msg = None
    check = False
    try:

        brand = Brand.objects.get(b_id=id,b_pw=pw) # and   select * from member_member where id= id and pw =pw --->한줄 
        #print(member.query) # 지금 작성한 쿼리문 반환...
        
    except Exception as e:
        msg = "아이디 혹은 비밀번호가 잘못되었습니다."
        
        url='/brands/'
        context={
            'msg' : msg,
            'url' : url
        }
        return render(request,'result.html',context)
    else:
        check = True
        #로그인 처리
        request.session['brandlogin'] = brand.b_no
        request.session['confirm'] = int(brand.b_confirm)
       
        
        return redirect('/brands/')
    # response = render(request,'brandsindex.html',context)

    # if check:
    #     ckid = request.POST.get("ckid") #파라미터의 ckid    체크를했다면? value="sdnjksdkljet"---> ckid=="sdnjksdkljet"
    #                                                         #체크를 안했다면?                ----> ckid==''
    #     ck = request.COOKIES.get('ckid') # 쿠키파일중에 파일명이 ckid 찾기
    #     # print(ck)

    #     if ckid != None: #아이디 기억하기 체크된 상태--->'나는 쿠키에 저장하겠다~ 는 의미를 코드로 구현해야한다'
    #         if ck == None: # 이전에 저장한 쿠키가 없는 상태
    #             #쿠키파일 생성...(create)
               
    #             response.set_cookie("ckid",id,max_age=60*60*365*2)
    #             # ckid라는 파일명으로 로그인한 아이디를 컨텐츠에 넣고 2년이라는 시간으로 쿠키파일 설정.(초단위라는 이야기~)
               
    #         elif ck != id: #현재 나는 체크를 누른상태 + 있긴있는데~~ 내가 지금 로그인하려는 id와 쿠키에 저장된 아이디가 다르다른 상태!=====>수정(update)
                
    #             response.set_cookie("ckid",id,max_age=60*60*365*2)
    #             # ckid라는 파일명으로 로그인한 아이디를 컨텐츠에 넣고 2년이라는 시간으로 쿠키파일 설정.
              
    #         else: #비어있지도 않고~ + ck==id
    #             pass
    #     else:           #아이디 기억하기 체크되지 않은 상태--->'나는 쿠키에 저장하지 않겠다~ 는 의미를 코드로 구현해야한다'
    #         if ck == id:        #이전에 ck에 아이디와 지금 입력한 아이디가 같은데, 아이디기억 체크를 해제했다? ---->삭제(delete)
                
    #             response.delete_cookie("ckid")
                
    #             # ckid라는 파일명으로 로그인한 아이디를 컨텐츠에 넣고 2년이라는 시간으로 쿠키파일 설정.
        
    

    # return response


def Brands_logout(request:HttpRequest):
    request.session.pop('brandlogin') # 세션에 저장된 하나의 키와 밸류 삭제.
    request.session.pop('confirm')
    #print(request.session['login'])
    #request.session.flush() # 세션의 저장된 정보 초기화
    return redirect('/brands/')


def Brands_mypage(request:HttpRequest):
    no = int(request.session['brandlogin'])
    
    b = Brand.objects.get(b_no=no)
    # b.b_info = str(b.b_info).replace('<br>','\r\n')
    
    tel1 = str(b.b_hp)[:3]
    tel2 = b.b_hp[3:7]
    tel3 = b.b_hp[7:]
    pw = b.b_pw.replace(b.b_pw[:2],'*'*len(b.b_pw[:2]))
    # 저장된 정보를 가지고가서 띄워주고, 수정/탈퇴를 한다
    serialnum=str(b.b_serialnum)
    serialnum= serialnum.replace(serialnum[4:],'*'*len(serialnum[4:]))
    if b.b_confirm ==2:
        b.b_confirm = '보류'
    elif b.b_confirm ==1:
        b.b_confirm = '승인'
    else:
        b.b_confirm ='승인거절'

    allbuy = Buy.objects.all()
    count=0
    sellmoney=0
    for my in allbuy:
        print(my.st_no.b_no.b_korname)
        if my.st_no.b_no.b_no == b.b_no:
            count+=my.buynum
            sellmoney+=my.buy_tot

    mybrand = Brand.objects.filter(b_no=no)        
    # mybrand.b_sellcnt = count
    # mybrand.b_sellmoney = sellmoney
    mybrand.update(b_sellcnt=count,b_sellmoney=sellmoney)

    context={
        'b' : b,
        'tel1' : tel1,
        'tel2' : tel2,
        'tel3' : tel3,
        'pw' : pw,
        'serialnum' : serialnum,
        'count' : count,
        'sellmoney' : sellmoney
    }

    return render(request,'mypage/bmypage.html',context)


def Brands_selectmode(request:HttpRequest):
    m = request.GET.get('m')
    print(m) #넘어오는 것 확인.
    no = request.session['brandlogin']
    b = Brand.objects.get(b_no=no)

    context = {
        'b' : b,
        'm' : m
    }
    return render(request,'mypage/bcheckwho.html',context)

def Brands_checkselect(request:HttpRequest):
    m = request.POST.get('mode')
    pw = request.POST.get('pw')
    serialnum = request.POST.get('serialnum')

    try:
        if m =='1':#회원정보 수정 페이지 이동
            b = Brand.objects.get(b_pw=pw,b_serialnum=serialnum)
            tel1 = str(b.b_hp)[:3]
            tel2 = b.b_hp[3:7]
            tel3 = b.b_hp[7:]
            print(b.b_info)
            b.b_info = str(b.b_info).replace('<br>','\r\n')
            context = {
                'b' : b,
                'tel1' : tel1,
                'tel2' : tel2,
                'tel3' : tel3,
                # 'info' :  info
            }
            return render(request,'mypage/bupdateform.html',context)
        elif m=='2':# 삭제
            b = Brand.objects.get(b_pw=pw,b_serialnum=serialnum)
            
    except:
        msg = '비밀번호 혹은 사업자등록번호를 다시 확인하세요'
        url = '/brands/bmypage/'
        context = {
            'msg' : msg,
            'url' : url,
        }
        return render(request,'result.html',context)
    else:
        #회원탈퇴만 여기로 온다
        request.session.flush()
        path=os.path.dirname(b.b_img.name)
        b.delete()
        if os.path.exists(os.path.join(settings.MEDIA_ROOT,path)):
            try:
                os.rmdir(os.path.join(settings.MEDIA_ROOT,path))
            except Exception as e:
               print(e)
               
        msg='회원탈퇴 성공'
        url= '/brands/'
        context={
            'msg' : msg,
            'url' : url
        }
        return render(request,'result.html',context)

def Brands_checkupdateform(request:HttpRequest):
    b_url = request.POST.get('b_url')
    b_addr = request.POST.get('b_addr')
    b_managername = request.POST.get('b_managername')
    b_korname = request.POST.get('b_korname')
    b_engname = request.POST.get('b_engname')
    b_info = request.POST.get('b_info')
    b_id = request.POST.get('b_id')
    b_pw = request.POST.get('b_pw')
    b_email = request.POST.get('b_email')
    b_serialnum = request.POST.get('b_serialnum')
    tel1 = request.POST.get('tel1')
    tel2 = request.POST.get('tel2')
    tel3 = request.POST.get('tel3')
    b_hp = tel1+tel2+tel3
    b_refund_num = request.POST.get('b_refund_num')
    b_img = request.FILES.get('b_img')
    b_img = 'brands_img/'+b_img.name
    no = request.session['brandlogin']
    brand = Brand.objects.filter(b_no=no)


    brand.update(b_url=b_url,b_addr=b_addr,b_managername=b_managername,b_korname=b_korname,b_engname=b_engname,b_info=b_info,b_id=b_id,b_pw=b_pw,b_email=b_email,b_serialnum=b_serialnum,b_hp=b_hp,b_img=b_img,b_refund_num=b_refund_num)
    msg = '회원정보가 수정되었습니다.'
    url = '/brands/bmypage/'
    context={
        'msg' : msg,
        'url' : url
    }
    return render(request,'result.html',context)


def Brands_mclist(request:HttpRequest):
    no = request.session['brandlogin']
    n=Brand.objects.get(b_no=no)
    ms = Item.objects.filter(b_no=n)
    print(ms)
    context={
        'ms' : ms
    }
    return render(request,'merchandise/mclist.html',context)


def Brands_mcregisterform(request:HttpRequest):
    b = request.session['brandlogin']
    b = Brand.objects.get(b_no=b)
    bigcate = Bigcate.objects.all()
    midcate = Midcate.objects.all()
    
        

    context ={
        'b' : b,
        'bigcate' : bigcate,
        'midcate' : midcate
    }
    return render(request,'merchandise/mcregisterform.html',context)


def Brands_bcheckmcregisterform(request:HttpRequest):
    bigcate_no=request.POST.get('bigcate_no')
    midcate_no=request.POST.get('midcate_no')
    no=request.session['brandlogin']
    it_name=request.POST.get('it_name')
    it_price=request.POST.get('it_price')
    it_point=request.POST.get('it_point')
    print(it_point)
    it_discount=request.POST.get('it_discount')
    it_regdate = datetime.now()
    
    try:
        big = Bigcate.objects.get(bigcate_no=bigcate_no)
        mid = Midcate.objects.get(midcate_no=midcate_no)
        n = Brand.objects.get(b_no=no)
        Item.objects.create(bigcate_no=big,midcate_no=mid,b_no=n,it_name=it_name,it_price=it_price,it_point=it_point,it_discount=it_discount,it_regdate=it_regdate)
    except:
        msg = '상품등록 실패. 재등록이 필요합니다.'
        url = '/brands/mclist/'
        
    else:
        msg = '상품등록 성공.'
        url = '/brands/mclist/'

    finally:
        context={
            'msg' : msg,
            'url' : url
        }
        return render(request,'result.html',context)
    

def Brands_bextraAdd(request:HttpRequest):
    # 해당 아이탬 불러오기
    itno = request.GET.get('no')
    it = Item.objects.get(it_no=itno)
    context = {
        'it' : it,
        'itno' : itno
    }
    return render(request,'merchandise/bextraAddform.html',context)


def Brands_bcheckextraddform(request:HttpRequest):
    no = int(request.POST.get('it_no'))
    print(no)
    item = Item.objects.get(it_no=no)
    print(item.bigcate_no)
    print(item.b_no.b_engname)
    print(type(item.bigcate_no.bigcate_no))
    bigcate = Bigcate.objects.get(bigcate_no=item.bigcate_no.bigcate_no)
    
    try:
        clicking = int(request.POST.get('cliknum')) #  색상의 클릭을한 갯수를 가지고 온다
        # 색상 넣어주기
        for i in range(1,clicking+1):
            globals()['col{}'.format(str(i))]= request.POST.get('col'+str(i))
    except Exception as e:
        print(e)

    try:
        clicking2 = int(request.POST.get('cliknum1'))
        # 옵션 넣어주기
        for i in range(1,clicking2+1):
            globals()['opt{}'.format(str(i))]= request.POST.get('opt'+str(i))
    except Exception as e:
        print(e)

    if item.bigcate_no.bigcate_no != 1 and item.bigcate_no.bigcate_no != 2 and item.bigcate_no.bigcate_no != 3:
        try:
            clicking3 = int(request.POST.get('scliknum'))
            #신발사이즈 넣어주기
            for i in range(1,clicking3+1):
                globals()['ss{}'.format(str(i))]= request.POST.get('ss'+str(i))
        except Exception as e:
            print(e)
    else:
        size = request.POST.getlist('size')
        for i in range(size.__len__()):
            print(size[i])


  



    ii_imgs = request.FILES.getlist('ii_img') 
    try:
        msg=''
        try:
            for i in range(1,clicking+1):
                Color.objects.create(it_no=item,col_name=globals()['col{}'.format(str(i))])
        except:
            msg+='색상 적용 안됨/'
        try:
            for i in range(1,clicking2+1):
                Options.objects.create(it_no=item,opt_name=globals()['opt{}'.format(str(i))])
        except:
            msg+='옵션 적용 안됨/'
        if item.bigcate_no.bigcate_no != 1 and item.bigcate_no.bigcate_no != 2 and item.bigcate_no.bigcate_no != 3:
            try:
                for i in range(1,clicking3+1):
                    Shoesize.objects.create(it_no=item, bigcate_no=bigcate,ss_name=globals()['ss{}'.format(str(i))])
            except:
                msg+='신발 사이즈 적용 안됨/'
        else:
            try:
                
                for i in range(size.__len__()):
                    Size.objects.create(it_no=item,s_name=size[i],bigcate_no=bigcate)
               
            except:
                msg+='사이즈 적용 안됨/'
        try:    
            # Itemimage.objects.create(it_no=item,id=item.b_no.b_engname,ii_img=ii_img)
            for ii_img in ii_imgs:
                img = Itemimage(it_no=item,ii_img=ii_img,ii_id=item.b_no.b_engname)
                img.save()
        except Exception as e:
            print(e)
            msg += '상품이미지 적용 안됨/'
    except:
        msg += '//문제발생'
        url = '/brands/mclist/'
    else:
       msg+= '//적용 완료'
       url = '/brands/mclist/'

    context = {
        'msg' : msg,
        'url' : url
    }
    # print(msg)
        
    return render(request,'result.html',context)


def Brands_bstockregister(request:HttpRequest):
    itno=request.GET.get('no')  # url에 파라미터로 가지고온 정보.
    item = Item.objects.get(it_no=itno)
    # print(item.bigcate_no)  # 아이탬의 대분류 번호 찾아오기
    
    bigcate = Bigcate.objects.get(bigcate_no=item.bigcate_no.bigcate_no)
    
    
    color = Color.objects.filter(it_no=item)   #해당상품의 아이템 색상정보
    print(color.__len__())
    collength = color.__len__()
    
    option = Options.objects.filter(it_no=item)
    print(option.__len__())
    optlength = option.__len__()

    itimg= Itemimage.objects.filter(it_no=item)
    print(itimg.__len__())

    if item.bigcate_no.bigcate_no != 1 and item.bigcate_no.bigcate_no != 2 and item.bigcate_no.bigcate_no != 3:
        size = Shoesize.objects.filter(it_no=item)
        sizelength = size.__len__()
    else:
        size = Size.objects.filter(it_no=item)
        sizelength = size.__len__()
    


    context={
        'collength' : collength,
        'optlength' : optlength,
        'sizelength' : sizelength,
        'itimg' : itimg,
        'size' : size,
        'bigcate' : bigcate,
        'item' : item,
        'color' : color,
        'option' : option,
    }    

    return render(request,'merchandise/bstockregisterform.html',context)


def Brands_checkbstockregisterform(request:HttpRequest):
   
    #입력된 정보를 가지고오는 작업
    itno = request.POST.get('no')
    item = Item.objects.get(it_no=itno)
    color = Color.objects.filter(it_no=item)
    option = Options.objects.filter(it_no=item)
    brand = Brand.objects.get(b_no=item.b_no.b_no)
    bigcate = Bigcate.objects.get(bigcate_no=item.bigcate_no.bigcate_no)
    


    if item.bigcate_no.bigcate_no!= 4 and item.bigcate_no.bigcate_no!= 5 :
        size = Size.objects.filter(it_no=item)
    else:
        size = Shoesize.objects.filter(it_no=item)
    
    collength = color.__len__()
    sizelength = size.__len__()
    num = color.__len__() * size.__len__()
       


    
    sellcnt = request.POST.getlist('sellcnt')
    stock = request.POST.getlist('stock')
    status = request.POST.getlist('status')
    print(sellcnt.__len__())
    for i in range(stock.__len__()):
        print(i)
        stock[i] = int(stock[i])
        sellcnt[i] = int(sellcnt[i])
        if  stock[i] > 0:
            status[i] = '가능'
        else:
            status[i] = '소진'
    # 상태 가지고 오는것
    # for i in range(num):
    #     globals()['status{}'.format(str(i+1))] = request.POST.get(str(i+1)+'status')
    #     if  globals()['stock{}'.format(str(i+1))] > 0:
    #         globals()['status{}'.format(str(i+1))] = '가능'
    #     else:
    #          globals()['status{}'.format(str(i+1))] = '소진'
    try:
        i = 0
        print("i = ",i)
        for c in color:
            for s in size:
                if item.bigcate_no.bigcate_no!= 4 and item.bigcate_no.bigcate_no!= 5 :
                    # stk = Stock.objects.filter(b_no=brand,it_no=item,col_no=c,s_no=s)
                    # print(stk.__len__())
                    # stk.update(b_no=brand,it_no=item,col_no=c,s_no=s,st_cnt=stock[i])
                    Stock.objects.create(b_no=brand,it_no=item,col_no=c,s_no=s,st_cnt=stock[i],st_sellcnt=sellcnt[i],st_status=status[i])
                else:
                    # stk = Stock.objects.filter(b_no=brand,it_no=item,col_no=c,ss_no=s)
                    # print(stk.__len__())
                    # stk.update(b_no=brand,it_no=item,col_no=c,ss_no=s,st_cnt=stock[i],st_sellcnt=4,st_status=status[i])
                    Stock.objects.create(b_no=brand,it_no=item,col_no=c,ss_no=s,st_cnt=stock[i],st_sellcnt=sellcnt[i],st_status=status[i])
                print('성공')
                print("i = ",i)
                i+=1
    
        # print(num*num-num)
        # for i in range(num*num-num):
        #     st=Stock.objects.all()
        #     stnum =st.__len__()
        #     Stock.objects.filter(st_no=stnum).delete()
    except Exception as e:
        print('실패')
        print(e)
    
    stock = Stock.objects.filter(b_no=brand,it_no=item)


    context = {
        'item' : item,
        'itno' : itno,
        'color' : color,
        'size' : size,
        'collength' : collength,
        'sizelength' : sizelength,
        'bigcate' : bigcate,
        'stock' : stock

    }

    return render(request,'merchandise/bstockcheckform.html',context)
       

def Brands_bstockcheckform(request:HttpRequest):
    itno = request.GET.get('no')
    item = Item.objects.get(it_no=itno)
    color = Color.objects.filter(it_no=item)
    option = Options.objects.filter(it_no=item)
    brand = Brand.objects.get(b_no=item.b_no.b_no)
    bigcate = Bigcate.objects.get(bigcate_no=item.bigcate_no.bigcate_no)
    
    if item.bigcate_no.bigcate_no!= 4 and item.bigcate_no.bigcate_no!= 5 :
        size = Size.objects.filter(it_no=item)
    else:
        size = Shoesize.objects.filter(it_no=item)
    
    collength = color.__len__()
    sizelength = size.__len__()
    num = color.__len__() * size.__len__()

    stock = Stock.objects.filter(b_no=brand,it_no=item)

    for st in stock:
        
        jaego = st.st_cnt
        

        if jaego == 0:
            print('들어옴')
            st.st_status = '소진'
            st.save()


    context = {
        'item' : item,
        'itno' : itno,
        'color' : color,
        'size' : size,
        'collength' : collength,
        'sizelength' : sizelength,
        'bigcate' : bigcate,
        'stock' : stock

    }

    return render(request,'merchandise/bstockcheckform.html',context)



def Brands_bstockupdateform(request:HttpRequest):
   
    #입력된 정보를 가지고오는 작업
    itno = request.GET.get('no')
    item = Item.objects.get(it_no=itno)
    color = Color.objects.filter(it_no=item)
    option = Options.objects.filter(it_no=item)
    brand = Brand.objects.get(b_no=item.b_no.b_no)
    bigcate = Bigcate.objects.get(bigcate_no=item.bigcate_no.bigcate_no)
    


    if item.bigcate_no.bigcate_no!= 4 and item.bigcate_no.bigcate_no!= 5 :
        size = Size.objects.filter(it_no=item)
    else:
        size = Shoesize.objects.filter(it_no=item)
    
    collength = color.__len__()
    sizelength = size.__len__()
    num = color.__len__() * size.__len__()
       
    

    # 상태 가지고 오는것
    # for i in range(num):
    #     globals()['status{}'.format(str(i+1))] = request.POST.get(str(i+1)+'status')
    #     if  globals()['stock{}'.format(str(i+1))] > 0:
    #         globals()['status{}'.format(str(i+1))] = '가능'
    #     else:
    #          globals()['status{}'.format(str(i+1))] = '소진'
    # try:
    #     i = 0
    #     print("i = ",i)
    #     for c in color:
    #         for s in size:
    #             if item.bigcate_no.bigcate_no!= 4 and item.bigcate_no.bigcate_no!= 5 :
    #                 stk = Stock.objects.filter(b_no=brand,it_no=item,col_no=c,s_no=s)
    #                 # print(stk.__len__())
    #                 stk.update(b_no=brand,it_no=item,col_no=c,s_no=s,st_cnt=stock[i])
    #                 # Stock.objects.create(b_no=brand,it_no=item,col_no=c,s_no=s,st_cnt=stock[i],st_sellcnt=sellcnt[i],st_status=status[i])
    #             else:
    #                 stk = Stock.objects.filter(b_no=brand,it_no=item,col_no=c,ss_no=s)
    #                 # print(stk.__len__())
    #                 stk.update(b_no=brand,it_no=item,col_no=c,ss_no=s,st_cnt=stock[i])
    #                 # Stock.objects.create(b_no=brand,it_no=item,col_no=c,ss_no=s,st_cnt=stock[i],st_sellcnt=sellcnt[i],st_status=status[i])
    #             print('성공')
    #             print("i = ",i)
    #             i+=1
    
    #     # print(num*num-num)
    #     # for i in range(num*num-num):
    #     #     st=Stock.objects.all()
    #     #     stnum =st.__len__()
    #     #     Stock.objects.filter(st_no=stnum).delete()
    # except Exception as e:
    #     print('실패')
    #     print(e)
    
    stock = Stock.objects.filter(b_no=brand,it_no=item)


    context = {
        'item' : item,
        'itno' : itno,
        'color' : color,
        'size' : size,
        'collength' : collength,
        'sizelength' : sizelength,
        'bigcate' : bigcate,
        'stock' : stock

    }

    return render(request,'merchandise/bstockupdateform.html',context)

def Brands_checkbstockupdateform(request):
    #입력된 정보를 가지고오는 작업
    itno = request.POST.get('no')
    item = Item.objects.get(it_no=itno)
    color = Color.objects.filter(it_no=item)
    option = Options.objects.filter(it_no=item)
    brand = Brand.objects.get(b_no=item.b_no.b_no)
    bigcate = Bigcate.objects.get(bigcate_no=item.bigcate_no.bigcate_no)
    


    if item.bigcate_no.bigcate_no!= 4 and item.bigcate_no.bigcate_no!= 5 :
        size = Size.objects.filter(it_no=item)
    else:
        size = Shoesize.objects.filter(it_no=item)
    
    collength = color.__len__()
    sizelength = size.__len__()
    num = color.__len__() * size.__len__()
    
    stt = Stock.objects.filter(it_no=item,col_no=color)
    status=[]
    stock = request.POST.getlist('stock')
    for i in range(stock.__len__()):
        print(i)
        stock[i] = int(stock[i])
        if  stock[i] > 0:
            status.append('가능') 
        else:
             status.append('소진')
    # 상태 가지고 오는것
    # for i in range(num):
    #     globals()['status{}'.format(str(i+1))] = request.POST.get(str(i+1)+'status')
    #     if  globals()['stock{}'.format(str(i+1))] > 0:
    #         globals()['status{}'.format(str(i+1))] = '가능'
    #     else:
    #          globals()['status{}'.format(str(i+1))] = '소진'
    try:
        i = 0
        print("i = ",i)
        for c in color:
            for s in size:
                if item.bigcate_no.bigcate_no!= 4 and item.bigcate_no.bigcate_no!= 5 :
                    stk = Stock.objects.filter(b_no=brand,it_no=item,col_no=c,s_no=s)
                    # print(stk.__len__())
                    stk.update(b_no=brand,it_no=item,col_no=c,s_no=s,st_cnt=stock[i],st_status=status[i])
                    # Stock.objects.create(b_no=brand,it_no=item,col_no=c,s_no=s,st_cnt=stock[i],st_sellcnt=sellcnt[i],st_status=status[i])
                else:
                    stk = Stock.objects.filter(b_no=brand,it_no=item,col_no=c,ss_no=s)
                    # print(stk.__len__())
                    stk.update(b_no=brand,it_no=item,col_no=c,ss_no=s,st_cnt=stock[i],st_status=status[i])
                    # Stock.objects.create(b_no=brand,it_no=item,col_no=c,ss_no=s,st_cnt=stock[i],st_sellcnt=sellcnt[i],st_status=status[i])
                print('성공')
                print("i = ",i)
                i+=1
    
        # print(num*num-num)
        # for i in range(num*num-num):
        #     st=Stock.objects.all()
        #     stnum =st.__len__()
        #     Stock.objects.filter(st_no=stnum).delete()
    except Exception as e:
        print('실패')
        print(e)
    
    stock = Stock.objects.filter(b_no=brand,it_no=item)


    context = {
        'item' : item,
        'itno' : itno,
        'color' : color,
        'size' : size,
        'collength' : collength,
        'sizelength' : sizelength,
        'bigcate' : bigcate,
        'stock' : stock

    }

    return render(request,'merchandise/bstockcheckform.html',context)

def Brands_deleteitem(request:HttpRequest):
    itno = request.GET.get('no')
    print(itno)
    try:
        item = Item.objects.filter(it_no=itno)
        print(item)
        item.delete()
        msg = '상품삭제완료'
        url = '/brands/mclist/'
    except:
        msg = '상품삭제실패'
        url = '/brands/mclist/'
    

    context={
        'msg' : msg,
        'url' : url
    }

    return render(request,'result.html',context)
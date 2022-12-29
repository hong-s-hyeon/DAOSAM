from django.shortcuts import render,redirect
from django.http import HttpRequest
from Brands.models import Brand, Item, Itemimage, Stock, Size, Shoesize,Color,Options,Bigcate,Midcate
from Members.models import User, Payment,Delivery,Grade
from .models import Basket, Buy

import datetime



# Create your views here.
def Menubar_showbrands(request:HttpRequest):

    today = datetime.datetime.today()
    before_month = today - datetime.timedelta(days=30)
    print('---------')
    print(before_month)
    print(type(before_month))

    brands = Brand.objects.filter(b_joindate__gt=before_month)
    
    context= {
        'brands' : brands
    }
    


    return render(request,'showBrands/showbrands.html',context)


def Menubar_newbrands(request:HttpRequest):
    today = datetime.datetime.today()
    before_month = today - datetime.timedelta(days=0.5)
    print('---------')
    print(before_month)
    print(type(before_month))

    brands = Brand.objects.filter(b_joindate__gt=before_month)
    
    context= {
        'brands' : brands
    }

    return render(request,'updatecontents/newbrands.html',context)


def Menubar_newitems(request:HttpRequest):
    today = datetime.datetime.today()
    before_month = today - datetime.timedelta(days=0.5)

   

    items_size= Item.objects.filter(it_regdate__gt=before_month).filter(bigcate_no__lte=3).order_by("-it_regdate")
    items_ssize= Item.objects.filter(it_regdate__gt=before_month).filter(bigcate_no__gt=3).order_by("-it_regdate")

    color_list=[]
    size_list=[]
    scolor_list=[]
    ssize_list=[]
    img_list=[]
    context={}

    if items_size.__len__()!=0:
        for item in items_size:
            color = Color.objects.filter(it_no=item)
            color_list.append(color)
            size =  Size.objects.filter(it_no=item)
            size_list.append(size)
            stock= Stock.objects.filter(it_no=item)
            imgs = Itemimage.objects.filter(it_no=item)
            img_list.append(imgs[0])
         
    
      
       
        context['stock'] = stock
        context['color'] = color
        context['size'] = size
        context['items_size'] = items_size
        context['imgs'] = imgs
        context['il'] = img_list


    simg_list=[]

    if items_ssize.__len__()!=0:
        for item in  items_ssize:
            scolor = Color.objects.filter(it_no=item)
            scolor_list.append(scolor)
            ssize =  Size.objects.filter(it_no=item)
            ssize_list.append(ssize)
            sstock= Stock.objects.filter(it_no=item)
            simgs = Itemimage.objects.filter(it_no=item)
            simg_list.append(simgs[0])
            print(simgs[0].ii_img)

        # context={
           
        #     'sstock' : sstock,
        #     'scolor' : scolor,
        #     'ssize' : ssize,
        #     'items_ssize' : items_ssize,
        #     'sil' : simg_list,
        # }
        context['sstock'] = sstock
        context['scolor'] = scolor
        context['ssize'] = ssize
        context['items_ssize'] = items_ssize
        context['simgs'] = simgs
        context['sil'] = simg_list

    return render(request,'updatecontents/newitems.html',context)




def Menubar_branditem(request:HttpRequest):
    bno = request.GET.get('no')
    brand = Brand.objects.get(b_no=bno)
    
    # 브랜드를 눌러서 들어왔으니, 브랜드 조회수 하나 증가
    brand.b_hit +=1
    brand.save()


    items_size= Item.objects.filter(b_no=brand).filter(bigcate_no__lte=3).order_by("-it_regdate")
    items_ssize= Item.objects.filter(b_no=brand).filter(bigcate_no__gt=3).order_by("-it_regdate")
    # print(items_size)
    color_list=[]
    size_list=[]
    scolor_list=[]
    ssize_list=[]
    img_list=[]
    img_reallist=[]


  



    if items_size.__len__()!=0:
        for item in items_size:
            color = Color.objects.filter(it_no=item)
            color_list.append(color)
            size =  Size.objects.filter(it_no=item)
            size_list.append(size)
            stock= Stock.objects.filter(it_no=item)
            imgs = Itemimage.objects.filter(it_no=item)
            img_list.append(imgs[0])
            print(imgs[0].ii_img)
        print(img_list)
        


        context={
            'b' : brand,
            'stock' : stock,
            'color' : color,
            'size' : size,
            'items_size' : items_size,
            'imgs' : imgs,
            'il' : img_list,
            #'ir' : img_reallist,
        }


    simg_list=[]

    if items_ssize.__len__()!=0:
        for item in  items_ssize:
            scolor = Color.objects.filter(it_no=item)
            scolor_list.append(scolor)
            ssize =  Size.objects.filter(it_no=item)
            ssize_list.append(ssize)
            sstock= Stock.objects.filter(it_no=item)
            imgs = Itemimage.objects.filter(it_no=item)
            simg_list.append(imgs[0])
           
        context={
            'b' : brand,
            'sstock' : sstock,
            'scolor' : scolor,
            'ssize' : ssize,
            'items_ssize' : items_ssize,
            'sil' : simg_list,
        }

    return render(request,'searchItem/branditems.html',context)


def Menubar_itemdetail(request:HttpRequest):
    
    # 해당 상품의 아이템 번호를 가지고온다!
    itno = int(request.GET.get('no'))
    print(itno)
    item = Item.objects.get(it_no=itno)
    print(item)
    color = Color.objects.filter(it_no=item)


    if item.bigcate_no.bigcate_no !=4 and item.bigcate_no.bigcate_no !=5:
        size = Size.objects.filter(it_no=item)
    
    else:
        size = Shoesize.objects.filter(it_no=item)
    
    
    option = Options.objects.filter(it_no=item)

    itemimage = Itemimage.objects.filter(it_no=item)
    

    
    
    context={
        'item' : item,
        'color' : color,
        'size' : size,
        'option' : option,
        'imgs' : itemimage,
        
    }

    return render(request,'item/itemdetail.html',context)


def Menubar_buyitem(request:HttpRequest):
    itno = request.GET.get('no')
    price = request.GET.get('price')
    cno = request.GET.get('selectcolor')
    sno = request.GET.get('selectsize')
    optno = request.GET.get('selectoption')
    quantity = request.GET.get('quantity')
    
    

    print(optno)
    item = Item.objects.get(it_no=itno)
    color=Color.objects.get(col_no=cno)
    
    if item.bigcate_no.bigcate_no !=4 and item.bigcate_no.bigcate_no !=5:
        size = Size.objects.get(s_no=sno)
        stock = Stock.objects.get(it_no=item,col_no=color,s_no=size)

    else:
        size = Shoesize.objects.get(ss_no=sno)
        stock = Stock.objects.get(it_no=item,col_no=color,ss_no=size)
    
    
    if optno != '':
        option = Options.objects.get(opt_no=optno)


    if stock.st_cnt >= int(quantity):


        imgs = Itemimage.objects.filter(it_no=item)
        print(imgs)
        for img in imgs:
            print(img.ii_img)
        # 유저 정보
        uno = request.session['login']
        user = User.objects.get(u_no=uno)

        payment = Payment.objects.get(u_no=user)
        delivery = Delivery.objects.get(u_no=user)
    

        if optno == '':
            context = {
                'price' : price,
                'quantity' : quantity,
                'stock' : stock,
                'user' : user,
                'payment' : payment,
                'delivery' : delivery,
                'imgs' : imgs,
                'item' : item,
                
            }
        else:
            context = {
                'price' : price,
                'quantity' : quantity,
                'stock' : stock,
                'user' : user,
                'payment' : payment,
                'delivery' : delivery,
                'imgs' : imgs,
                'item' : item,
                'option' : option,
            }


        return render(request,'buying/buyitemform.html',context)
    else:
        msg='재고가 충분하지 않습니다. 다른 상품을 선택해 주세요'
        url='/menubar/itemdetail/?no='+itno
        context = {
            'msg' : msg,
            'url' : url
        }
        return render(request,'result.html',context)

def Menubar_cateitems(request:HttpRequest):
    big = request.GET.get('b')
    mid = request.GET.get('m')

    bigcate = Bigcate.objects.get(bigcate_no=big)
    midcate = Midcate.objects.get(midcate_no=mid)


    items_size= Item.objects.filter(bigcate_no=bigcate,midcate_no=midcate).filter(bigcate_no__lte=3).order_by("-it_regdate")
    items_ssize= Item.objects.filter(bigcate_no=bigcate,midcate_no=midcate).filter(bigcate_no__gt=3).order_by("-it_regdate")
    print(items_size)
    color_list=[]
    size_list=[]
    scolor_list=[]
    ssize_list=[]
    img_list=[]
  
    if items_size.__len__()!=0:
        for item in items_size:
            color = Color.objects.filter(it_no=item)
            color_list.append(color)
            size =  Size.objects.filter(it_no=item)
            size_list.append(size)
            stock= Stock.objects.filter(it_no=item)
            imgs = Itemimage.objects.filter(it_no=item)
            img_list.append(imgs[0])
            print(imgs[0].ii_img)
        print(img_list)
        
      

        context={
            
            'stock' : stock,
            'color' : color,
            'size' : size,
            'items_size' : items_size,
            'imgs' : imgs,
            'il' : img_list,
            #'ir' : img_reallist,
        }




    if items_ssize.__len__()!=0:
        for item in  items_ssize:
            scolor = Color.objects.filter(it_no=item)
            scolor_list.append(scolor)
            ssize =  Size.objects.filter(it_no=item)
            ssize_list.append(ssize)
            stock= Stock.objects.filter(it_no=item)
            imgs = Itemimage.objects.filter(it_no=item)
            img_list.append(imgs[0])
        context={
            'stock' : stock,
            'scolor' : scolor,
            'ssize' : ssize,
            'items_ssize' : items_ssize,
            'imgs' : imgs,
            'il' : img_list,
        }


    if items_ssize.__len__()==0 and items_size.__len__()==0:
        msg='등록된 상품이 존재하지 않습니다.'
        url='/'
        context = {
            'msg' : msg,
            'url' : url
        }

        return render(request,'result.html',context)



    return render(request,'searchItem/cateitems.html',context)

def Menubar_checkbuyitemform(request:HttpRequest):
    uno = request.POST.get('uno')
    pno = request.POST.get('pno')
    dno = request.POST.get('dno')
    stno = request.POST.get('stno')
    qn = int(request.POST.get('qn'))
    itno = request.POST.get('itno')
    price = request.POST.get('price')

    tot = int(price) * int(qn)
   
    user = User.objects.get(u_no=uno)
    pay = Payment.objects.get(p_no=pno)
    deliver = Delivery.objects.get(d_no=dno)
    stock = Stock.objects.filter(st_no=stno)



    try:
        for s in stock:
            Buy.objects.create(u_no=user,p_no=pay,d_no=deliver,st_no=s,buynum=qn,buy_tot=tot)

            #상품의 제고를 1 내려주고 판매량에 1 더해주기
            cnt = s.st_cnt - int(qn)
            sellcnt = int(qn)
        stock.update(st_cnt=cnt,st_sellcnt=sellcnt)
        

        msg='결제 성공!'
        url='/menubar/buylist/'

        context= {
            'msg' : msg,
            'url' : url
        }
        return render(request,'result.html',context)

    except Exception as e:
        print(e)
        msg='결제 실패! 다시 시도해 주세요.'
        url='/'

        context= {
            'msg' : msg,
            'url' : url
        }
        return render(request,'result.html',context)

def Menubar_buylist(request:HttpRequest):
    login_uno= request.session['login']
    user = User.objects.get(u_no=login_uno)

    buylist = Buy.objects.filter(u_no=user).order_by("-buy_no")

        
    
    context={
        'buylist' : buylist,
    }

    return render(request,'buying/buylist.html',context)

def Menubar_itemlikecntup(request:HttpRequest):
    itno= request.GET.get('no')
    item = Item.objects.get(it_no=itno)
    
    item.it_likecnt+=1
    item.save()

    return redirect('/menubar/itemdetail/?no='+itno)


def Menubar_itemlikecntdown(request:HttpRequest):
    itno = request.GET.get('no')
    item = Item.objects.get(it_no=itno)

    item.it_likecnt-=1
    item.save()

    return redirect('/menubar/itemdetail/?no='+itno)


def Menubar_rankbrand(request:HttpRequest):
    brands = Brand.objects.all().order_by('-b_hit')
    
    context= {
        'brands' : brands
    }

    return render(request,'ranking/rank_brand.html',context)

def Menubar_regdateitem(request:HttpRequest):
    items = Item.objects.all().order_by('-it_regdate')
    img_list=[]
    for item in items:
        imgs = Itemimage.objects.filter(it_no=item)
        img_list.append(imgs[0])
        
    
    context = {
        'items' : items,
        'il' : img_list,
    }

    return render(request,'main_index.html',context)

def Menubar_rankitem(request:HttpRequest):
    items = Item.objects.all().order_by('-it_likecnt')
    img_list=[]
    for item in items:
        imgs = Itemimage.objects.filter(it_no=item)
        img_list.append(imgs[0])
        
    
    context = {
        'items' : items,
        'il' : img_list,
    }

    return render(request,'ranking/rank_item.html',context)


def Menubar_searchitem(request:HttpRequest):
    search = request.GET.get('sch')
    
    items = Item.objects.filter(it_name__contains=search)

    img_list=[]
    for item in items:
        imgs = Itemimage.objects.filter(it_no=item)
        img_list.append(imgs[0])
        
    
    context = {
        'items' : items,
        'il' : img_list,
    }


    return render(request,'searchItem/searchitem.html',context)

##가격순
def Menubar_priceitem(request:HttpRequest):
    items = Item.objects.all().order_by('it_price')
    img_list=[]
    for item in items:
        imgs = Itemimage.objects.filter(it_no=item)
        img_list.append(imgs[0])
        
    
    context = {
        'items' : items,
        'il' : img_list,
    }

    return render(request,'main_index.html',context)

def Menubar_discountitem(request:HttpRequest):
    items = Item.objects.all().order_by('-it_discount')
    img_list=[]
    for item in items:
        imgs = Itemimage.objects.filter(it_no=item)
        img_list.append(imgs[0])
        
    
    context = {
        'items' : items,
        'il' : img_list,
    }

    return render(request,'main_index.html',context)


def Menubar_basket(request:HttpRequest):
    itno = request.GET.get('no')
    price = request.GET.get('price')
    cno = request.GET.get('selectcolor')
    sno = request.GET.get('selectsize')
    optno = request.GET.get('selectoption')
    quantity = request.GET.get('quantity')
    

    item = Item.objects.get(it_no=itno)
    color=Color.objects.get(col_no=cno)
    
    if item.bigcate_no.bigcate_no !=4 and item.bigcate_no.bigcate_no !=5:
        size = Size.objects.get(s_no=sno)
        stock = Stock.objects.get(it_no=item,col_no=color,s_no=size)

    else:
        size = Shoesize.objects.get(ss_no=sno)
        stock = Stock.objects.get(it_no=item,col_no=color,ss_no=size)
    
    
    if optno != '':
        option = Options.objects.get(opt_no=optno)


    if stock.st_cnt >= int(quantity):


        imgs = Itemimage.objects.filter(it_no=item)
        print(imgs)
        for img in imgs:
            print(img.ii_img)
        
        uno = request.session['login']
        user = User.objects.get(u_no=uno)

        try:
            Basket.objects.create(u_no=user,st_no=stock,ba_cnt=int(quantity))
        except Exception as e:
            print(e)

        baskets = Basket.objects.all().filter(u_no=user)
        if optno == '':
            context = {
                # 'price' : price,
                # 'quantity' : quantity,
                # 'stock' : stock,
                # 'user' : user,
                # 'imgs' : imgs,
                # 'item' : item,
                'baskets' : baskets,
            }
        else:
            context = {
                # 'price' : price,
                # 'quantity' : quantity,
                # 'stock' : stock,
                # 'user' : user,
                # 'imgs' : imgs,
                # 'item' : item,
                # 'option' : option,
                'baskets' : baskets,
            }


        return render(request,'basket/basket.html',context)
    else:
        msg='재고가 충분하지 않습니다. 다른 상품을 선택해 주세요'
        url='/menubar/itemdetail/?no='+itno
        context = {
            'msg' : msg,
            'url' : url
        }
        return render(request,'result.html',context)
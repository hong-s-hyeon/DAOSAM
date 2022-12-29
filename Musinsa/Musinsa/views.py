from django.shortcuts import render,redirect
from django.http import HttpRequest
from Brands.models import Bigcate,Midcate,Item,Color,Size,Shoesize,Stock,Itemimage


def main_index(request):
    bigcate= Bigcate.objects.all()
    midcate= Midcate.objects.all()

    # bc=[]
    # mc=[]
    # for big in bigcate:
    #     bc.append(big)
    # for mid in bigcate:
    #     mc.append(mid)

    context={}

 
    context['bigcate'] = bigcate
    context['midcate'] = midcate

    items = Item.objects.all()
    img_list=[]
    for item in items:
        imgs = Itemimage.objects.filter(it_no=item)
        print(imgs)
        img_list.append(imgs[0])
    
    print(img_list)
    context['items'] = items
    context['il'] = img_list
   
    # request.session['bigcate'] = bc
    # request.session['midcate'] = mc
    

    return render(request,'main_index.html',context)
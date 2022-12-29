import random 
from django import template

register = template.Library()# tag library를 만들기 위한  모듈레벨의 인스턴스 객체

@register.filter
def mul(i,j):
    return (j*i)


@register.filter
def cal(i,j):
    a=int(j)
    b=int(i)
    return a*b
    
@register.filter
def sum(i,j):
    i=int(i)
    j=int(j)
    return (j+i)

@register.filter
def avg(i,j):
    su=i/j
    return round(su,2)

@register.filter(name='range')
def len(data):
    data = int(data)
    return range(data)

@register.filter(name='size')
def size(data):
    return range(data.__len__())

@register.filter
def indexOfimage(data,i):
    return data[i].ii_img.url

@register.filter
def discount(i,j):
    i=int(i)
    j=int(j)
    return int(i*(100-j)/100)

@register.filter
def abc(items_size,i):
    price = discount(items_size[i].it_price,items_size[i].it_discount)
    return "상품명 : " + items_size[i].it_name + "<br>정가 : " + str(items_size[i].it_price) + "원<br>할인율 : " + str(items_size[i].it_discount) + "%<br>할인가 : " + str(price) + "원<br>"

@register.filter
def allit(items_size,i):
    return str(items_size[i].it_no)

@register.filter
def randstr(i,j):
    i=str(i)
    j=str(j)
    return i.join(j)

@register.filter
def numformat(i):
    j = random.randint(1000,9999)
    return '{}{}{}'.format(i,j,i)


@register.filter
def latestitem(items_size,items_ssize):
    ls=[]
    for si in items_size:
        
        ls.append(si)
    for ssi in items_ssize:
        ls.append(ssi)
    
    return sorted(ls, key=lambda ls: ls)
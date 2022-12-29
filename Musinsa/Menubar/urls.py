from django.urls import path
from . import views

urlpatterns=[
    path('showbrands/',views.Menubar_showbrands),
    path('newbrands/',views.Menubar_newbrands),
    path('newitems/',views.Menubar_newitems),
    path('branditem/',views.Menubar_branditem),
    path('itemdetail/', views.Menubar_itemdetail),
    path('buyitem/',views.Menubar_buyitem),
    path('cateitems/',views.Menubar_cateitems),
    path('checkbuyitemform/',views.Menubar_checkbuyitemform),
    path('buylist/', views.Menubar_buylist),
    path('itemlikecntup/',views.Menubar_itemlikecntup),
    path('itemlikecntdown/',views.Menubar_itemlikecntdown),
    path('rankbrand/',views.Menubar_rankbrand),
    path('rankitem/',views.Menubar_rankitem),
    path('regdateitem/',views.Menubar_regdateitem),
    path('searchitem/',views.Menubar_searchitem),
    path('priceitem/',views.Menubar_priceitem),
    path('discountitem/',views.Menubar_discountitem),
    path('basket/',views.Menubar_basket),
    # path('refunditem/',views.Menubar_refunditem),


]
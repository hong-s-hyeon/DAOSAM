from django.urls import path,include
from . import views

urlpatterns=[
    path('',views.Brands_index),
    path('bjoinform/',views.Brands_joinform),
    path('bcheckjoinform/',views.Brands_checkjoinform),
    path('bloginform/',views.Brands_loginform),
    path('bcheckloginform/',views.Brands_checkloginform),
    path('blogout/',views.Brands_logout),
    path('bmypage/',views.Brands_mypage),
    path('bselectmode/',views.Brands_selectmode),
    path('bcheckselect/',views.Brands_checkselect),
    path('bcheckupdateform/',views.Brands_checkupdateform),
    path('mclist/',views.Brands_mclist),
    path('mcregisterform/',views.Brands_mcregisterform),
    path('bcheckmcregisterform/',views.Brands_bcheckmcregisterform),
    path('bextraAdd/',views.Brands_bextraAdd),
    path('bcheckextraddform/', views.Brands_bcheckextraddform),
    path('bstockregister/',views.Brands_bstockregister),
    path('bcheckstockregisterform/',views.Brands_checkbstockregisterform),
    path('bstockcheckform/',views.Brands_bstockcheckform),
    path('bstockupdateform/',views.Brands_bstockupdateform),
    path('checkbstockupdateform/',views.Brands_checkbstockupdateform),
    path('deleteitem/',views.Brands_deleteitem),

]
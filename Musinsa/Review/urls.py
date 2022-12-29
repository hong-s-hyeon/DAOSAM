from django.urls import path,include
from . import views

urlpatterns=[
    path('',views.Review),                          # 후기 페이지
    path('write/<int:buy_no>',views.write),     # 후기 작성 페이지
    path('checkWrite/',views.checkWrite),       # 후기 작성 확인
    path('read/',views.read),                   # 후기 읽기
    path('update/',views.update),               # 후기 수정 페이지
    path('checkUpdate/',views.checkUpdate),     # 후기 수정 확인
    path('delete/',views.delete),               # 후기 삭제
]
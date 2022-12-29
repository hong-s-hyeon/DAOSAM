from django.urls import path,include
from . import views

urlpatterns=[
    path('joinform/',views.joinform),                       # 회원가입 페이지
    path('checkjoinform/',views.checkjoinform),             # 회원가입 확인
    path('loginform/',views.loginform),                     # 로그인 페이지
    path('checkloginform/',views.checkloginform),           # 로그인 확인
    path('logout/',views.logout),                           # 로그아웃
    path('mypage/',views.mypage),                           # 마이페이지
    path('pwpage/',views.pwpage),                           # 비밀번호 확인 페이지
    path('checkPw/',views.checkPw),                         # 비밀번호 확인
    path('updateInfo/',views.updateInfo),                   # 내 정보 수정 페이지
    path('viewed_item/',views.viewed_item),                 # 최근 본 상품 페이지
    path('like_item/',views.like_item),                     # 좋아요 누른 상품 페이지
    path('basket_item/',views.basket_item),                 # 장바구니 페이지
    path('ordered_list/',views.ordered_list),               # 주문배송조회 페이지
    path('findid/',views.findid),                           # 아이디 찾기 페이지
    path('checkfindId/',views.checkfindId),                         # 아이디 찾기 확인
    path('findpw/',views.findpw),                           # 비밀번호 찾기 페이지
    path('checkfindPw/',views.checkfindPw),                         # 비밀번호 찾기 확인
]
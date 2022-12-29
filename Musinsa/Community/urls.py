from django.urls import path,include
from . import views

urlpatterns=[
    path('',views.community),                   # 커뮤니티 페이지
    path('write/<int:bo_no>',views.write),      # 글 작성 페이지
    path('checkWrite/',views.checkWrite),       # 글 작성 확인
    path('read/',views.read),                   # 글 읽기
    path('update/',views.update),               # 글 수정 페이지
    path('checkUpdate/',views.checkUpdate),     # 글 수정 확인
    path('delete/',views.delete),               # 글 삭제
    path('<int:no>/comment',views.commentInsert),       # 댓글 생성
    path('comment/<int:co_no>',views.commentDelete),    # 댓글 삭제
]
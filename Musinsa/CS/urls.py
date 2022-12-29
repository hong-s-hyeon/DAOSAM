from django.urls import path,include
from . import views

urlpatterns=[
    path('',views.CS),                   # 고객센터 페이지
    path('write/<int:qna_no>',views.write),      # 글 작성 페이지
    path('checkWrite/',views.checkWrite),       # 글 작성 확인
    path('read/',views.read),                   # 글 읽기
    path('update/',views.update),               # 글 수정 페이지
    path('checkUpdate/',views.checkUpdate),     # 글 수정 확인
    path('delete/',views.delete),               # 글 삭제
    path('<int:no>/comment',views.commentInsert),       # 댓글 생성
    path('comment/<int:cs_co_no>',views.commentDelete),    # 댓글 삭제
]
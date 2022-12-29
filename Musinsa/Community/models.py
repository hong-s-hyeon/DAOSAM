from django.db import models

from Members.models import User

# Create your models here.
class Board(models.Model):
    bo_no = models.AutoField(primary_key=True)                                  # 게시판 번호
    u_no = models.ForeignKey(User, models.DO_NOTHING, db_column='u_no')         # 유저 번호
    bo_title = models.CharField(max_length=100)                                 # 게시글 제목
    bo_date = models.DateTimeField(blank=True, null=True, auto_now_add=True)    # 게시글 날짜
    bo_hit = models.IntegerField(blank=True, null=True, default=0)              # 조회수
    bo_content = models.CharField(max_length=1000)                              # 게시글 내용
    bo_img = models.FileField(blank=True, upload_to ='community/')              # 게시글 이미지

    # 페이징 처리
    groupno = models.IntegerField(default=0)
    orderno = models.IntegerField(default=0)

    class Meta:
        db_table = 'board'
        managed = True

class Comment(models.Model):
    co_no = models.AutoField(primary_key=True)                  # 댓글 번호
    board = models.ForeignKey(Board,on_delete=models.CASCADE)   # 개별 게시글
    user = models.ForeignKey(User,on_delete=models.CASCADE)     # 개별 사용자
    content = models.TextField()                                # 댓글 내용
    logtime = models.DateTimeField(auto_now_add=True)           # 댓글 등록일

    def __str__(self) -> str:
        return str(self.no) + '\t' + self.title

    class Meta:
        db_table = 'comment'
        managed = True
        verbose_name = '답글'
        verbose_name_plural = '답글'
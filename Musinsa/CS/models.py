from django.db import models

from Members.models import User
from Brands.models import Brand

# Create your models here.

class Qcategory(models.Model):
    qcate_no = models.AutoField(primary_key=True)
    qcate_name = models.CharField(max_length=10)

    class Meta:
        db_table = 'qcategory'
        managed = True

class Faq(models.Model):
    faq_no = models.AutoField(primary_key=True)
    qcate_no = models.ForeignKey('Qcategory', models.DO_NOTHING, db_column='qcate_no')
    faq_title = models.CharField(max_length=100)
    faq_reply = models.CharField(max_length=1000)

    class Meta:
        db_table = 'faq'
        managed = True


class Qna(models.Model):
    qna_no = models.AutoField(primary_key=True)
    u_no = models.ForeignKey(User, models.DO_NOTHING, db_column='u_no')
    b_no = models.ForeignKey(Brand, models.DO_NOTHING, db_column='b_no')
    qcate_no = models.ForeignKey(Qcategory, models.DO_NOTHING, db_column='qcate_no')
    qna_title = models.CharField(max_length=100)
    qna_date = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    qna_content = models.CharField(max_length=1000)
    qna_img = models.CharField(max_length=300, blank=True, null=True)

    # 페이징 처리
    groupno = models.IntegerField(default=0)
    orderno = models.IntegerField(default=0)

    class Meta:
        db_table = 'qna'
        managed = True

class CS_Comment(models.Model):
    cs_co_no = models.AutoField(primary_key=True)                   # 고객센터 댓글 번호
    cs_board = models.ForeignKey(Qna,on_delete=models.CASCADE)      # 고객센터 개별 게시글
    cs_user = models.ForeignKey(User,null=True,on_delete=models.CASCADE)      # 고객센터 개별 사용자
    cs_brand = models.ForeignKey(Brand,null=True,on_delete=models.CASCADE)    # 고객센터 개별 브랜드
    cs_content = models.TextField()                                 # 고객센터 댓글 내용
    cs_logtime = models.DateTimeField(auto_now_add=True)            # 고객센터 댓글 등록일

    def __str__(self) -> str:
        return str(self.no) + '\t' + self.title

    class Meta:
        db_table = 'cs_comment'
        managed = True
        verbose_name = '고객센터 답글'
        verbose_name_plural = '고객센터 답글'
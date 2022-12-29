from django.db import models

# Grade 테이블 클래스
class Grade(models.Model):
    g_no = models.AutoField(primary_key=True)
    g_name = models.CharField(max_length=20)
    g_discount = models.CharField(max_length=20)
    g_limit = models.IntegerField(blank=True, null=True)
    
    class Meta:
        db_table = 'grade'
        managed = True


# User 테이블클래스
class User(models.Model):
    u_no = models.AutoField(primary_key=True)
    u_id = models.CharField(unique=True, max_length=20)
    u_pw = models.CharField(max_length=20)
    u_name = models.CharField(max_length=20)
    u_nickname = models.CharField(max_length=20)
    u_hp = models.CharField(max_length=20, blank=True, null=True)
    u_email = models.CharField(max_length=50, blank=True, null=True)
    u_birth = models.DateField(blank=True, null=True)
    u_joindate = models.DateTimeField(blank=True, null=True)
    u_self_cert = models.IntegerField(blank=True, null=True,default=0)
    u_refundnum = models.CharField(max_length=20, blank=True, null=True)
    u_point = models.IntegerField(blank=True, null=True,default=0)
    g_no = models.ForeignKey(Grade,on_delete=models.CASCADE, db_column='g_no', blank=True, null=True,default=1)
    u_dep = models.IntegerField(blank=True, null=True,default=0)

    def __str__(self) -> str:
        return self.u_name
    class Meta:
        db_table = 'user'
        managed = True


# 테이블을 순서대로 불러온다
# 테이블 내부에 수정해야하는 것을 수정한다.
# cmd창에서 샘플데이터 추가

# Payment 테이블클래스
class Payment(models.Model):
    p_no = models.AutoField(primary_key=True)
    u_no = models.ForeignKey(User, on_delete=models.CASCADE, db_column='u_no')
    p_name = models.CharField(max_length=20)
    p_cardnum = models.CharField(max_length=20)

    class Meta:
        db_table = 'payment'
        managed = True

# Delivery 테이블클래스
class Delivery(models.Model):
    d_no = models.AutoField(primary_key=True)
    u_no = models.ForeignKey(User,on_delete=models.CASCADE, db_column='u_no')
    d_addr = models.CharField(max_length=50)
    d_recipient = models.CharField(max_length=20)
    d_name = models.CharField(max_length=20)
    d_phone = models.CharField(max_length=20)
    d_option = models.CharField(max_length=100, blank=True, null=True, default='없음')

    class Meta:
        db_table = 'delivery'
        managed = True
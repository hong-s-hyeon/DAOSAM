from django.db import models

#파일 삭제를 위한 임포트
from django.db.models.signals import post_delete
from django.dispatch import receiver


def id_dir_path(instance,filename):

    return '{}/{}'.format(instance.ii_id,filename)


# Create your models here.
class Brandcate(models.Model):
    bc_no = models.AutoField(primary_key=True)
    bc_catename = models.CharField(max_length=20)

    class Meta:
        db_table = 'brandcate'
        managed = True
   

    def __str__(self) -> str:
        return str(self.bc_no)

class Brand(models.Model):
    b_no = models.AutoField(primary_key=True)
    bc_no = models.ForeignKey(Brandcate, on_delete = models.CASCADE, db_column='bc_no')
    b_url = models.CharField(max_length=100)
    b_addr = models.CharField(max_length=30)
    b_managername = models.CharField(max_length=20)
    b_korname = models.CharField(max_length=20)
    b_engname = models.CharField(max_length=20)
    b_info = models.TextField()
    b_img = models.FileField(null=True,upload_to='brands_img/')
    b_id = models.CharField(max_length=20)
    b_pw = models.CharField(max_length=20)
    b_hp = models.CharField(max_length=20)
    b_email = models.CharField(max_length=20)
    b_serialnum = models.CharField(max_length=20)
    b_joindate = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    b_refund_num = models.CharField(max_length=20, blank=True, null=True, default='등록필요')
    b_likecnt = models.IntegerField(blank=True, null=True, default=0)
    b_dep = models.IntegerField(blank=True, null=True, default=1)
    b_confirm = models.IntegerField(blank=True, null=True,default=2)
    b_sellmoney = models.IntegerField(blank=True, null=True, default=0)
    b_hit = models.IntegerField(blank=True, null=True,default=0)
    b_sellcnt = models.IntegerField(blank=True, null=True,default=0)
    
    class Meta:
        db_table = 'brand'
        managed = True
  

@receiver(post_delete,sender=Brand)
def deleteFile(sender,**kwargs):
    b = kwargs.get('instance')
    b.b_img.delete(save=False)






# 상품 관련 테이블
class Bigcate(models.Model):
    bigcate_no = models.AutoField(primary_key=True)
    bigcate_name = models.CharField(max_length=20)

   
    def __str__(self) -> str:
        return str(self.bigcate_no)

    class Meta:
        db_table = 'bigcate'
        managed = True

class Midcate(models.Model):
    midcate_no = models.AutoField(primary_key=True)
    bigcate_no = models.ForeignKey(Bigcate, on_delete = models.CASCADE, db_column='bigcate_no')
    midcate_name = models.CharField(max_length=20)

    class Meta:
        db_table = 'midcate'
        managed = True



class Item(models.Model):
    it_no = models.AutoField(primary_key=True)
    bigcate_no = models.ForeignKey(Bigcate, on_delete = models.CASCADE, db_column='bigcate_no')
    midcate_no = models.ForeignKey(Midcate, on_delete = models.CASCADE, db_column='midcate_no')
    b_no = models.ForeignKey(Brand, on_delete = models.CASCADE, db_column='b_no')
    it_name = models.CharField(max_length=20)
    it_info = models.CharField(max_length=300)
    it_price = models.IntegerField()
    it_point = models.IntegerField()
    it_discount = models.IntegerField()
    it_regdate = models.DateTimeField(blank=True, null=True,auto_now_add=True)
    it_likecnt = models.IntegerField(blank=True, null=True, default=0)

    class Meta:
        db_table = 'item'
        managed = True



class Size(models.Model):
    s_no = models.AutoField(primary_key=True)
    it_no = models.ForeignKey(Item, on_delete = models.CASCADE, db_column='it_no')
    bigcate_no = models.ForeignKey(Bigcate, on_delete = models.CASCADE, db_column='bigcate_no')
    s_name = models.CharField(max_length=20)

    class Meta:
        db_table = 'size'
        managed = True



class Shoesize(models.Model):
    ss_no = models.AutoField(primary_key=True)
    it_no = models.ForeignKey(Item, on_delete = models.CASCADE, db_column='it_no')
    bigcate_no = models.ForeignKey(Bigcate, on_delete = models.CASCADE, db_column='bigcate_no')
    ss_name = models.CharField(max_length=20)

    class Meta:
        db_table = 'shoesize'
        managed = True   



class Color(models.Model):
    col_no = models.AutoField(primary_key=True)
    it_no = models.ForeignKey(Item, on_delete = models.CASCADE, db_column='it_no')
    col_name = models.CharField(max_length=20)
    
    class Meta:
        db_table = 'color'
        managed = True  



class Options(models.Model):
    opt_no = models.AutoField(primary_key=True)
    it_no = models.ForeignKey(Item, on_delete = models.CASCADE, db_column='it_no')
    opt_name = models.CharField(max_length=20)

    class Meta:
        db_table = 'options'
        managed = True 



class Itemimage(models.Model):
    ii_no = models.AutoField(primary_key=True)
    it_no = models.ForeignKey(Item, on_delete = models.CASCADE, db_column='it_no')
    ii_id = models.CharField(max_length=20, blank=True, null=True)
    ii_img = models.FileField(null=True,upload_to=id_dir_path)

    class Meta:
        db_table = 'itemimage'
        managed = True


@receiver(post_delete,sender=Itemimage)
def deletFile(sender,**kwargs):
    iimg = kwargs.get('instance')
    iimg.ii_img.delete(save=False)



class Stock(models.Model):
    st_no = models.AutoField(primary_key=True)
    b_no = models.ForeignKey(Brand, on_delete = models.CASCADE, db_column='b_no')
    it_no = models.ForeignKey(Item, on_delete = models.CASCADE, db_column='it_no')
    col_no = models.ForeignKey(Color, on_delete = models.CASCADE, db_column='col_no')
    s_no = models.ForeignKey(Size, on_delete = models.CASCADE, db_column='s_no', blank=True, null=True)
    ss_no = models.ForeignKey(Shoesize, on_delete = models.CASCADE, db_column='ss_no',blank=True, null=True)
    # opt_no = models.ForeignKey(Options, on_delete = models.CASCADE, db_column='opt_no',blank=True, null=True)
    st_cnt = models.IntegerField()
    st_sellcnt = models.IntegerField()
    st_status = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'stock'
        managed = True
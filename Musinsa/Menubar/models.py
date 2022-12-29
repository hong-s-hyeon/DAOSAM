from django.db import models
from Members.models import User,Payment,Delivery
from Brands.models import Stock

# Create your models here.
class Buy(models.Model):
    buy_no = models.AutoField(primary_key=True)
    u_no = models.ForeignKey(User, on_delete=models.CASCADE, db_column='u_no')
    p_no = models.ForeignKey(Payment, on_delete=models.CASCADE, db_column='p_no')
    d_no = models.ForeignKey(Delivery, on_delete=models.CASCADE, db_column='d_no', default=1)
    st_no = models.ForeignKey(Stock, on_delete=models.CASCADE, db_column='st_no')
    buydate = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    buynum = models.IntegerField(blank=True, null=True)
    buystatus = models.CharField(max_length=20, blank=True, null=True)
    buy_tot = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'buy'

class Basket(models.Model):
    ba_no = models.AutoField(primary_key=True)
    u_no = models.ForeignKey(User, on_delete=models.CASCADE, db_column='u_no')
    st_no = models.ForeignKey(Stock, on_delete=models.CASCADE, db_column='st_no')
    ba_cnt = models.IntegerField(blank=True,null=True)

    class Meta:
        managed = True
        db_table = 'basket'
from django.db import models

from Menubar.models import Buy
from Brands.models import Brand
from Members.models import User

class Mark(models.Model):
    m_no = models.AutoField(primary_key=True)
    buy_no = models.ForeignKey(Buy, models.DO_NOTHING, db_column='buy_no')
    u_no = models.ForeignKey(User, models.DO_NOTHING, db_column='u_no')
    b_no = models.ForeignKey(Brand, models.DO_NOTHING, db_column='b_no')
    m_size = models.IntegerField()
    m_color = models.IntegerField()
    m_puton = models.IntegerField()
    m_rebuy = models.IntegerField()
    m_tot = models.DecimalField(max_digits=3, decimal_places=2)
    m_logtime = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    m_content = models.CharField(max_length=1000)
    m_title = models.CharField(max_length=100)
    m_img = models.CharField(max_length=300, blank=True, null=True)

    # 페이징 처리
    groupno = models.IntegerField(default=0)
    orderno = models.IntegerField(default=0)

    class Meta:
        db_table = 'mark'
        managed = True
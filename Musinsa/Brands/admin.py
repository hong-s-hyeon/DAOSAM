from django.contrib import admin
from .models import Brand, Size
# Register your models here.


@admin.register(Brand)
class BrandsAdmin(admin.ModelAdmin):
    
    # url'admin/'에서 '사용자들'에 사용자를 등록할 때 뜨는 필드들이다.
    list_display= (
        'b_no',
        'bc_no',
        'b_url',
        'b_addr',
        'b_managername',
        'b_korname',
        'b_korname',
        'b_img',
        'b_serialnum',
        'b_dep',
        'b_confirm'
        

    )
    # url'admin/'에서 '사용자들'에서 해당 필드의 값을 클릭했을 때 상세로 넘어가게끔 링크를 걸어줄 애들을 정하는 곳
    list_display_links =(
        'b_confirm',
    )

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    
    # url'admin/'에서 '사용자들'에 사용자를 등록할 때 뜨는 필드들이다.
    list_display= (
        's_no',
        'it_no',
        'bigcate_no',
        's_name'

        

    )
    # url'admin/'에서 '사용자들'에서 해당 필드의 값을 클릭했을 때 상세로 넘어가게끔 링크를 걸어줄 애들을 정하는 곳
    list_display_links =(
        's_no',
    )
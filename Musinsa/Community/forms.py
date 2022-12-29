from unicodedata import name
from django import forms
from .models import Board
from django_summernote.fields import SummernoteTextFormField
from django_summernote.widgets import SummernoteWidget

#Form 클래스 정의
# - Form태그를 통하여 입력받는 클래스...
# - HTML 코드 내부에 입력창을 우리가 일일이 지정할 필요가 없다...형식이 제한적이다...

class BoardWriteForm(forms.ModelForm):
    # 필드 정의
    bo_title = forms.CharField(
        label='제목',
        widget=forms.TextInput(
            attrs= { # 태그에 들어갈 속성 지정하는 부분..
                'placeholder' : '게시글 제목',
                'id' : 'bo_title',
            }
        )
    )

    bo_content = forms.CharField(widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '500px'}}))

    class Meta:
        model = Board # 이 form클래스는 Board 테이블을 바탕으로 사용할 것이다.
        fields = [ #현재 form에서  사용할 데이터 필드 지정...
            'bo_title',
            'bo_content',
        ]
        # widgets = {
        #     'content' : SummernoteWidget(
        #         attrs={
        #             'summernote' : {
        #                 'width' : '50%',
        #                 'height' : '400px',
        #             }
        #         }
        #     ),
        # }

    def clean(self):
        cleaned_data = super(Board,self).clean()

        bo_title = cleaned_data.get('bo_title','')
        bo_content = cleaned_data.get('bo_contents','')
    
        if bo_title == '':
            self.add_error('bo_title','제목 입력하세요')
        elif bo_content == '':
            self.add_error('bo_content','글 내용을 입력하세요')
        else:
            self.bo_title = bo_title
            self.bo_content = bo_content

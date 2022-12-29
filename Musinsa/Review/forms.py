from unicodedata import name
from django import forms
from .models import Mark
from django_summernote.fields import SummernoteTextFormField
from django_summernote.widgets import SummernoteWidget

#Form 클래스 정의
# - Form태그를 통하여 입력받는 클래스...
# - HTML 코드 내부에 입력창을 우리가 일일이 지정할 필요가 없다...형식이 제한적이다...

class MarkWriteForm(forms.ModelForm):
    # 필드 정의
    m_title = forms.CharField(
        label='제목',
        widget=forms.TextInput(
            attrs= { # 태그에 들어갈 속성 지정하는 부분..
                'placeholder' : '후기 제목',
                'id' : 'm_title',
            }
        )
    )

    m_content = forms.CharField(widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '500px'}}))

    class Meta:
        model = Mark # 이 form클래스는 Mark 테이블을 바탕으로 사용할 것이다.
        fields = [ #현재 form에서  사용할 데이터 필드 지정...
            'm_title',
            'm_content',
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
        cleaned_data = super(Mark,self).clean()

        m_title = cleaned_data.get('m_title','')
        m_content = cleaned_data.get('m_contents','')
    
        if m_title == '':
            self.add_error('m_title','제목 입력하세요')
        elif m_content == '':
            self.add_error('m_content','후기 내용을 입력하세요')
        else:
            self.m_title = m_title
            self.m_content = m_content

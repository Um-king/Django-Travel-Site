from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    tags = forms.CharField(required=False, help_text="태그를 쉼표로 구분하여 입력하세요.")
    
    class Meta:
        model = Post
        fields = ['title', 'contents', 'image', 'category', 'fromDate', 'toDate', 'count', 'subContent', 'tags']
        widgets = {
            'fromDate': forms.DateInput(attrs={'type': 'date', 'required': 'False'}),
            'toDate': forms.DateInput(attrs={'type': 'date', 'required': 'False'}),
        }
        required = {
            'category': False,
            'fromDate': False,
            'toDate': False,
            'count': False,
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['message']



class TravelerForm(forms.Form):
    GENDER = forms.ChoiceField(choices=[('남', '남'), ('여', '여')])
    AGE_GRP = forms.FloatField()
    TRAVEL_STYL_1 = forms.IntegerField()
    TRAVEL_STYL_2 = forms.IntegerField()
    TRAVEL_STYL_3 = forms.IntegerField()
    TRAVEL_STYL_4 = forms.IntegerField()
    TRAVEL_STYL_5 = forms.IntegerField()
    TRAVEL_STYL_6 = forms.IntegerField()
    TRAVEL_STYL_7 = forms.IntegerField()
    TRAVEL_STYL_8 = forms.IntegerField()
    TRAVEL_MOTIVE_1 = forms.IntegerField()
    TRAVEL_COMPANIONS_NUM = forms.IntegerField()
    TRAVEL_MISSION_INT = forms.IntegerField()




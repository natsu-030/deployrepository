from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'efforts', 'encouragement', 'is_public']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'efforts': forms.Textarea(attrs={'class': 'form-control', 'required': True}),
            'encouragement': forms.Textarea(attrs={'class': 'form-control', 'required': True}),    
            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['is_public'].initial = True  # デフォルトでチェックされるように設定
        
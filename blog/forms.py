from  django import forms
from django.forms import ModelForm
from blog.models import (Comment)


class CommentForm(ModelForm):
	class Meta:
		model = Comment
		fields = '__all__'
		widgets = {
			'article': forms.Select(attrs = {'id':'article',\
				'class':'stext-111 cl2 plh3 size-116 p-lr-18 invisible',\
				}),
			'name': forms.TextInput(attrs = {'id':'name',\
				'class':'stext-111 cl2 plh3 size-116 p-lr-18',\
				'placeholder':'Name *'}),
			'comment': forms.Textarea(attrs = {'id':'comment',\
				'class':'stext-111 cl2 plh3 size-124 p-lr-18 p-tb-15',\
				'placeholder':'Comment...',
				'rows':'4'}),
			'email': forms.EmailInput(attrs = {'id':'email',\
				'class':'stext-111 cl2 plh3 size-116 p-lr-18',
				'placeholder':'Email *'}),
			'website': forms.TextInput(attrs = {'id':'website',\
				'class':'stext-111 cl2 plh3 size-116 p-lr-18',
				'placeholder':'Website'})
		}

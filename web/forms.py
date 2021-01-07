
from django import forms
from django.forms import ModelForm
from web.models import (Subscriber, Client, Cart)

class SubscribeForm(ModelForm):
	class Meta:
		model = Subscriber
		fields = '__all__'
		widgets = {
		'email': forms.EmailInput(attrs = {
			'class':'input1 bg-none plh1 stext-107 cl7',
			'placeholder':'email@example.com'
			})
		}

class ClientForm(ModelForm):
	class Meta:
		model = Client
		fields = '__all__'
		widgets = {
		'name': forms.TextInput(attrs = {
			'class':'stext-111 cl2 plh3 size-116 p-l-62 p-r-30',
			'placeholder':'Name/Company',
			'name':'name'
			}),
		'email': forms.EmailInput(attrs = {
			'class':'stext-111 cl2 plh3 size-116 p-l-62 p-r-30',
			'placeholder':'Your Email Address',
			'name':'email'
			}),
		'message': forms.Textarea(attrs = {
			'class':'stext-111 cl2 plh3 size-120 p-lr-28 p-tb-25',
			'placeholder':'How Can We Help?',
			'name':'msg'
			}),
		}

class CartForm(forms.ModelForm):
	class Meta:
		model = Cart
		fields = '__all__'
		widgets = {
		'cart_id': forms.HiddenInput(),
		'cart_products': forms.SelectMultiple(attrs = {
			'class':'form-control'
			})
		}

class SearchForm(forms.Form):
	search_query = forms.CharField(max_length = 100, widget = forms.TextInput(attrs = {
		'class':'plh3',
		'placeholder':'Search...',
		'name':'search'
		}))

class ProductSearchForm(forms.Form):
	search_query = forms.CharField(max_length = 100, widget = forms.TextInput(attrs = {
		'class':'mtext-107 cl2 size-114 plh2 p-r-15',
		'placeholder':'Search',
		'name':'search-product'
		}))

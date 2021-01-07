import random, json, requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.template.loader import render_to_string
from django.views import View, generic
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .filters import ProductFilter
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from django.utils.crypto import get_random_string
from django.conf import settings

from django.core.paginator import (Paginator, 
                                   EmptyPage, 
                                   PageNotAnInteger)

from web.models import (Product,
                        Categorie,
                         SiteDetail,
                         FAQ,
                         SlideProduct,
                         Cart,
                         Client,
                         Order,
                         SearchQuery,
                         BillingForm, 
                         BillingAddress)

from web.forms import (SubscribeForm,
                       ClientForm,
                       SearchForm, 
                       ProductSearchForm,
                       CartForm)


# Create your views here.

################################
#
#
#   CUSTOM FUNCTION AND CLASSES
#
################################
def auto_paginate(queryset, request, get_arg = 'page',paginate_by = 10):
    page = request.GET.get(get_arg, 1)
    paginator = Paginator(queryset, paginate_by)
    try:
        return paginator.page(page)
    except PageNotAnInteger:
        return paginator.page(1)
    except EmptyPage:
        return paginator.page(paginator.num_pages)

def cart_total(user):
    order = Order.objects.filter(user=user, ordered=False)

    if order.exists():
        return order[0].orderitems.count()
    else:
        return 0

###########
#
#
#   END
#
#
###########

class Index(View):
    ''' This view launches the landing page
    of the website'''

    def get(self, request, ** kwargs):
        ''' This the get method for the
        index view'''
        context = {}
        template = 'web/index_fix.html'
        try:
            context['form_status'] = kwargs['form_status']
        except:
            pass
        try:
            order = Order.objects.filter(user=request.user, ordered=False)
            if order.exists():
                context['cart'] = order[0]
            else: 
                context['cart'] = order
        except: 
            pass
        context['active_home'] = True
        context['subscribeform'] = SubscribeForm()
        context['site_details'] = SiteDetail.objects.get()
        context['slide_products'] = SlideProduct.objects.all().order_by('-upload_timestamp')
        product_list = Product.objects.all().order_by('-upload_timestamp')
        context['categories'] = Categorie.objects.all()
        context['products'] = auto_paginate(request=request,queryset = product_list , paginate_by = 16)
        return render(request, template, context)

class ProductDetail(View):
    '''This view renders the product
    detail page'''

    def get(self, request, **kwargs):
        '''This is the get method
        for ProductDetail'''
        template = 'web/product-detail.html'
        context = {}
        try:
            order = Order.objects.filter(user=request.user, ordered=False)
            if order.exists():
                context['cart'] = order[0]
            else:
                context['cart'] = order
        except: 
            pass
        context['active_category'] = True
        context['site_details'] = SiteDetail.objects.get()
        context['subscribeform'] = SubscribeForm()
        context['categories'] = Categorie.objects.all()
        context['product'] = Product.objects.get(slug = kwargs['slug'])
        related_products_list = []
        for category in context['product'].product_category.all():
            related_products_list.append(Product.objects.filter( product_category__name = category.name ))
        context['related_products_list'] = related_products_list

        return render(request, template, context)

class CategoryView(View):
    '''This is the view that renders a single
    category of all the categories available'''
    def _fetch_category_product(self, category):
        get_category = Categorie.objects.get(name = category)
        get_products = Product.objects.filter(product_category = get_category)
        return get_products


    def get(self, request, **kwargs):
        fetch_category = kwargs['category']
        template = 'web/category.html'
        context = {}
        try:
            order = Order.objects.filter(user=request.user, ordered=False)
            if order.exists():
                context['cart'] = order[0]
            else:
                context['cart'] = order
        except: 
            pass
        product_list = self._fetch_category_product(category = fetch_category)
        context['active_category'] = True
        context['current_category'] = fetch_category
        context['products'] = auto_paginate(request= request,queryset= product_list, paginate_by = 3)
        context['site_details'] = SiteDetail.objects.get()
        context['subscribeform'] = SubscribeForm()
        context['categories'] = Categorie.objects.all()
        return render(request, template, context)



class FAQView(View):

    def get(self, request):
        '''This is the get method for the
        FAQ view '''
        context = {}
        template = 'web/faq.html'
        faq_list = FAQ.objects.all().order_by('-upload_timestamp')
        try:
            order = Order.objects.filter(user=request.user, ordered=False)
            if order.exists():
                context['cart'] = order[0]
            else:
                context['cart'] = order
        except: 
            pass
        context['faqs'] = auto_paginate(request=request,queryset = faq_list , paginate_by = 1)
        context['site_details'] = SiteDetail.objects.get()
        context['subscribeform'] = SubscribeForm()
        context['categories'] = Categorie.objects.all()
        return render(request, template, context)

class ContactView(View):

    def get(self, request, ** kwargs):
        '''This is the get method for the
        contact view '''
        context = {}
        try:
            context['form_status'] = kwargs['form_status']
        except:
            pass
        template = 'web/contact.html'
        context['active_contact'] = True
        try:
            order = Order.objects.filter(user=request.user, ordered=False)
            if order.exists():
                context['cart'] = order[0]
            else:
                context['cart'] = order
        except: 
            pass
        context['client_form'] = ClientForm()
        context['site_details'] = SiteDetail.objects.get()
        context['subscribeform'] = SubscribeForm()
        context['categories'] = Categorie.objects.all()
        return render(request, template, context)

class Client(View):

    def post(self, request, ** kwargs):
        '''This is the view that handles
        new clients from the contact page'''
        new_client = ClientForm(request.POST)
        if(new_client.is_valid()):
            new_client.save()
            return ContactView().get(request, form_status = 'success')
        else:
            return ContactView().get(request, form_status = 'fail')


class SubscribeView(View):
    def post(self, request):
        '''This view handles new 
        subscribers'''
        new_subscriber = SubscribeForm(request.POST)
        if(new_subscriber.is_valid()):
            new_subscriber.save()
            return Index().get(request, form_status = 'success')
        else:
            return Index().get(request, form_status = 'fail')


class AboutView(View):
    
    def get(self, request):
        '''This is the get method
        for the About view'''
        template = 'web/about.html'
        context = {}
        try:
            order = Order.objects.filter(user=request.user, ordered=False)
            if order.exists():
                context['cart'] = order[0]
            else:
                context['cart'] = order
        except: 
            pass
        context['active_about'] = True
        context['site_details'] = SiteDetail.objects.get()
        context['subscribeform'] = SubscribeForm()
        context['categories'] = Categorie.objects.all()
        return render(request, template, context)

# Add to Cart View
class AddToCart(LoginRequiredMixin, View):

    def post(self, request):
        '''This method adds user selected
        products to their carts'''
        context = {}
        template = 'web/cart.html'
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('num_product')
        new_item = Product.objects.get( slug = product_id)
        order_item, created = Cart.objects.get_or_create(
            product=new_item,
            user=request.user,
            purchased=False,
        )
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            # check if the order item is in the order
            if order.orderitems.filter(product__slug=new_item.slug).exists():
                    order_item.quantity = quantity
                    order_item.save()
                    context['cart'] = order
                    content = {}
                    content['html'] = render_to_string(template, context)
                    content['count'] = cart_total(request.user)
                    content = json.dumps(content)
                    messages.info(request, f"{new_item.name} quantity has  been updated.")
                    return HttpResponse(content)
            else:
                order.orderitems.add(order_item)
                order_item.quantity = quantity
                order_item.save()
                messages.info(request, f"{new_item.name} has been added to your cart.")
                context['cart'] = order
                content = {}
                content['html'] = render_to_string(template, context)
                content['count'] = cart_total(request.user)
                content = json.dumps(content)
                return HttpResponse(content)
        else:
            order = Order.objects.create(
                user=request.user)
            order_item.quantity = quantity
            order_item.save()
            order.orderitems.add(order_item)
            messages.info(request, f"{new_item.name} has been added to your cart.")          
            context['cart'] = order
            content = {}
            content['html'] = render_to_string(template, context)
            content['count'] = cart_total(request.user)
            content = json.dumps(content)
            return HttpResponse(content)

class ViewCart(LoginRequiredMixin, View):
    '''This view gives a summary of all
    the products and quantitites available
    in the cart'''
    def get(self, request, ** kwargs):
        ''' This the get method for the
        index view'''
        context = {}
        template = 'web/shopping-cart.html'

        user = request.user
        carts = Cart.objects.filter(user=user, purchased=False)
        orders = Order.objects.filter(user=user, ordered=False)
        try:
            context['form_status'] = kwargs['form_status']
        except:
            pass
        if carts.exists():
            if orders.exists():
                order = orders[0]
                context['cart'] = Order.objects.filter(user=request.user, ordered=False)[0]
                context['active_home'] = True
                context['categories'] = Categorie.objects.all()
                context['subscribeform'] = SubscribeForm()
                context['site_details'] = SiteDetail.objects.get()
                return render(request, template, context)
            else:
                messages.warning(request, "You do not have any item in your Cart")
                context['cart'] = Order.objects.filter(user=request.user, ordered=False)
                context['active_home'] = True
                context['categories'] = Categorie.objects.all()
                context['subscribeform'] = SubscribeForm()
                context['site_details'] = SiteDetail.objects.get()
                return render(request, template, context)
            
        else:
            messages.warning(request, "You do not have any item in your Cart")
            context['cart'] = Order.objects.filter(user=request.user, ordered=False)
            context['active_home'] = True
            context['categories'] = Categorie.objects.all()
            context['subscribeform'] = SubscribeForm()
            context['site_details'] = SiteDetail.objects.get()
            return render(request, template, context)



class UpdateCart(LoginRequiredMixin, View):
    '''This is the view for removing of
     products in the cart'''
    def get(self, request, **kwargs):
        new_item = Product.objects.get( slug = kwargs['slug'])
        order_qs = Order.objects.filter(
            user=request.user,
            ordered=False
        )
        if order_qs.exists():
            order = order_qs[0]
            # check if the order item is in the order
            if order.orderitems.filter(product__slug=new_item.slug).exists():
                order_item = Cart.objects.filter(
                    product=new_item,
                    user=request.user
                )[0]
                order.orderitems.remove(order_item)
                order_item.delete()
                messages.warning(request, f"{new_item.name} has been removed from your cart.")
                return redirect("web:view_cart")
            else:
                messages.info(request, f"{new_item.name} not in the active order.")
                return redirect("web:view_cart")
        else:
            messages.info(request, "You do not have an active order")
            return redirect("web:view_cart")

class HeaderSearch(View):
    '''This is the view for query
    database for searches'''
    def post(self, request):
        new_search = SearchForm(request.POST)

def search_view(request):
    query = request.GET.get('q', None)
    user = None
    context = {}
    try:
        order = Order.objects.filter(user=request.user, ordered=False)
        if order.exists():
            context['cart'] = order[0]
        else:
            context['cart'] = order
    except: 
        pass
    if request.user.is_authenticated:
        user = request.user
    context["query"] = query
    if query is not None:
        SearchQuery.objects.create(user=user, query=query)
        blog_list = Product.objects.search(query=query)
        context['blog_list'] = blog_list
    context['subscribeform'] = SubscribeForm()
    context['site_details'] = SiteDetail.objects.get()
    context['categories'] = Categorie.objects.all()
    return render(request, 'web/view.html',context)

@login_required
def checkout(request):

    # Checkout view
    form = BillingForm
    context = {}
    order_qs = Order.objects.filter(user= request.user, ordered=False)
    if order_qs.exists():
        order_items = order_qs[0].orderitems.all()
        order_total = order_qs[0].total_price()
        context["form"] = form
        context["order_items"] =  order_items
        context["order_total"] = order_total
        # Getting the saved saved_address
        saved_address = BillingAddress.objects.filter(user = request.user)
        if saved_address.exists():
            savedAddress = saved_address.first()
            context["savedAddress"] = savedAddress
            context['firstname'] = savedAddress.firstname
            context['lastname'] = savedAddress.lastname
        if request.method == "POST":
            saved_address = BillingAddress.objects.filter(user = request.user)
            if saved_address.exists():
                savedAddress = saved_address.first()
                form = BillingForm(request.POST, instance=savedAddress)
                if form.is_valid():
                    billingaddress = form.save(commit=False)
                    billingaddress.user = request.user
                    billingaddress.save()
            else:
                form = BillingForm(request.POST)
                if form.is_valid():
                    billingaddress = form.save(commit=False)
                    billingaddress.user = request.user
                    billingaddress.save()
        context['cart'] = order_qs[0]
        context['subscribeform'] = SubscribeForm()
        context['site_details'] = SiteDetail.objects.get()
        context['categories'] = Categorie.objects.all()
        context['key'] = ''
        context['email'] = request.user.email
        context['id'] = get_random_string(length=16, allowed_chars=u'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')                    
        return render(request, 'web/details.html', context)
    else:
        return redirect("web:view_cart")



@login_required
def charge(request, **kwargs):
    YOUR_SECRET_KEY = ''
    url_2 = 'https://api.paystack.co/transaction/verify/{}'.format(kwargs['reference'])
    response = requests.get(url_2,
      headers={'Authorization': 'Bearer {}'.format(YOUR_SECRET_KEY)})
    if response.json()['status'] == False:
        pass
    else:
        if response.json()['data']['status'] == "success":
            order = Order.objects.get(user=request.user, ordered=False)
            orderId = get_random_string(length=16, allowed_chars=u'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
            order.ordered = True
            order.paymentId = kwargs['reference'] 
            order.orderId = '{0}{1}'.format(request.user, orderId)
            order.save()
            cartItems = Cart.objects.filter(user=request.user)
            for item in cartItems:
              item.purchased = True
              item.save() 
    content = json.dumps(response.json())
    return HttpResponse(content)
    

@login_required
def oderView(request):
    context = {}
    try:
        orders = Order.objects.filter(user=request.user, ordered=True)
        context["orders"] = orders
    except:
        messages.warning(request, "You do not have an active order")
        return redirect('web:web_index')
    context['subscribeform'] = SubscribeForm()
    context['site_details'] = SiteDetail.objects.get()
    context['categories'] = Categorie.objects.all()
    return render(request, 'web/order.html', context)
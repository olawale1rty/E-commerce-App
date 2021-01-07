from django.urls import path
import web.views as views

app_name = 'web'
urlpatterns = [
    path('index/', views.Index.as_view(), name = 'web_index'),
    path('product/<slug:slug>', views.ProductDetail.as_view(), name = 'product_detail'),
    path('categories/<str:category>', views.CategoryView.as_view(), name = 'product_categories'),
    path('FAQ/', views.FAQView.as_view(), name = 'qa'),
    path('contact/', views.ContactView.as_view(), name = 'contact'),
    path('new_client/', views.Client.as_view(), name = 'new_client'),
    path('subscribe/', views.SubscribeView.as_view(), name = 'subscribe'),
    path('about/', views.AboutView.as_view(), name = 'about'),
    path('add_to_cart/',views.AddToCart.as_view(), name = 'add_2_cart'),
    path('view_cart_contents/',views.ViewCart.as_view(), name = 'view_cart'),
    path('update_cart/<slug:slug>',views.UpdateCart.as_view(), name = 'update_cart'),
    
    path('checkout/', views.checkout, name="checkout"),
    path('verify_transaction/<str:reference>', views.charge, name="charge"),
    path('my-orders/', views.oderView, name="oderView")
]


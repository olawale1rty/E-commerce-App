from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db.models import Q
from django.utils import timezone
from django.forms import ModelForm

# Get the user model
User = get_user_model()

# Create your models here.

class SiteDetail(models.Model):
    name = models.CharField(max_length = 100)
    logo = models.ImageField(upload_to = 'site_detail/images')
    favicon = models.ImageField(upload_to = 'site_detail/images')
    apple_icon = models.ImageField(upload_to = 'site_detail/images')
    address = models.TextField()
    site_email = models.EmailField()
    site_biography = models.TextField()
    site_mission = models.TextField()
    site_quote = models.TextField()
    site_quote_by = models.TextField()
    our_story_image = models.ImageField(upload_to = 'site_detail/images', blank = True)
    our_mission_image = models.ImageField(upload_to = 'site_detail/images', blank = True)

    def __str__(self):
        return self.name

class PhoneNumber(models.Model):
    name = models.CharField(max_length = 70)
    phone_number = models.CharField(max_length = 14)
    site = models.ForeignKey(SiteDetail, on_delete = models.CASCADE)

    def __str__(self):
        return self.name

class SiteSocial(models.Model):
    socials = (
        ('facebook','Facebook'),
        ('instagram','Instagram'),
        ('twitter','Twitter'),
        ('whatsapp','WhatsAap'))
    site = models.ForeignKey(SiteDetail, on_delete = models.CASCADE)
    social_media = models.CharField(max_length = 50, choices = socials)
    link = models.URLField()

    def __str__(self):
        return self.social_media

class Categorie(models.Model):
    name = models.CharField(max_length = 40)
    image = models.ImageField(upload_to = 'category/images')
    slug = models.SlugField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class ProductQuerySet(models.QuerySet):

    def search(self, query):
        lookup = (
                    Q(name__icontains=query) |
                    Q(slug__icontains=query) |
                    Q(description__icontains=query) |
                    Q(unit_discount_price__icontains=query)
                    )

        return self.filter(lookup)

class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def search(self, query=None):
        if query is None:
            return self.get_queryset().none()
        return self.get_queryset().search(query)

class Product(models.Model):
    currencies = (
        ('₦','naira'),
        ('＄','dollars'))
    name = models.CharField(max_length = 100)
    description = models.TextField()
    slug = models.SlugField()
    sale_currency = models.CharField(max_length = 6, choices = currencies)
    unit_price = models.CharField(max_length = 10)
    unit_discount_price = models.CharField(max_length = 10)
    quantity_available = models.CharField(max_length = 10)
    product_category = models.ManyToManyField(Categorie)
    upload_timestamp = models.DateTimeField(auto_now_add = True)

    objects = ProductManager()

    def __str__(self):
        return self.name

    def update_quantity(self, quantity_sold):
        self.quantity_available = self.quantity_available - quantity_sold

class SlideProduct(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    advert_text = models.CharField(max_length = 100)
    upload_timestamp = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.product.name

class ProductPhoto(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    image = models.ImageField(upload_to = 'products/images')

    def __str__(self):
        return self.product.name

class Subscriber(models.Model):
    email = models.EmailField()

    def __str__(self):
        return self.email

class FAQ(models.Model):
    question = models.CharField(max_length = 200)
    answer = models.TextField()
    upload_timestamp = models.DateTimeField( auto_now_add = True)

    def __str__(self):
        return self.question

class AdditionalInformation(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    feature = models.CharField(max_length = 100)
    detail = models.CharField(max_length = 100)

    def __str__(self):
        return self.product.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    quantity = models.CharField(max_length = 10)
    purchased = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.quantity} of {self.product.name}'

    def sub_total_price(self):
        total = int(self.product.unit_discount_price) * int(self.quantity)
        floattotal = float("{0:.2f}".format(total))
        return floattotal

class Client(models.Model):
    name = models.CharField(max_length = 100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name

# Order Model
class Order(models.Model):
    orderitems  = models.ManyToManyField(Cart)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    paymentId = models.CharField(max_length=200, blank=True , null=True)
    orderId = models.CharField(max_length=200, blank=True, null=True)
    
    def __str__(self):
        return self.user.username

    def total_price(self):
        total = 0
        for order_item in self.orderitems.all():
            total += order_item.sub_total_price()
        return total

class SearchQuery(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL)
    query = models.CharField(max_length=220)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.query

    class Meta:
        verbose_name_plural = "Search Queries"

class BillingAddress(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length = 20)
    lastname = models.CharField(max_length = 20)
    address = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=50)
    city = models.CharField(max_length=30)
    landmark = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.user.username} billing address'

    class Meta:
        verbose_name_plural = "Billing Addresses"


# Address Form
class BillingForm(ModelForm):

    class Meta:
        model = BillingAddress
        fields = ['firstname', 'lastname','address', 'zipcode', 'city', 'landmark']
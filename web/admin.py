from django.contrib import admin
import web.models as models

# Register your models here.
admin.site.register(models.SiteDetail)
admin.site.register(models.PhoneNumber)
admin.site.register(models.SiteSocial)
admin.site.register(models.Product)
admin.site.register(models.ProductPhoto)
admin.site.register(models.Categorie)
admin.site.register(models.FAQ)
admin.site.register(models.AdditionalInformation)
admin.site.register(models.SlideProduct)
admin.site.register(models.Order)
admin.site.register(models.Cart)
admin.site.register(models.Client)
admin.site.register(models.Subscriber)
admin.site.register(models.SearchQuery)
admin.site.register(models.BillingAddress)
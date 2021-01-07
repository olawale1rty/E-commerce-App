from django.contrib import admin
import blog.models

# Register your models here.
admin.site.register(blog.models.Author)
admin.site.register(blog.models.Categorie)
admin.site.register(blog.models.Comment)

class ArticleTextInline(admin.StackedInline):
	model = blog.models.ArticleText
	extra = 1

class ArticleImageInline(admin.StackedInline):
	model = blog.models.ArticleImage
	extra = 1

class ArticleVideoInline(admin.StackedInline):
	model = blog.models.ArticleVideo
	extra = 1

class ArticleAdmin(admin.ModelAdmin):
	fieldsets = [
	("New Content",{'fields':['author',
		'title',
		'categories',
		'featured_products',
		'publication_status',
		'slug',
		'upload_date']})]

	inlines = [
		ArticleTextInline,
		ArticleImageInline,
		ArticleVideoInline]

admin.site.register(blog.models.Article, ArticleAdmin)
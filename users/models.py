from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.text import slugify
from django.utils. translation import gettext_lazy as _
from PIL import Image
from django.core.files.storage import default_storage as storage

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    #User model with granular control

    email = models.EmailField(_('email address'), unique=True)
    # first_name = models.CharField(_('first name'), max_length=20)
    username = models.CharField(_('username'), max_length=20, unique=True)
    slug = models.SlugField(default='slug')
    is_staff = models.BooleanField(_('staff'),default=False)
    is_active = models.BooleanField(_('active'),default=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    last_login = models.DateTimeField(_('last login'), auto_now=True)
    avatar = models.ImageField(upload_to='avatars', default='default.jpg', blank=True, null=True)
    bio = models.TextField(_('Bio'), blank=True, null=True)
    social_handle = models.CharField(_('Twitter/Instagram handle'), max_length=15, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        # full_name = '%s %s' %(self.first_name, self.last_name)
        return self.username

    def get_email(self):
        return self.email

    def save(self, *args, **kwargs):
        self.slug = slugify(self.email)
        super(CustomUser, self).save()

        img = Image.open(self.avatar)

        if img.height > 514 or img.width > 534:
            output_size = (514, 534)
            img.thumbnail(output_size)
            # img.save(self.avatar.path)
            fh = storage.open(self.avatar.name, "w")
            picture_format = 'png'
            img.save(fh, picture_format)
            fh.close()
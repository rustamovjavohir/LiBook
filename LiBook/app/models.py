# from django.contrib.auth.models import User
from datetime import datetime, timedelta

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import UserManager


class User(AbstractBaseUser, PermissionsMixin):  # PermissionsMixin
    objects = UserManager()
    first_name = models.CharField(_("first name"), max_length=150, blank=True, null=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True, null=True)
    profile_image = models.ImageField(max_length=255, blank=True, null=True)
    email = models.EmailField(_("email address"), blank=True)
    username = models.CharField(_('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        error_messages={
                         'unique': _("A user with that username already exists."),
                     },)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_(
            "Designates whether the user can log into this admin site."
        ),
        null=True, blank=True
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting account."
        ), null=True, blank=True
    )
    address = models.CharField(max_length=250, blank=True, null=True)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now, null=True, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ['id']

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    @property
    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def update_profile(self, validated_data):
        self.first_name = validated_data.get("first_name", self.first_name)
        self.last_name = validated_data.get("last_name", self.last_name)
        self.profile_image = validated_data.get(
            "profile_image", self.profile_image
        )
        self.email = validated_data.get("email", self.email)
        self.date_of_birth = validated_data.get(
            "date_of_birth", self.date_of_birth
        )
        self.save()
        return self

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def photo_url(self):
        try:
            return self.profile_image.url
        except Exception as e:
            return ''


class Category(models.Model):
    name = models.CharField("Kategoriya name", max_length=100, null=True)
    photo = models.ImageField(null=True, blank=True)
    views = models.IntegerField(default=0)
    status = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        try:
            return self.name
        except Exception as e:
            return ""


class Book(models.Model):
    TYPE = (('AUDIO', "AUDIO"),
            ("DOC", "DOC"))
    LANG = (('UZ', "UZ"),
            ("RU", "RU"))
    category_list = Category.objects.all()
    CATEGORY_NAME = ()
    for obj in category_list:
        my_tuple = ((f"{obj.name.upper()}", f"{obj.name}"),)
        CATEGORY_NAME += my_tuple
    category = models.CharField(choices=CATEGORY_NAME, default='Lirika', max_length=250)
    author = models.CharField(max_length=100, null=True)
    name = models.CharField(max_length=100, null=True)
    about = models.TextField(null=True)
    file = models.FileField(null=True)
    add_date = models.DateField(auto_now_add=True, blank=True)
    photo = models.ImageField(null=True, blank=True)
    status = models.IntegerField(null=True, blank=True)
    type = models.CharField(max_length=6, null=True, choices=TYPE, default="DOC")
    lang = models.CharField(max_length=2, null=True, default="UZ", choices=LANG)
    views = models.IntegerField(default=0)
    price = models.IntegerField(default=5000)
    rate = models.IntegerField(default=0)
    count = models.IntegerField(default=1)
    sold_num = models.IntegerField(default=0)

    # @property
    def __str__(self):
        return self.name

    @property
    def file_url(self):
        try:
            return self.file.url
        except Exception as e:
            return ''

    @property
    def photo_url(self):
        try:
            return self.photo.url
        except Exception as e:
            return ''

    class Meta:
        ordering = ['id']


class Box(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    is_delivered = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.book.name


class Advice(models.Model):
    text = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    telegram_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        try:
            return self.text[:20]
        except Exception as e:
            return ''


class Discount(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    new_price = models.IntegerField()
    stat = models.DateTimeField(auto_now_add=True)
    finish_date = models.DateTimeField(default=datetime.now() + timedelta(days=5))
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.book} {self.new_price}"

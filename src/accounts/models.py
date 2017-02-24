from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.core.validators import EmailValidator

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.CharField('email address', max_length=150, unique=True, validators=[EmailValidator])
    first_name = models.CharField('first name', max_length=30, blank=True)
    last_name = models.CharField('last name', max_length=30, blank=True)
    date_joined = models.DateTimeField('date joined', auto_now_add=True)
    birthday = models.DateField('birthday', blank=True, null=True)
    country = models.CharField('country', max_length=30, blank=True)
    city = models.CharField('city', max_length=30, blank=True)
    is_active = models.BooleanField('active', default=False)
    is_staff = models.BooleanField('staff status', default=False)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def username(self):
        return self.email.split('@')[0]

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)
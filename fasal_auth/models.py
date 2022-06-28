from typing import List
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy  as _

# Create your models here.
class UserManager(BaseUserManager):

    def _create_user(self,email,password,**extra_fields):

        if not email:
            raise ValueError('The email must be set')
        
        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self,email,password,**extra_fields):
        extra_fields.setdefault('is_superuser',False)
        return self._create_user(email,password,**extra_fields)
    
    def create_superuser(self,email,password,**extra_fields):
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_staff',True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email,password,**extra_fields)



class User(AbstractBaseUser,PermissionsMixin):
    email = models.CharField(_('email address'),max_length=50,unique=True)
    first_name = models.CharField(_('first name'),max_length=30,blank=True)
    last_name = models.CharField(_('last name'),max_length=30,blank=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS: List[str] = []

    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        
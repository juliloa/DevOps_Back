from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from .roles import Roles

class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        return self.create_user(email, name, password, **extra_fields)

class Users(AbstractBaseUser):
    id_card = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=100)
    email = models.CharField(unique=True, max_length=150)
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True, null=True)
    warehouse = models.ForeignKey('Warehouses', models.DO_NOTHING, blank=True, null=True)
    role = models.ForeignKey(Roles, models.DO_NOTHING)
    status = models.BooleanField(blank=True, null=True)
    last_login = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'id_card']

    objects = CustomUserManager()

    # is_authenticated siempre devuelve True para el usuario autenticado
    @property
    def is_authenticated(self):
        return True

    # is_anonymous siempre devuelve False para el usuario autenticado
    @property
    def is_anonymous(self):
        return False

    @property
    def is_active(self):
        return self.status if self.status is not None else True

    def __str__(self):
        return self.email

    class Meta:
        managed = False
        db_table = 'users'

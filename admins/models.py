from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, admin_id, email, password=None, **extra_fields):
        if not email:
            raise ValueError('이메일 주소를 입력해주세요.')
        email = self.normalize_email(email)
        user = self.model(admin_id=admin_id, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, admin_id, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        return self.create_user(admin_id, email, password, **extra_fields)

    def create_superuser(self, admin_id, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(admin_id, email, password, **extra_fields)


class Admin(AbstractBaseUser, PermissionsMixin):
    admins_id = models.AutoField(primary_key=True)
    admin_id = models.CharField(max_length=30, blank=True, unique=True)
    cell_num = models.CharField(max_length=11, blank=True, unique=True)
    email = models.CharField(max_length=50, blank=True, unique=True)
    create_date = models.DateTimeField(auto_now_add=True)
    last_date = models.DateTimeField(null=True)
    adms_id = models.IntegerField(null=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'admin_id'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser



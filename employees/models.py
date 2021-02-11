from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
import uuid


# Create your models here.
class UserManager(BaseUserManager):

    def _create_user(self, email,name, password, is_staff, is_superuser):
        if not email:
            raise ValueError('Users must have an email address')
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            name=name,
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self,name, email, password):
        user = self._create_user(email, name, password, False, False)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        user = self._create_user(email = email, name = name, password = password, is_staff= True, is_superuser= True)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)
    def get_email(self):
        return self.email

class Company(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    blood_group = models.CharField(max_length=5)
    address = models.TextField()
    phone_number = models.BigIntegerField()
    position = models.CharField(max_length=50)
    company = models.ForeignKey(to=Company, on_delete=models.SET_NULL, null=True)
    details = models.BooleanField(default=False)
    working = models.BooleanField(default=False)
    work_log_id = models.UUIDField(null=True)

    def __str__(self):
        return self.user.name

class Work_log(models.Model):
    employee = models.ForeignKey(to=Employee, on_delete=models.SET_NULL, null=True)
    date = models.DateField(default=timezone.now)
    start_time = models.TimeField(default=timezone.now)
    work_log_id = models.UUIDField(default = uuid.uuid4, editable = False)
    end_time = models.TimeField(null=True)
    worked_on = models.CharField(max_length=200)
    work_description = models.TextField(null=True)
    work_file = models.FileField(upload_to='workfiles/%Y/%m/%d',null=True)


    def __str__(self):
        return self.employee.user.name



from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError

def validate_age(value):
    age = relativedelta(timezone.now().date(), value).years
    if age < 14:
        raise ValidationError('User must be at least 14 years old.')

def validate_fullname(value):
    valid_chars = all(char.isalpha() or char.isspace() for char in value)
    if not valid_chars:
        raise ValidationError('Full name should only contain letters and spaces.')


class UserManager(BaseUserManager):
    def create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError('The email field must be set')
        if not password:
            raise ValueError('The password field must be set')
        if not username:
            raise ValueError('The username field must be set')

        email_normalized = self.normalize_email(email)
        user = self.model(username=username, email=email_normalized, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True, validators=[RegexValidator(r'^[a-zA-Z0-9_]+$')])
    email = models.EmailField(max_length=150, unique=True)
    fullname = models.CharField(max_length=255, validators=[validate_fullname])
    birthday = models.DateField(validators=[validate_age])
    picture = models.BinaryField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'fullname', 'birthday']

    def __str__(self):
        return self.username
    
class Business(models.Model):
    email = models.EmailField(max_length=150, unique=True)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_businesses')

class Team(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)

class Employee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ('user', 'business')

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()
    progress = models.FloatField(default=0.0)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    business = models.ForeignKey(Business, on_delete=models.SET_NULL, null=True, blank=True)

    def clean(self):
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError("Start date must be before or equal to end date.")

class Role(models.Model):
    name = models.CharField(max_length=20, unique=True, default='Guest', validators=[RegexValidator(r'^[\p{L} ]+$')])
    perm = models.IntegerField(default=0)

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('L', 'LOW'),
        ('M', 'MEDIUM'),
        ('H', 'HIGH'),
    ]
    STATUS_CHOICES = [
        ('TODO', 'To do'),
        ('IN_PROGRESS', 'In progress'),
        ('DONE', 'Done'),
    ]
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, default='L')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='TODO')
    user_assigned = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    team_assigned = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)

    def clean(self):
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError("Start date must be before or equal to end date.")

class UserProjectRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ('user', 'project')

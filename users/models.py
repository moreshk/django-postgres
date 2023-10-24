from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

    
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    USER_TYPES = (
    ('TEACHER', 'Teacher'),
    ('STUDENT', 'Student'),
    ('PARENT', 'Parent'),
    ('ADMINISTRATOR', 'Administrator')
    )

    user_type = models.CharField(max_length=15, choices=USER_TYPES, default='Student')
    has_completed_onboarding = models.BooleanField(default=False)
    objects = CustomUserManager()

class GradeResult(models.Model):
    user_id = models.IntegerField()
    feedback = models.TextField()
    numeric_grade = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    grading_criteria = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
    assignment_id = models.IntegerField(null=True, blank=True)

class Assignment(models.Model):
    teacher_id = models.IntegerField()
    assignment_type = models.CharField(max_length=255)
    assignment_sub_type = models.CharField(max_length=255)
    grade = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    task_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255)

    class Meta:
        db_table = 'assignments'


# New School model
class School(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    admin_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255)
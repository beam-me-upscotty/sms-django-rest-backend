from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)
import datetime
from .utils import USER_TYPE_CHOICES, YEAR_TYPE_CHOICES


class Department(models.Model):
    name = models.CharField(max_length=20)
    duration = models.IntegerField()


class Course(models.Model):
    name = models.CharField(max_length=20)
    department = models.ManyToManyField(Department)


class Subject(models.Model):
    name = models.CharField(max_length=20, unique=True)
    course = models.ManyToManyField(Course)


class UserManager(BaseUserManager):

    use_in_migrations = True

    def create_user(self, username, name, user_type, password=None):
        user = self.model(
            username=username,
            user_type=user_type,
            name=name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, username, name, user_type, password):
        user = self.create_user(
            username,
            password=password,
            user_type=user_type,
            name=name,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, username, name, user_type, password):
        user = self.create_user(
            username,
            password=password,
            user_type=user_type,
            name=name,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):

    username = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=12)
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=1)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'user_type']

    def __str__(self):
        return self.username

    objects = UserManager()


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    year_of_study = models.PositiveSmallIntegerField(choices=YEAR_TYPE_CHOICES, default=1)


class Parent(models.Model):
    parent = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    child = models.ManyToManyField(Student)


class Teacher(models.Model):
    class Meta:
        unique_together = (('user', 'subject'),)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)


class Exam(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    year_of_study = models.PositiveSmallIntegerField(choices=YEAR_TYPE_CHOICES, default=1)
    total_marks = models.IntegerField()
    creation_date = models.DateField(auto_now_add=True)


class Marks(models.Model):
    class Meta:
        unique_together = (('student', 'exam'),)

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    marks_scored = models.IntegerField()


class Attendance(models.Model):
    date = models.DateField(default=datetime.datetime.now)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)



from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)
import datetime


class Department(models.Model):
    name = models.CharField(max_length=20)
    duration = models.IntegerField()


class Course(models.Model):
    name = models.CharField(max_length=20)
    department = models.ManyToManyField(Department)


class Subject(models.Model):
    name = models.CharField(max_length=20)
    course = models.ManyToManyField(Course)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save()
        return user

    def create_user_main(self, email, password, name):

        user = self.create_user(
            email,
            password=password,
        )
        user.name = name
        return user

    def create_teacher(self, email, password, name):
        user = self.create_user_main(
            email,
            password=password,
            name=name
        )
        user.teacher = True
        user.save()
        return user

    def create_student(self, email, password, name):
        user = self.create_user_main(
            email,
            password=password,
            name=name
        )
        user.student = True
        user.save()
        return user

    def create_parent(self, email, password, name):
        user = self.create_user_main(
            email,
            password=password,
            name=name
        )
        user.parent = True
        user.save()
        return user


class User(AbstractBaseUser):
    name = models.CharField(max_length=20)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    is_teacher = models.BooleanField(default=False)
    is_parent = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        # The user is identified by their email address
        return self.name

    def __str__(self):
        return self.name.__str__() + "(" + self.email.__str__() + ")"

    def has_module_perms(self, app_label):

        return True

    @property
    def is_teacher(self):
        return self.is_teacher

    @property
    def is_student(self):
        return self.is_student

    @property
    def is_parent(self):
            return self.is_parent

    objects = UserManager()


class Parent(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)


class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    year_of_study = models.IntegerField()
    has_parent = models.ForeignKey(Parent, on_delete=models.CASCADE)


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
    total_marks = models.IntegerField()


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



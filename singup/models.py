from django.db import models
from django.utils.functional import lazy
from django.contrib.auth.models import User
import logging
# from .views import requests

# Create your models here.
# from singup.middleware.request_exposer import get_current_request


# exposed_request = None

class Teacher(models.Model):
    username = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    dateofbirth = models.DateField()
    
class Student(models.Model):
    username = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    dateofbirth = models.DateField()

teachers = lazy(lambda: tuple((teacher.username, teacher.username) for teacher in Teacher.objects.all()), tuple)
classes = (
    ('1A', '1A'),
    ('1B', '1B'),
    ('2A', '2A'),
    ('2B', '2B'),
    ('3A', '3A'),
    ('3B', '3B'),
    ('4A', '4A'),
    ('4B', '4B'),
    ('5A', '5A'),
    ('5B', '5B')
)

class TeacherClass(models.Model):
    teacher = models.CharField(max_length=100, choices=teachers())
    assigned = models.CharField(max_length=5, choices=classes)

    def __str__(self):
        return self.assigned
    


# import threading

# thread_local = threading.local()

# def get_current_request():
#     return getattr(thread_local, 'request', None)

# def set_current_request(request):
#     thread_local.request = request

# def your_method():
#     request = get_current_request()
#     username=None
#     if request:
#         # Access the request object attributes as needed
#         username = request.user.username
#         # Perform your logic using the request object
#         # ...
#     else:
#         # Handle the case when the request is not available
#         pass
#     return username
# temp = get_current_request()
# print(temp)

students = lazy(lambda: tuple((student.username, student.username) for student in Student.objects.all()), tuple)
# teacherclass = lazy(
#     lambda: tuple(
#         (teacher.assigned, teacher.assigned) 
#         for teacher in TeacherClass.objects.filter(teacher=user)
#     ),
#     tuple
# )
class StudentClass(models.Model):
    student = models.CharField(max_length=100, choices=students())
    assignclass = models.CharField(max_length=5, choices=classes)

examtypes = (('Sem1', 'Sem1'), ('Sem2', 'Sem2'), ('Finals', 'Finals'))
class Marks(models.Model):
    username = models.CharField(max_length=100)
    exam_type = models.CharField(max_length=10, choices=examtypes)
    maths = models.DecimalField(max_digits=4, decimal_places=2)
    science = models.DecimalField(max_digits=4, decimal_places=2)
    labs = models.DecimalField(max_digits=4, decimal_places=2)
    sports = models.DecimalField(max_digits=4, decimal_places=2)
    percentage = models.DecimalField(max_digits=4, decimal_places=2)
    pf = models.BooleanField(default=False  )

    def save(self, *args, **kwargs):
        self.percentage = (self.maths +  self.science +  self.labs  +  self.sports)/400
        self.pf = self.percentage > 35
        super(Marks, self).save(*args, **kwargs)

    def __str__(self):
        return f"Exam Type: {self.exam_type}, Maths: {self.maths}, Science: {self.science}, Labs: {self.labs}, Sports: {self.sports}, Percentage: {self.percentage}, Final Result: {self.pf}"

    
    




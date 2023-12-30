from django.db import models

class Employee(models.Model):
    Emp_First_Name = models.CharField(max_length=10)
    Emp_Last_Name = models.CharField(max_length=10)
    Emp_Designation = models.CharField(max_length=20)
    Emp_Salary = models.IntegerField()
    Emp_Company = models.CharField(max_length=20)
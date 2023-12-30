from django.urls import path
from .views import EmployeeAPI, EmployeeDetail

urlpatterns = [
    path('Employee/', EmployeeAPI.as_view()),
    path('employee-retrive/<int:pk>/',EmployeeDetail.as_view()),
]
